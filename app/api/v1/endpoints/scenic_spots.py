from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional

from app.config.config import ConfigManager
from app.models.scenic_models import (
    ScenicGuideCreateRequest,
    ScenicGuideUpdateRequest,
    ScenicGuideResponse,
    TimeSlotCreateRequest,
    TimeSlotUpdateRequest,
    TimeSlotBatchCreateRequest,
    CommonResponse
)
from app.models.ticket_models import TicketTimeSlotResponse
from app.services.scenic_service import ScenicService
from app.config.config import config

router = APIRouter()

def get_scenic_service() -> ScenicService:
    """获取景点服务实例"""
    pool = config.get_mysql_pool()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库连接池未初始化"
        )
    return ScenicService(pool)


# ========== 景点导览相关接口 ==========

@router.post("/guides", response_model=CommonResponse, status_code=status.HTTP_201_CREATED)
async def create_scenic_guide(
        request: ScenicGuideCreateRequest,
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    创建景点导览
    
    Args:
        request: 创建请求参数
        scenic_service: 景点服务实例
        
    Returns:
        创建结果
    """
    response = scenic_service.create_scenic_guide(request)
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.message
        )
    return response


@router.get("/guides/{guide_id}", response_model=ScenicGuideResponse)
async def get_scenic_guide(
        guide_id: str,
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    根据ID查询景点导览
    
    Args:
        guide_id: 导览ID
        scenic_service: 景点服务实例
        
    Returns:
        景点导览信息
    """
    guide = scenic_service.get_scenic_guide(guide_id)
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="景点导览不存在"
        )
    return guide


@router.get("/guides/scenic/{scenic_id}", response_model=ScenicGuideResponse)
async def get_scenic_guide_by_scenic_id(
        scenic_id: str,
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    根据景点ID查询景点导览
    
    Args:
        scenic_id: 景点ID
        scenic_service: 景点服务实例
        
    Returns:
        景点导览信息
    """
    guide = scenic_service.get_scenic_guide_by_scenic_id(scenic_id)
    if not guide:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="景点导览不存在"
        )
    return guide


@router.get("/guides", response_model=List[ScenicGuideResponse])
async def get_all_scenic_guides(
        open_status: Optional[int] = Query(None, description="开放状态：0-关闭，1-开放"),
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    根据open_status开放状态查询所有景点导览，open_status为空时查询所有
    
    Args:
        open_status: 开放状态筛选（可选）
        scenic_service: 景点服务实例
        
    Returns:
        景点导览列表
    """
    guides = scenic_service.get_all_scenic_guides(open_status)
    return guides


@router.put("/guides/{guide_id}", response_model=CommonResponse)
async def update_scenic_guide(
        guide_id: str,
        request: ScenicGuideUpdateRequest,
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    更新景点导览
    
    Args:
        guide_id: 导览ID
        request: 更新请求参数
        scenic_service: 景点服务实例
        
    Returns:
        更新结果
    """
    response = scenic_service.update_scenic_guide(guide_id, request)
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.message
        )
    return response


@router.delete("/guides/{guide_id}", response_model=CommonResponse)
async def delete_scenic_guide(
        guide_id: str,
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    删除景点导览
    
    Args:
        guide_id: 导览ID
        scenic_service: 景点服务实例
        
    Returns:
        删除结果
    """
    response = scenic_service.delete_scenic_guide(guide_id)
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.message
        )
    return response


# ========== 时段管理相关接口 ==========

@router.post("/time-slots", response_model=CommonResponse, status_code=status.HTTP_201_CREATED)
async def create_time_slot(
        request: TimeSlotCreateRequest,
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    创建时段
    
    Args:
        request: 创建请求参数
        scenic_service: 景点服务实例
        
    Returns:
        创建结果
    """
    response = scenic_service.create_time_slot(request)
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.message
        )
    return response


@router.post("/time-slots/batch", response_model=CommonResponse, status_code=status.HTTP_201_CREATED)
async def batch_create_time_slots(
        request: TimeSlotBatchCreateRequest,
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    批量创建时段
    
    Args:
        request: 批量创建请求参数
        scenic_service: 景点服务实例
        
    Returns:
        创建结果
    """
    response = scenic_service.batch_create_time_slots(request)
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.message
        )
    return response


@router.get("/time-slots/scenic/{scenic_id}", response_model=List[TicketTimeSlotResponse])
async def get_time_slots_by_scenic(
        scenic_id: str,
        start_date: Optional[str] = Query(None, description="开始日期，格式：YYYY-MM-DD"),
        end_date: Optional[str] = Query(None, description="结束日期，格式：YYYY-MM-DD"),
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    根据景点ID查询时段
    
    Args:
        scenic_id: 景点ID
        start_date: 开始日期（可选）
        end_date: 结束日期（可选）
        scenic_service: 景点服务实例
        
    Returns:
        时段列表
    """
    slots = scenic_service.get_time_slots_by_scenic(scenic_id, start_date, end_date)
    return slots


@router.put("/time-slots/{slot_id}", response_model=CommonResponse)
async def update_time_slot(
        slot_id: str,
        request: TimeSlotUpdateRequest,
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    更新时段
    
    Args:
        slot_id: 时段ID
        request: 更新请求参数
        scenic_service: 景点服务实例
        
    Returns:
        更新结果
    """
    response = scenic_service.update_time_slot(slot_id, request)
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.message
        )
    return response


@router.delete("/time-slots/{slot_id}", response_model=CommonResponse)
async def delete_time_slot(
        slot_id: str,
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    删除时段
    
    Args:
        slot_id: 时段ID
        scenic_service: 景点服务实例
        
    Returns:
        删除结果
    """
    response = scenic_service.delete_time_slot(slot_id)
    if not response.success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=response.message
        )
    return response


@router.delete("/time-slots/scenic/{scenic_id}", response_model=CommonResponse)
async def delete_time_slots_by_scenic(
        scenic_id: str,
        scenic_service: ScenicService = Depends(get_scenic_service)
):
    """
    删除景点的所有时段
    
    Args:
        scenic_id: 景点ID
        scenic_service: 景点服务实例
        
    Returns:
        删除结果
    """
    response = scenic_service.delete_time_slots_by_scenic(scenic_id)
    return response
