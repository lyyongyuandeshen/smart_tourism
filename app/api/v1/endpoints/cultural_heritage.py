from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from app.models.cultural_heritage_models import (
    CulturalHeritageCreate,
    CulturalHeritageResponse,
    CulturalHeritageQueryRequest,
    CulturalHeritageListResponse,
    CulturalHeritageUploadResponse,
    CulturalHeritageDeleteResponse
)
from app.services.cultural_heritage_service import CulturalHeritageService
from app.config.config import config

router = APIRouter()


def get_cultural_heritage_service() -> CulturalHeritageService:
    """获取文化遗产服务实例"""
    pool = config.get_mysql_pool()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库连接池未初始化"
        )
    return CulturalHeritageService(pool)


@router.get("/list", response_model=CulturalHeritageListResponse)
async def query_cultural_heritages(
    file_id: Optional[str] = Query(None, description="文件编号（精确匹配）"),
    file_name: Optional[str] = Query(None, description="文件名称（模糊匹配）"),
    file_type: Optional[str] = Query(None, description="文件类型"),
    tag: Optional[str] = Query(None, description="所属标签"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    heritage_service: CulturalHeritageService = Depends(get_cultural_heritage_service)
):
    """
    查询文化遗产列表
    
    支持以下查询方式：
    - 全量查询：不传任何参数，返回所有文化遗产（分页）
    - 根据文件编号查询：传入file_id参数
    - 根据文件名称查询：传入file_name参数（支持模糊匹配）
    - 根据文件类型查询：传入file_type参数（文件、图片、视频）
    - 根据标签查询：传入tag参数（非遗、古建、民俗、文献）
    - 组合查询：可以同时传入多个参数
    
    Args:
        file_id: 文件编号
        file_name: 文件名称
        file_type: 文件类型
        tag: 所属标签
        page: 页码
        page_size: 每页数量
        heritage_service: 文化遗产服务实例
        
    Returns:
        文化遗产列表响应
    """
    try:
        request = CulturalHeritageQueryRequest(
            file_id=file_id,
            file_name=file_name,
            file_type=file_type,
            tag=tag,
            page=page,
            page_size=page_size
        )
        
        response = heritage_service.query_cultural_heritages(request)
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/{file_id}", response_model=CulturalHeritageResponse)
async def get_cultural_heritage_detail(
    file_id: str,
    heritage_service: CulturalHeritageService = Depends(get_cultural_heritage_service)
):
    """
    根据文件ID查询文化遗产详情
    
    Args:
        file_id: 文件ID
        heritage_service: 文化遗产服务实例
        
    Returns:
        文化遗产详情
    """
    try:
        heritage = heritage_service.get_cultural_heritage_by_id(file_id)
        
        if not heritage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"文化遗产不存在：{file_id}"
            )
        
        return heritage
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.post("/upload", response_model=CulturalHeritageUploadResponse)
async def upload_cultural_heritage(
    heritage: CulturalHeritageCreate,
    heritage_service: CulturalHeritageService = Depends(get_cultural_heritage_service)
):
    """
    上传文化遗产信息到数据库
    
    如果文件ID已存在，则更新文化遗产信息；否则创建新文化遗产。
    
    Args:
        heritage: 文化遗产信息
        heritage_service: 文化遗产服务实例
        
    Returns:
        上传响应
    """
    try:
        response = heritage_service.upload_cultural_heritage(heritage)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传失败：{str(e)}"
        )


@router.delete("/{file_id}", response_model=CulturalHeritageDeleteResponse)
async def delete_cultural_heritage(
    file_id: str,
    heritage_service: CulturalHeritageService = Depends(get_cultural_heritage_service)
):
    """
    删除文化遗产信息
    
    Args:
        file_id: 文件ID
        heritage_service: 文化遗产服务实例
        
    Returns:
        删除响应
    """
    try:
        response = heritage_service.delete_cultural_heritage(file_id)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND if "不存在" in response.message else status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败：{str(e)}"
        )
