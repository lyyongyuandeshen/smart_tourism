from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from datetime import date

from app.models.ticket_models import (
    TicketTimeSlotResponse,
    PurchaseTicketRequest,
    PurchaseTicketResponse
)
from app.services.ticket_service import TicketService
from app.config.config import ConfigManager, config

router = APIRouter()

# 全局配置管理器实例
# config = ConfigManager()


def get_ticket_service() -> TicketService:
    """获取票务服务实例"""
    pool = config.get_mysql_pool()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库连接池未初始化"
        )
    return TicketService(pool)


@router.get("/time-slots/{scenic_id}", response_model=List[TicketTimeSlotResponse])
async def get_available_time_slots(
        scenic_id: str,
        reservation_date: Optional[date] = Query(None, description="预约日期，格式：YYYY-MM-DD，为空则默认为当天日期"),
        ticket_service: TicketService = Depends(get_ticket_service)
):
    """
    根据景点ID查询指定日期的可用时段余票信息
    
    Args:
        scenic_id: 景点ID
        reservation_date: 预约日期，为空则默认为当天日期
        ticket_service: 票务服务实例
        
    Returns:
        时段余票列表
        
    Example:
        GET /api/v1/tickets/time-slots/scenic001?reservation_date=2025-11-28
        GET /api/v1/tickets/time-slots/scenic001  # 默认查询当天
    """
    try:
        time_slots = ticket_service.get_available_time_slots(scenic_id, reservation_date)
        return time_slots
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.post("/purchase", response_model=PurchaseTicketResponse)
async def purchase_ticket(
        request: PurchaseTicketRequest,
        ticket_service: TicketService = Depends(get_ticket_service)
):
    """
    购票接口
    
    Args:
        request: 购票请求参数
        ticket_service: 票务服务实例
        
    Returns:
        购票响应，包含订单号和电子票信息
    """
    try:
        response = ticket_service.purchase_ticket(request)

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
            detail=f"购票失败：{str(e)}"
        )
