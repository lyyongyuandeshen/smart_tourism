from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from decimal import Decimal


class MemberLevelBase(BaseModel):
    """会员等级基础模型"""
    level: int = Field(..., ge=1, description="会员等级")
    level_name: str = Field(..., min_length=1, max_length=64, description="等级名称")
    points_min: int = Field(..., ge=0, description="所需积分下限")
    points_max: int = Field(..., ge=0, description="所需积分上限")
    discount_rate: Decimal = Field(..., ge=0, le=100, description="专属折扣（百分比，如95.00表示95折）")
    priority_booking: bool = Field(False, description="优先预约权限")


class MemberLevelCreate(MemberLevelBase):
    """创建会员等级请求模型"""
    pass


class MemberLevelUpdate(BaseModel):
    """更新会员等级请求模型"""
    level_name: Optional[str] = Field(None, min_length=1, max_length=64, description="等级名称")
    points_min: Optional[int] = Field(None, ge=0, description="所需积分下限")
    points_max: Optional[int] = Field(None, gt=0, description="所需积分上限")
    discount_rate: Optional[Decimal] = Field(None, ge=0, le=100, description="专属折扣（百分比）")
    priority_booking: Optional[bool] = Field(None, description="优先预约权限")


class MemberLevelResponse(MemberLevelBase):
    """会员等级响应模型"""
    id: int
    is_deleted: int = Field(0, description="是否删除（0-未删除，1-已删除）")
    create_time: datetime
    update_time: datetime

    class Config:
        from_attributes = True


class MemberLevelQueryRequest(BaseModel):
    """会员等级查询请求模型"""
    level: Optional[int] = Field(None, ge=1, le=10, description="会员等级")
    keyword: Optional[str] = Field(None, description="关键词（等级名称模糊匹配）")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")


class MemberLevelListResponse(BaseModel):
    """会员等级列表响应模型"""
    success: bool
    message: str
    total: int = 0
    page: int = 1
    page_size: int = 10
    data: List[MemberLevelResponse] = []


class MemberLevelOperationResponse(BaseModel):
    """会员等级操作响应模型（创建/更新/删除）"""
    success: bool
    message: str
    level_id: Optional[str] = None
