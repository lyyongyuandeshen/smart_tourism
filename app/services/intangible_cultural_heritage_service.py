from typing import List, Optional
from datetime import datetime
import uuid
from mysql.connector import pooling
from fastapi import UploadFile, HTTPException

from app.repository.intangible_cultural_heritage_repo import IntangibleCulturalHeritageRepository
from app.models.intangible_cultural_heritage_models import (
    IntangibleCulturalHeritageResponse,
    IntangibleCulturalHeritageCreate,
    IntangibleCulturalHeritageUpdate,
    IntangibleCulturalHeritageQueryRequest,
    IntangibleCulturalHeritageListResponse,
    IntangibleCulturalHeritageUploadResponse,
    IntangibleCulturalHeritageDeleteResponse
)
from app.services.tos_service import TosService
from app.models.tos_models import UploadFileData


class IntangibleCulturalHeritageService:
    """非遗技艺业务服务类"""

    def __init__(self, pool: pooling.MySQLConnectionPool, tos_service: TosService):
        self.heritage_repo = IntangibleCulturalHeritageRepository(pool)
        self.tos_service = tos_service

    def _generate_heritage_number(self) -> str:
        """
        生成非遗编号
        
        Returns:
            非遗编号，格式：SNYYYYMMDDXXXXX
        """
        # 获取当前日期
        current_date = datetime.now().strftime("%Y%m%d")
        
        # 获取最大编号
        max_number = self.heritage_repo.get_max_heritage_number()
        
        if max_number and max_number.startswith(f"SN{current_date}"):
            # 如果当天已有编号，递增序号
            sequence = int(max_number[-5:]) + 1
            new_sequence = f"{sequence:05d}"
        else:
            # 当天第一个编号
            new_sequence = "00001"
        
        return f"SN{current_date}{new_sequence}"

    async def upload_video_and_create_heritage(
        self, 
        heritage_data: IntangibleCulturalHeritageCreate,
        video_file: UploadFile
    ) -> IntangibleCulturalHeritageUploadResponse:
        """
        上传视频并创建非遗技艺记录
        
        Args:
            heritage_data: 非遗技艺数据
            video_file: 视频文件
            
        Returns:
            上传响应
        """
        try:
            # 1. 上传视频到TOS
            upload_result: UploadFileData = await self.tos_service.upload_file(
                file=video_file,
                custom_path="intangible_cultural_heritage/videos"
            )
            
            # 2. 生成非遗编号
            heritage_number = self._generate_heritage_number()
            
            # 3. 创建非遗技艺记录
            heritage_record = {
                'heritage_number': heritage_number,
                'heritage_name': heritage_data.heritage_name,
                'interactive_question_bank': heritage_data.interactive_question_bank,
                'video_url': upload_result.file_path,  # 使用TOS返回的文件路径
                'is_published': False  # 默认不发布
            }
            
            rows_affected = self.heritage_repo.create_intangible_cultural_heritage(heritage_record)
            
            if rows_affected > 0:
                return IntangibleCulturalHeritageUploadResponse(
                    success=True,
                    message="非遗技艺创建成功",
                    heritage_number=heritage_number,
                    video_url=upload_result.file_path
                )
            else:
                # 如果数据库插入失败，删除已上传的视频文件
                await self.tos_service.delete_file(upload_result.file_path)
                return IntangibleCulturalHeritageUploadResponse(
                    success=False,
                    message="非遗技艺创建失败"
                )
                
        except HTTPException:
            raise
        except Exception as e:
            return IntangibleCulturalHeritageUploadResponse(
                success=False,
                message=f"创建非遗技艺失败：{str(e)}"
            )

    def query_intangible_cultural_heritages(
        self, 
        request: IntangibleCulturalHeritageQueryRequest
    ) -> IntangibleCulturalHeritageListResponse:
        """
        查询非遗技艺列表
        
        Args:
            request: 查询请求参数
            
        Returns:
            非遗技艺列表响应
        """
        try:
            # 计算偏移量
            offset = (request.page - 1) * request.page_size
            
            # 查询非遗技艺列表
            heritages = self.heritage_repo.get_intangible_cultural_heritages(
                heritage_number=request.heritage_number,
                heritage_name=request.heritage_name,
                interactive_question_bank=request.interactive_question_bank,
                is_published=request.is_published,
                offset=offset,
                limit=request.page_size
            )
            
            # 查询总数
            total = self.heritage_repo.count_intangible_cultural_heritages(
                heritage_number=request.heritage_number,
                heritage_name=request.heritage_name,
                interactive_question_bank=request.interactive_question_bank,
                is_published=request.is_published
            )
            
            # 转换为响应模型
            heritage_list = [
                IntangibleCulturalHeritageResponse(
                    id=h['id'],
                    heritage_number=h['heritage_number'],
                    heritage_name=h['heritage_name'],
                    interactive_question_bank=h['interactive_question_bank'],
                    video_url=h['video_url'],
                    is_published=h['is_published'],
                    created_at=h['created_at'],
                    updated_at=h['updated_at']
                )
                for h in heritages
            ]
            
            return IntangibleCulturalHeritageListResponse(
                success=True,
                message="查询成功",
                total=total,
                page=request.page,
                page_size=request.page_size,
                data=heritage_list
            )
            
        except Exception as e:
            return IntangibleCulturalHeritageListResponse(
                success=False,
                message=f"查询失败：{str(e)}",
                total=0,
                page=request.page,
                page_size=request.page_size,
                data=[]
            )

    def search_by_heritage_name(self, heritage_name: str, page: int = 1, page_size: int = 10) -> IntangibleCulturalHeritageListResponse:
        """
        根据非遗名称模糊搜索
        
        Args:
            heritage_name: 非遗名称（模糊匹配）
            page: 页码
            page_size: 每页数量
            
        Returns:
            非遗技艺列表响应
        """
        request = IntangibleCulturalHeritageQueryRequest(
            heritage_name=heritage_name,
            page=page,
            page_size=page_size
        )
        return self.query_intangible_cultural_heritages(request)

    def get_all_heritages(self, page: int = 1, page_size: int = 10) -> IntangibleCulturalHeritageListResponse:
        """
        查询全量非遗技艺列表
        
        Args:
            page: 页码
            page_size: 每页数量
            
        Returns:
            非遗技艺列表响应
        """
        request = IntangibleCulturalHeritageQueryRequest(
            page=page,
            page_size=page_size
        )
        return self.query_intangible_cultural_heritages(request)

    def get_published_heritages(self, page: int = 1, page_size: int = 10) -> IntangibleCulturalHeritageListResponse:
        """
        获取已发布的非遗视频全量信息
        
        Args:
            page: 页码
            page_size: 每页数量
            
        Returns:
            已发布的非遗技艺列表响应
        """
        request = IntangibleCulturalHeritageQueryRequest(
            is_published=True,
            page=page,
            page_size=page_size
        )
        return self.query_intangible_cultural_heritages(request)

    def get_intangible_cultural_heritage_by_number(self, heritage_number: str) -> Optional[IntangibleCulturalHeritageResponse]:
        """
        根据非遗编号查询非遗技艺详情
        
        Args:
            heritage_number: 非遗编号
            
        Returns:
            非遗技艺详情
        """
        try:
            heritage = self.heritage_repo.get_intangible_cultural_heritage_by_number(heritage_number)
            
            if not heritage:
                return None
            
            return IntangibleCulturalHeritageResponse(
                id=heritage['id'],
                heritage_number=heritage['heritage_number'],
                heritage_name=heritage['heritage_name'],
                interactive_question_bank=heritage['interactive_question_bank'],
                video_url=heritage['video_url'],
                is_published=heritage['is_published'],
                created_at=heritage['created_at'],
                updated_at=heritage['updated_at']
            )
            
        except Exception as e:
            return None

    def update_intangible_cultural_heritage(
        self, 
        heritage_number: str, 
        update_data: IntangibleCulturalHeritageUpdate
    ) -> IntangibleCulturalHeritageUploadResponse:
        """
        更新非遗技艺信息
        
        Args:
            heritage_number: 非遗编号
            update_data: 更新数据
            
        Returns:
            更新响应
        """
        try:
            # 检查非遗技艺是否存在
            existing_heritage = self.heritage_repo.get_intangible_cultural_heritage_by_number(heritage_number)
            
            if not existing_heritage:
                return IntangibleCulturalHeritageUploadResponse(
                    success=False,
                    message=f"非遗技艺不存在：{heritage_number}"
                )
            
            # 构建更新数据
            heritage_data = {}
            if update_data.heritage_name is not None:
                heritage_data['heritage_name'] = update_data.heritage_name
            if update_data.interactive_question_bank is not None:
                heritage_data['interactive_question_bank'] = update_data.interactive_question_bank
            if update_data.video_url is not None:
                heritage_data['video_url'] = update_data.video_url
            if update_data.is_published is not None:
                heritage_data['is_published'] = update_data.is_published
            
            # 如果没有需要更新的字段
            if not heritage_data:
                return IntangibleCulturalHeritageUploadResponse(
                    success=False,
                    message="没有需要更新的字段"
                )
            
            # 更新非遗技艺
            rows_affected = self.heritage_repo.update_intangible_cultural_heritage(heritage_number, heritage_data)
            
            if rows_affected > 0:
                return IntangibleCulturalHeritageUploadResponse(
                    success=True,
                    message="非遗技艺更新成功",
                    heritage_number=heritage_number
                )
            else:
                return IntangibleCulturalHeritageUploadResponse(
                    success=False,
                    message="非遗技艺更新失败"
                )
                
        except Exception as e:
            return IntangibleCulturalHeritageUploadResponse(
                success=False,
                message=f"更新失败：{str(e)}"
            )

    def delete_intangible_cultural_heritage(self, heritage_number: str) -> IntangibleCulturalHeritageDeleteResponse:
        """
        删除非遗技艺信息
        
        Args:
            heritage_number: 非遗编号
            
        Returns:
            删除响应
        """
        try:
            # 检查非遗技艺是否存在
            existing_heritage = self.heritage_repo.get_intangible_cultural_heritage_by_number(heritage_number)
            
            if not existing_heritage:
                return IntangibleCulturalHeritageDeleteResponse(
                    success=False,
                    message=f"非遗技艺不存在：{heritage_number}"
                )
            
            # 删除非遗技艺
            rows_affected = self.heritage_repo.delete_intangible_cultural_heritage(heritage_number)
            
            if rows_affected > 0:
                return IntangibleCulturalHeritageDeleteResponse(
                    success=True,
                    message="非遗技艺删除成功",
                    heritage_number=heritage_number
                )
            else:
                return IntangibleCulturalHeritageDeleteResponse(
                    success=False,
                    message="非遗技艺删除失败"
                )
                
        except Exception as e:
            return IntangibleCulturalHeritageDeleteResponse(
                success=False,
                message=f"删除失败：{str(e)}"
            )