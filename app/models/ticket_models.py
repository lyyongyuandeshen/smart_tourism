from datetime import date, datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from decimal import Decimal


class TicketTimeSlot(BaseModel):
    """票余量表（分预约时段）"""
    id: str
    ticket_id: str
    scenic_id: str
    reservation_date: date
    start_time: str
    end_time: str
    total_quota: int
    used_quota: int
    remaining_quota: int
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class TicketTimeSlotResponse(BaseModel):
    """时段余票响应模型"""
    id: str
    ticket_id: str
    scenic_id: str
    reservation_date: date
    start_time: str
    end_time: str
    total_quota: int
    used_quota: int
    remaining_quota: int


class ElectronicTicket(BaseModel):
    """票务凭证"""
    id: str
    order_id: str
    ticket_id: str
    qr_code_url: str
    verification_code: str
    valid_start_date: date
    valid_end_date: date
    verification_status: int = Field(description="核销状态：1-未核销，2-已核销，3-已过期")
    refund_status: int = Field(description="退款状态：1-未退款，2-退款中，3-已退款，4-退款失败")
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class TicketSales(BaseModel):
    """票务销售记录"""
    id: str
    order_no: str
    sales_channel: int = Field(description="销售渠道：1-官网，2-OTA平台，3-线下窗口，4-自助售票机")
    channel_name: str
    scenic_id: str
    scenic_name: str
    ticket_type: int = Field(description="票务类型：1-成人票，2-儿童票，3-老人票，4-联票")
    ticket_price: Decimal
    ticket_quantity: int
    total_amount: Decimal
    payment_status: int = Field(description="支付状态：1-已支付，2-未支付，3-已退款")
    payment_time: Optional[datetime] = None
    refund_amount: Optional[Decimal] = None
    refund_time: Optional[date] = None
    settlement_status: int = Field(description="分账状态：1-未分账，2-已分账，3-分账中")
    settlement_amount: Optional[Decimal] = None
    settlement_time: Optional[date] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class TouristInfo(BaseModel):
    """游客信息模型"""
    name: str = Field(description="游客姓名")
    phone: str = Field(description="游客电话")


class PurchaseTicketRequest(BaseModel):
    """购票请求模型"""
    user_id: str = Field(description="用户ID")
    scenic_id: str = Field(description="景点ID")
    scenic_name: str = Field(description="景点名称")
    order_title: str = Field(description="订单标题（票名）")
    tourists: List[TouristInfo] = Field(description="游客信息列表")
    ticket_date: date = Field(description="票日期")
    start_time: str = Field(description="票开始时间，格式：HH:MM")
    end_time: str = Field(description="票结束时间，格式：HH:MM")
    ticket_price: Decimal = Field(description="单张票价", gt=0)
    ticket_quantity: int = Field(description="票数量", ge=1)
    sales_channel: int = Field(default=1, description="销售渠道：1-官网，2-OTA平台，3-线下窗口，4-自助售票机")
    channel_name: str = Field(default="官网", description="渠道名称")


class PurchaseTicketResponse(BaseModel):
    """购票响应模型"""
    success: bool
    message: str
    order_no: Optional[str] = None
    electronic_tickets: Optional[list[dict]] = None
    total_amount: Optional[Decimal] = None
