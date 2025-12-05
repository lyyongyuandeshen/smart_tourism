from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from app.models.facility_models import (
    FacilityCreate,
    FacilityResponse,
    FacilityQueryRequest,
    FacilityListResponse,
    FacilityUploadResponse,
    FacilityDeleteResponse
)
from app.services.facility_service import FacilityService
from app.config.config import config

router = APIRouter()


def get_facility_service() -> FacilityService:
    """获取设备服务实例"""
    pool = config.get_mysql_pool()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库连接池未初始化"
        )
    return FacilityService(pool)


@router.get("/list", response_model=FacilityListResponse)
async def query_facilities(
    facility_id: Optional[str] = Query(None, description="设备编号（精确匹配）"),
    facility_name: Optional[str] = Query(None, description="设备名称（模糊匹配）"),
    category: Optional[str] = Query(None, description="设备分类"),
    status: Optional[str] = Query(None, description="设备状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    facility_service: FacilityService = Depends(get_facility_service)
):
    """
    查询设备列表
    
    支持以下查询方式：
    - 全量查询：不传任何参数，返回所有设备（分页）
    - 根据设备编号查询：传入facility_id参数
    - 根据设备名称查询：传入facility_name参数（支持模糊匹配）
    - 根据状态查询：传入status参数
    - 根据设备分类查询：传入category参数
    - 组合查询：可以同时传入多个参数
    
    Args:
        facility_id: 设备编号
        facility_name: 设备名称
        category: 设备分类
        status: 设备状态
        page: 页码
        page_size: 每页数量
        facility_service: 设备服务实例
        
    Returns:
        设备列表响应
    """
    try:
        request = FacilityQueryRequest(
            facility_id=facility_id,
            facility_name=facility_name,
            category=category,
            status=status,
            page=page,
            page_size=page_size
        )
        
        response = facility_service.query_facilities(request)
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/{facility_id}", response_model=FacilityResponse)
async def get_facility_detail(
    facility_id: str,
    facility_service: FacilityService = Depends(get_facility_service)
):
    """
    根据设备ID查询设备详情
    
    Args:
        facility_id: 设备ID
        facility_service: 设备服务实例
        
    Returns:
        设备详情
    """
    try:
        facility = facility_service.get_facility_by_id(facility_id)
        
        if not facility:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"设备不存在：{facility_id}"
            )
        
        return facility
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.post("/upload", response_model=FacilityUploadResponse)
async def upload_facility(
    facility: FacilityCreate,
    facility_service: FacilityService = Depends(get_facility_service)
):
    """
    上传设备信息到数据库
    
    如果设备ID已存在，则更新设备信息；否则创建新设备。
    
    Args:
        facility: 设备信息
        facility_service: 设备服务实例
        
    Returns:
        上传响应
    """
    try:
        response = facility_service.upload_facility(facility)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except ValueError as e:
        # Pydantic验证错误
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"数据验证失败：{str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传失败：{str(e)}"
        )


@router.delete("/{facility_id}", response_model=FacilityDeleteResponse)
async def delete_facility(
    facility_id: str,
    facility_service: FacilityService = Depends(get_facility_service)
):
    """
    删除设备信息
    
    Args:
        facility_id: 设备ID
        facility_service: 设备服务实例
        
    Returns:
        删除响应
    """
    try:
        response = facility_service.delete_facility(facility_id)
        
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
