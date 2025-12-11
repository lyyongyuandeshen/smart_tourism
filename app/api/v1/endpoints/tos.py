from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from typing import List, Optional
import logging

from app.services.tos_service import TosService
from app.models.tos_models import (
    UploadFileResponse, UploadFileData, BatchUploadResponse, BatchUploadData,
    DeleteFileRequest, DeleteFileResponse, FileInfoRequest, FileInfoResponse, FileInfo, GetPreViewResponse,
    GetPreViewRequest, PreViewData
)
from app.config.config import config

logger = logging.getLogger(__name__)

router = APIRouter()


# 获取TOS服务实例
def get_tos_service() -> TosService:
    """获取TOS服务实例"""
    return config.get_tos_service()


@router.post("/upload", response_model=UploadFileResponse, summary="上传单个文件")
async def upload_file(
        file: UploadFile = File(..., description="要上传的文件"),
        # file_type: str = Form(..., description="文件类型：image 或 video"),
        custom_path: Optional[str] = Form(None, description="自定义存储路径"),
        generate_thumbnail: bool = Form(False, description="是否生成缩略图（仅图片）"),
        tos_service: TosService = Depends(get_tos_service)
):
    """
    上传单个文件到TOS
    
    支持的图片格式：jpg, jpeg, png, gif, bmp, webp
    支持的视频格式：mp4, avi, mov, wmv, flv, mkv, webm
    
    Args:
        file: 要上传的文件
        file_type: 文件类型（image 或 video）
        custom_path: 自定义存储路径（可选）
        generate_thumbnail: 是否生成缩略图，仅对图片有效
        
    Returns:
        UploadFileResponse: 上传结果
    """
    try:
        upload_data = await tos_service.upload_file(
            file=file,
            # file_type=file_type,
            custom_path=custom_path,
            generate_thumbnail=generate_thumbnail
        )

        return UploadFileResponse(
            success=True,
            message="文件上传成功",
            data=upload_data
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"上传文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"上传文件失败: {str(e)}")


@router.post("/get_pre_signed_url", response_model=GetPreViewResponse, summary="获取预签名URL")
async def get_pre_signed_url(
        file_paths: List[GetPreViewRequest],
        tos_service: TosService = Depends(get_tos_service)
):
    """获取预签名URL"""
    try:
        pre_signed_urls = []
        for file_path in file_paths:
            url = await tos_service.get_pre_signed_url(file_path.file_path)
            # 创建PreViewData对象，符合模型要求
            preview_data = PreViewData(key=file_path.file_path, url=url)
            pre_signed_urls.append(preview_data)

        return GetPreViewResponse(
            success=True,
            message="预签名URL获取成功",
            data=pre_signed_urls
        )
    except Exception as e:
        logger.error(f"获取预签名URL失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取预签名URL失败: {str(e)}")


@router.post("/batch-upload", response_model=BatchUploadResponse, summary="批量上传文件")
async def batch_upload_files(
        files: List[UploadFile] = File(..., description="要上传的文件列表"),
        file_type: str = Form(..., description="文件类型：image 或 video"),
        custom_path: Optional[str] = Form(None, description="自定义存储路径"),
        generate_thumbnail: bool = Form(False, description="是否生成缩略图（仅图片）"),
        tos_service: TosService = Depends(get_tos_service)
):
    """
    批量上传文件到TOS
    
    Args:
        files: 要上传的文件列表
        file_type: 文件类型（image 或 video）
        custom_path: 自定义存储路径（可选）
        generate_thumbnail: 是否生成缩略图，仅对图片有效
        
    Returns:
        BatchUploadResponse: 批量上传结果
    """
    try:
        if not files:
            raise HTTPException(status_code=400, detail="请选择要上传的文件")

        batch_data = await tos_service.batch_upload_files(
            files=files,
            file_type=file_type,
            custom_path=custom_path,
            generate_thumbnail=generate_thumbnail
        )

        return BatchUploadResponse(
            success=True,
            message=f"批量上传完成，成功: {batch_data.success_count}，失败: {batch_data.failed_count}",
            data=batch_data
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"批量上传文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"批量上传文件失败: {str(e)}")


@router.delete("/delete", response_model=DeleteFileResponse, summary="删除文件")
async def delete_file(
        request: DeleteFileRequest,
        tos_service: TosService = Depends(get_tos_service)
):
    """
    删除TOS中的文件
    
    Args:
        request: 删除文件请求，包含文件路径
        
    Returns:
        DeleteFileResponse: 删除结果
    """
    try:
        success = tos_service.delete_file(request.file_path)

        if success:
            return DeleteFileResponse(
                success=True,
                message="文件删除成功"
            )
        else:
            return DeleteFileResponse(
                success=False,
                message="文件删除失败"
            )
    except Exception as e:
        logger.error(f"删除文件失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"删除文件失败: {str(e)}")


@router.post("/file-info", response_model=FileInfoResponse, summary="获取文件信息")
async def get_file_info(
        request: FileInfoRequest,
        tos_service: TosService = Depends(get_tos_service)
):
    """
    获取TOS中文件的详细信息
    
    Args:
        request: 获取文件信息请求，包含文件路径
        
    Returns:
        FileInfoResponse: 文件信息
    """
    try:
        file_info = tos_service.get_file_info(request.file_path)

        if file_info:
            return FileInfoResponse(
                success=True,
                message="获取文件信息成功",
                data=file_info
            )
        else:
            return FileInfoResponse(
                success=False,
                message="文件不存在或获取信息失败"
            )
    except Exception as e:
        logger.error(f"获取文件信息失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"获取文件信息失败: {str(e)}")


@router.get("/file-exists/{file_path:path}", summary="检查文件是否存在")
async def check_file_exists(
        file_path: str,
        tos_service: TosService = Depends(get_tos_service)
):
    """
    检查文件是否存在于TOS中
    
    Args:
        file_path: 文件路径
        
    Returns:
        dict: 检查结果
    """
    try:
        exists = tos_service.file_exists(file_path)

        return {
            "success": True,
            "message": "检查完成",
            "data": {
                "file_path": file_path,
                "exists": exists
            }
        }
    except Exception as e:
        logger.error(f"检查文件是否存在失败: {str(e)}")
        raise HTTPException(status_code=500, detail=f"检查文件是否存在失败: {str(e)}")
