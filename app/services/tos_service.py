import os
import uuid
import mimetypes
from datetime import datetime
from typing import Optional, List, Tuple
from io import BytesIO
import logging

import tos
from fastapi import UploadFile, HTTPException
from PIL import Image

from tos import HttpMethodType

from urllib.parse import quote

from app.config.tos_config import TosConfig
from app.models.tos_models import (
    UploadFileData, BatchUploadData, FailedFileInfo, FileInfo, PreViewData
)
from app.utils.get_content_type_util import get_content_type

logger = logging.getLogger(__name__)


class TosService:
    """火山云TOS对象存储服务"""

    def __init__(self, tos_config: TosConfig):
        """
        初始化TOS服务

        Args:
            tos_config: TOS配置对象
        """
        self.config = tos_config
        self.client = self._init_client()

    def _init_client(self) -> tos.TosClientV2:
        """初始化TOS客户端 - 使用官方SDK标准方式"""
        try:
            # 按照官方SDK方式初始化客户端
            # 参数顺序：ak, sk, endpoint, region
            client = tos.TosClientV2(
                ak=self.config.access_key,  # ak 参数
                sk=self.config.secret_key,  # sk 参数
                endpoint=self.config.endpoint,  # endpoint 参数
                region=self.config.region,  # region 参数
                enable_verify_ssl=True,  # 是否启用SSL验证
            )
            print(f"TOS客户端初始化成功 tosconfig:{self.config}")
            return client
        except tos.exceptions.TosClientError as e:
            # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
            error_msg = f"TOS客户端异常: {e.message}, cause: {e.cause}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        except tos.exceptions.TosServerError as e:
            # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
            error_msg = f"TOS服务端异常: code={e.code}, message={e.message}, request_id={e.request_id}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)
        except Exception as e:
            error_msg = f"TOS客户端初始化失败: {str(e)}"
            logger.error(error_msg)
            raise HTTPException(status_code=500, detail=error_msg)

    def _validate_file(self, file: UploadFile) -> None:
        """
        验证上传文件

        Args:
            file: 上传的文件
            file_type: 文件类型 (image/video)

        Raises:
            HTTPException: 文件验证失败时抛出异常
        """
        # 检查文件大小
        if hasattr(file, 'size') and file.size > self.config.max_file_size:
            raise HTTPException(
                status_code=413,
                detail=f"文件大小超过限制: {self.config.max_file_size / 1024 / 1024}MB"
            )

        # 获取文件扩展名
        file_ext = file.filename.split('.')[-1].lower() if file.filename else ""

    def _generate_file_path(self, original_filename: str, file_type: str, custom_path: Optional[str] = None) -> str:
        """
        生成文件存储路径

        Args:
            original_filename: 原始文件名
            file_type: 文件类型
            custom_path: 自定义路径

        Returns:
            str: 生成的文件路径
        """
        # 生成唯一文件名
        file_ext = original_filename.split('.')[-1].lower() if original_filename else ""
        unique_filename = f"{uuid.uuid4().hex}.{file_ext}"

        # 构建存储路径
        if custom_path:
            # 使用自定义路径
            base_path = custom_path.strip('/')
        else:
            # 使用默认路径
            if file_type == "image":
                base_path = self.config.image_prefix.strip('/')
            else:
                base_path = self.config.video_prefix.strip('/')

        # 按日期分组
        date_path = datetime.now().strftime("%Y/%m/%d")

        return f"{base_path}/{date_path}/{unique_filename}"

    async def upload_file(
            self,
            file: UploadFile,
            custom_path: Optional[str] = None,
            generate_thumbnail: bool = False
    ) -> UploadFileData:
        """
        上传单个文件

        Args:
            file: 上传的文件
            file_type: 文件类型 (image/video)
            custom_path: 自定义存储路径
            generate_thumbnail: 是否生成缩略图

        Returns:
            UploadFileData: 上传结果数据
        """
        try:
            # 验证文件
            self._validate_file(file)

            # 读取文件内容
            file_content = await file.read()
            file_size = len(file_content)

            # 生成存储路径
            file_path = self._generate_file_path(file.filename, "image", custom_path)

            # 获取MIME类型
            mime_type = mimetypes.guess_type(file.filename)[0] or 'application/octet-stream'

            # 使用官方SDK标准方式上传文件到TOS
            content = BytesIO(file_content)
            content.seek(0)  # 重置指针到开头，确保上传完整文件
            try:
                result = self.client.put_object(self.config.bucket_name, file_path, content=content,
                                                content_type=mime_type)
                # HTTP状态码
                logger.info('http status code:{}'.format(result.status_code))
                # 请求ID。请求ID是本次请求的唯一标识，建议在日志中添加此参数
                logger.info('request_id: {}'.format(result.request_id))
                # hash_crc64_ecma 表示该对象的64位CRC值, 可用于验证上传对象的完整性
                logger.debug('crc64: {}'.format(result.hash_crc64_ecma))
                logger.info(f"文件上传成功: {file.filename} -> {file_path}")

            except tos.exceptions.TosClientError as e:
                # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
                error_msg = 'fail with client error, message:{}, cause: {}'.format(e.message, e.cause)
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=f"文件上传失败: {error_msg}")
            except tos.exceptions.TosServerError as e:
                # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
                error_msg = 'fail with server error, code: {}'.format(e.code)
                # request id 可定位具体问题，强烈建议日志中保存
                logger.error('error with request id: {}'.format(e.request_id))
                logger.error('error with message: {}'.format(e.message))
                logger.error('error with http code: {}'.format(e.status_code))
                logger.error('error with ec: {}'.format(e.ec))
                logger.error('error with request url: {}'.format(e.request_url))
                raise HTTPException(status_code=500, detail=f"文件上传失败: {error_msg}")
            except Exception as e:
                error_msg = 'fail with unknown error: {}'.format(e)
                logger.error(error_msg)
                raise HTTPException(status_code=500, detail=f"文件上传失败: {error_msg}")

            # # 生成缩略图（仅图片）
            # thumbnail_url = None
            # if generate_thumbnail and file_type == "image":
            #     thumbnail_data = self._generate_thumbnail(file_content)
            #     if thumbnail_data:
            #         thumbnail_path = file_path.replace(f".{file_path.split('.')[-1]}", "_thumb.jpg")
            #         try:
            #             # 使用官方SDK方式上传缩略图
            #             thumbnail_content = BytesIO(thumbnail_data)
            #             thumb_result = self.client.put_object(self.config.bucket_name, thumbnail_path,
            #                                                   content=thumbnail_content)
            #             # 记录缩略图上传结果
            #             logger.debug('thumbnail http status code:{}'.format(thumb_result.status_code))
            #             logger.debug('thumbnail request_id: {}'.format(thumb_result.request_id))
            #             logger.debug('thumbnail crc64: {}'.format(thumb_result.hash_crc64_ecma))
            #             thumbnail_url = self._get_file_url(thumbnail_path)
            #         except tos.exceptions.TosClientError as e:
            #             # 操作失败，捕获客户端异常，一般情况为非法请求参数或网络异常
            #             logger.error(
            #                 'thumbnail fail with client error, message:{}, cause: {}'.format(e.message, e.cause))
            #             # 缩略图上传失败不影响主文件上传
            #         except tos.exceptions.TosServerError as e:
            #             # 操作失败，捕获服务端异常，可从返回信息中获取详细错误信息
            #             logger.error('thumbnail fail with server error, code: {}'.format(e.code))
            #             logger.error('thumbnail error with request id: {}'.format(e.request_id))
            #             logger.error('thumbnail error with message: {}'.format(e.message))
            #             # 缩略图上传失败不影响主文件上传
            #         except Exception as e:
            #             logger.error('thumbnail fail with unknown error: {}'.format(e))
            #             # 缩略图上传失败不影响主文件上传

            # 构建返回数据
            upload_data = UploadFileData(
                file_id=uuid.uuid4().hex,
                original_name=file.filename,
                file_name=os.path.basename(file_path),
                file_path=file_path,
                file_url=file_path,
                file_size=file_size,
                # file_type=file_type,
                mime_type=mime_type,
                upload_time=datetime.now(),
                # thumbnail_url=thumbnail_url
            )

            logger.info(f"文件上传成功: {file.filename} -> {file_path}")
            return upload_data

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"文件上传失败: {str(e)}")
            raise HTTPException(status_code=500, detail=f"文件上传失败: {str(e)}")

    async def batch_upload_files(
            self,
            files: List[UploadFile],
            file_type: str,
            custom_path: Optional[str] = None,
            generate_thumbnail: bool = False
    ) -> BatchUploadData:
        """
        批量上传文件

        Args:
            files: 上传的文件列表
            file_type: 文件类型 (image/video)
            custom_path: 自定义存储路径
            generate_thumbnail: 是否生成缩略图

        Returns:
            BatchUploadData: 批量上传结果数据
        """
        success_files = []
        failed_files = []

        for file in files:
            try:
                upload_data = await self.upload_file(file, custom_path)
                success_files.append(upload_data)
            except Exception as e:
                failed_files.append(FailedFileInfo(
                    original_name=file.filename,
                    error_message=str(e)
                ))

        return BatchUploadData(
            total_count=len(files),
            success_count=len(success_files),
            failed_count=len(failed_files),
            success_files=success_files,
            failed_files=failed_files
        )

    def delete_file(self, file_path: str) -> bool:
        """
        删除文件

        Args:
            file_path: 文件路径

        Returns:
            bool: 删除是否成功
        """
        try:
            result = self.client.delete_object(
                bucket=self.config.bucket_name,
                key=file_path
            )
            logger.info(f"文件删除成功: {file_path}, request_id={result.request_id}")
            return True
        except tos.exceptions.TosClientError as e:
            logger.error(f"文件删除客户端异常: {file_path}, message={e.message}, cause={e.cause}")
            return False
        except tos.exceptions.TosServerError as e:
            logger.error(f"文件删除服务端异常: {file_path}, code={e.code}, message={e.message}")
            return False
        except Exception as e:
            logger.error(f"文件删除未知异常: {file_path}, 错误: {str(e)}")
            return False

    def get_file_info(self, file_path: str) -> Optional[FileInfo]:
        """
        获取文件信息

        Args:
            file_path: 文件路径

        Returns:
            Optional[FileInfo]: 文件信息，不存在时返回None
        """
        try:
            print(f"正在获取文件信息: {file_path, self.config.bucket_name}")
            response = self.client.head_object(
                bucket=self.config.bucket_name,
                key=file_path
            )
            logger.debug(f"获取文件信息成功: {file_path}, request_id={response.request_id}")

            return FileInfo(
                file_name=os.path.basename(file_path),
                file_path=file_path,
                file_size=response.content_length,
                last_modified=response.last_modified,
                content_type=response.content_type,
                etag=response.etag
            )
        except tos.exceptions.TosClientError as e:
            logger.error(f"获取文件信息客户端异常: {file_path}, message={e.message}, cause={e.cause}")
            return None
        except tos.exceptions.TosServerError as e:
            logger.error(f"获取文件信息服务端异常: {file_path}, code={e.code}, message={e.message}")
            return None
        except Exception as e:
            logger.error(f"获取文件信息未知异常: {file_path}, 错误: {str(e)}")
            return None

    def file_exists(self, file_path: str) -> bool:
        """
        检查文件是否存在

        Args:
            file_path: 文件路径

        Returns:
            bool: 文件是否存在
        """
        return self.get_file_info(file_path) is not None

    def get_bucket_name(self) -> str:
        """
        获取桶名称

        Returns:
            str: 桶名称
        """
        return self.config.bucket_name

    async def get_pre_signed_url(self, file_path) -> str:
        """
        获取预签名URL
        """
        content_disposition_value = quote('inline')  # 将 'inline' 进行 URL 编码，虽然这里结果还是 inline
        content_type_value = get_content_type(file_path)
        # tos://mt-znwl-tos/videos/2025/12/11/
        # 生成预览链接（浏览器内嵌显示）
        preview_url = self.client.pre_signed_url(
            # 下载用 GET；上传用 PUT/POST
            http_method=HttpMethodType.Http_Method_Get,
            bucket=self.config.bucket_name,
            key=file_path,
            expires=3600,  # 过期时间（秒）
            query={
                # 强制浏览器预览 (inline)
                'response-content-disposition': content_disposition_value,
                # 强制 Content-Type 为图片类型
                'response-content-type': content_type_value
            }
            # 可选：添加响应头控制下载行为
        ).signed_url
        return preview_url
