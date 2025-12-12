from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File, Form
from typing import Optional
import logging

from app.models.intangible_cultural_heritage_models import (
    IntangibleCulturalHeritageCreate,
    IntangibleCulturalHeritageResponse,
    IntangibleCulturalHeritageListResponse,
    IntangibleCulturalHeritageUploadResponse,
    IntangibleCulturalHeritageDeleteResponse,
    IntangibleCulturalHeritageNameUpdate,
    IntangibleCulturalHeritagePublishUpdate,
    WatchVideoRequest,
    WatchVideoResponse, IntangibleCulturalHeritagePublishResponse
)
from app.services.intangible_cultural_heritage_service import IntangibleCulturalHeritageService
from app.services.tos_service import TosService
from app.config.config import config

logger = logging.getLogger(__name__)

router = APIRouter()


def get_intangible_cultural_heritage_service() -> IntangibleCulturalHeritageService:
    """获取非遗技艺服务实例"""
    pool = config.get_mysql_pool()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库连接池未初始化"
        )
    
    tos_service = config.get_tos_service()
    if not tos_service:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="TOS服务未初始化"
        )
    
    return IntangibleCulturalHeritageService(pool, tos_service)


def get_tos_service() -> TosService:
    """获取TOS服务实例"""
    tos_service = config.get_tos_service()
    if not tos_service:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="TOS服务未初始化"
        )
    return tos_service


@router.get("/list", response_model=IntangibleCulturalHeritageListResponse, summary="查询全量非遗技艺列表")
async def get_all_intangible_cultural_heritages(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    heritage_service: IntangibleCulturalHeritageService = Depends(get_intangible_cultural_heritage_service)
):
    """
    查询全量非遗技艺列表
    
    返回所有非遗技艺记录，支持分页查询
    
    Args:
        page: 页码
        page_size: 每页数量
        heritage_service: 非遗技艺服务实例
        
    Returns:
        非遗技艺列表响应
    """
    try:
        response = heritage_service.get_all_heritages(page=page, page_size=page_size)
        return response
        
    except Exception as e:
        logger.error(f"查询全量非遗技艺列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/published", response_model=IntangibleCulturalHeritageListResponse, summary="获取已发布的非遗视频全量信息")
async def get_published_intangible_cultural_heritages(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    heritage_service: IntangibleCulturalHeritageService = Depends(get_intangible_cultural_heritage_service)
):
    """
    获取已发布的非遗视频全量信息
    
    返回所有已发布的非遗技艺记录，支持分页查询
    
    Args:
        page: 页码
        page_size: 每页数量
        heritage_service: 非遗技艺服务实例
        
    Returns:
        已发布的非遗技艺列表响应
    """
    try:
        response = heritage_service.get_published_heritages(page=page, page_size=page_size)
        return response
        
    except Exception as e:
        logger.error(f"获取已发布的非遗视频列表失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/search", response_model=IntangibleCulturalHeritageListResponse, summary="根据非遗名称模糊搜索")
async def search_intangible_cultural_heritages_by_name(
    heritage_name: str = Query(..., description="非遗名称（模糊匹配）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    heritage_service: IntangibleCulturalHeritageService = Depends(get_intangible_cultural_heritage_service)
):
    """
    根据非遗名称模糊搜索非遗技艺
    
    支持按非遗名称进行模糊匹配查询
    
    Args:
        heritage_name: 非遗名称（模糊匹配）
        page: 页码
        page_size: 每页数量
        heritage_service: 非遗技艺服务实例
        
    Returns:
        非遗技艺列表响应
    """
    try:
        response = heritage_service.search_by_heritage_name(
            heritage_name=heritage_name,
            page=page,
            page_size=page_size
        )
        return response
        
    except Exception as e:
        logger.error(f"搜索非遗技艺失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"搜索失败：{str(e)}"
        )


@router.post("/create", response_model=IntangibleCulturalHeritageUploadResponse, summary="新增非遗技艺")
async def create_intangible_cultural_heritage(
    heritage_name: str = Form(..., description="非遗名称"),
    interactive_question_bank: str = Form(..., description="互动题库"),
    video_file: UploadFile = File(..., description="非遗技艺教学视频"),
    heritage_service: IntangibleCulturalHeritageService = Depends(get_intangible_cultural_heritage_service)
):
    """
    新增非遗技艺记录
    
    该接口将：
    1. 将上传的视频文件通过TOS服务上传到对象存储
    2. 生成非遗编号
    3. 将非遗信息保存到数据库
    
    Args:
        heritage_name: 非遗名称
        interactive_question_bank: 互动题库
        video_file: 非遗技艺教学视频文件
        heritage_service: 非遗技艺服务实例
        
    Returns:
        新增响应
    """
    try:
        # 验证视频文件类型
        if not video_file.filename or not video_file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm')):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="仅支持视频文件格式：mp4, avi, mov, wmv, flv, mkv, webm"
            )
        
        # 构建创建请求
        heritage_data = IntangibleCulturalHeritageCreate(
            heritage_name=heritage_name,
            interactive_question_bank=interactive_question_bank
        )
        
        # 调用服务层创建非遗技艺
        response = await heritage_service.upload_video_and_create_heritage(
            heritage_data=heritage_data,
            video_file=video_file
        )
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"新增非遗技艺失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"新增失败：{str(e)}"
        )


@router.get("/{heritage_number}", response_model=IntangibleCulturalHeritageResponse, summary="根据非遗编号查询详情")
async def get_intangible_cultural_heritage_detail(
    heritage_number: str,
    heritage_service: IntangibleCulturalHeritageService = Depends(get_intangible_cultural_heritage_service)
):
    """
    根据非遗编号查询非遗技艺详情
    
    Args:
        heritage_number: 非遗编号
        heritage_service: 非遗技艺服务实例
        
    Returns:
        非遗技艺详情
    """
    try:
        heritage = heritage_service.get_intangible_cultural_heritage_by_number(heritage_number)
        
        if not heritage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"非遗技艺不存在：{heritage_number}"
            )
        
        return heritage
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"查询非遗技艺详情失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.put("/{heritage_number}/name", response_model=IntangibleCulturalHeritageUploadResponse, summary="更新非遗技艺名称")
async def update_intangible_cultural_heritage_name(
    heritage_number: str,
    heritage_name: str = Form(..., description="非遗名称（必传）"),
    heritage_service: IntangibleCulturalHeritageService = Depends(get_intangible_cultural_heritage_service)
):
    """
    更新非遗技艺名称
    
    注意：此接口仅允许修改非遗名称，其他字段不可修改
    
    Args:
        heritage_number: 非遗编号（必传）
        heritage_name: 非遗名称（必传）
        heritage_service: 非遗技艺服务实例
        
    Returns:
        更新响应
    """
    try:
        # 构建更新数据，只包含名称字段
        update_data = IntangibleCulturalHeritageNameUpdate(
            heritage_number=heritage_number,
            heritage_name=heritage_name
        )

        response = heritage_service.update_intangible_cultural_heritage_name(update_data)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"更新非遗技艺名称失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新失败：{str(e)}"
        )


@router.put("/{heritage_number}/publish", response_model=IntangibleCulturalHeritagePublishResponse, summary="发布非遗技艺")
async def publish_intangible_cultural_heritage(
    heritage_number: str,
    is_published: bool = Form(True, description="是否发布（只能设置为True）"),
    heritage_service: IntangibleCulturalHeritageService = Depends(get_intangible_cultural_heritage_service)
):
    """
    发布非遗技艺
    
    注意：此接口只能将非遗技艺从未发布状态更新为发布状态
    
    Args:
        heritage_number: 非遗编号（必传）
        is_published: 是否发布（只能设置为True）
        heritage_service: 非遗技艺服务实例
        
    Returns:
        发布响应
    """
    try:
        # 验证只能设置为发布状态
        if not is_published:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="发布接口只能将非遗技艺设置为发布状态"
            )
        
        # 构建更新数据，只包含发布状态字段
        update_data = IntangibleCulturalHeritagePublishUpdate(
            heritage_number=heritage_number,
            is_published=is_published
        )

        response = heritage_service.update_intangible_cultural_heritage_publish(update_data)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"发布非遗技艺失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"发布失败：{str(e)}"
        )


@router.delete("/{heritage_number}", response_model=IntangibleCulturalHeritageDeleteResponse, summary="删除非遗技艺")
async def delete_intangible_cultural_heritage(
    heritage_number: str,
    heritage_service: IntangibleCulturalHeritageService = Depends(get_intangible_cultural_heritage_service)
):
    """
    删除非遗技艺信息
    
    Args:
        heritage_number: 非遗编号
        heritage_service: 非遗技艺服务实例
        
    Returns:
        删除响应
    """
    try:
        response = heritage_service.delete_intangible_cultural_heritage(heritage_number)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除非遗技艺失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败：{str(e)}"
        )


@router.post("/watch", response_model=WatchVideoResponse, summary="获取视频预签名播放链接")
async def watch_intangible_cultural_heritage_video(
    request: WatchVideoRequest,
    tos_service: TosService = Depends(get_tos_service)
):
    """
    获取非遗技艺教学视频的预签名播放链接
    
    该接口接受视频存储在后台的URL，通过TOS服务生成预签名播放链接
    
    Args:
        request: 观看视频请求，包含视频URL
        tos_service: TOS服务实例
        
    Returns:
        预签名播放链接响应
    """
    try:
        # 从请求中获取视频URL
        video_url = request.video_url
        # 调用TOS服务获取预签名URL
        pre_signed_url = await tos_service.get_pre_signed_url(video_url)
        
        # 构建响应数据
        return WatchVideoResponse(
            success=True,
            message="预签名播放链接获取成功",
            original_url=video_url,
            pre_signed_url=pre_signed_url,
            expires_at="1小时后过期"  # TOS服务默认1小时过期
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"获取预签名播放链接失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取播放链接失败：{str(e)}"
        )