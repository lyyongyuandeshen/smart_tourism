from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class Order(BaseModel):
    """订单模型"""
    id: str
    order_no: str
    user_id: str
    scenic_id: str
    scenic_name: str
    order_title: str
    order_price: Decimal
    ticket_quantity: int
    reschedule_limit: int = Field(description="改签次数上限")
    reschedule_used: int = Field(description="已使用改签次数")
    order_time: datetime = Field(description="下单时间")
    order_status: int = Field(description="订单状态：1-待支付，2-已支付，3-已取消，4-已完成，5-已退款")
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True
