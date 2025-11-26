from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from decimal import Decimal


class FacilityBase(BaseModel):
    """景区设备基础模型"""
    facility_id: str = Field(description="设备唯一编号")
    facility_name: str = Field(description="设备名称")
    category: str = Field(description="分类：洗手间、儿童乐园、休息区、轮椅通道、互动体验、便民点、避难点、风景名胜、紧急出口")
    icon: Optional[str] = Field(None, description="图标URL或图标类名")
    position_desc: str = Field(description="位置描述")
    longitude: Optional[Decimal] = Field(None, description="经度")
    latitude: Optional[Decimal] = Field(None, description="纬度")
    status: str = Field(description="状态：正常、维修、暂停、已拆除")


class FacilityCreate(FacilityBase):
    """创建设备请求模型"""
    pass


class FacilityResponse(FacilityBase):
    """设备响应模型"""
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="最后更新时间")

    class Config:
        from_attributes = True


class FacilityQueryRequest(BaseModel):
    """设备查询请求模型"""
    facility_id: Optional[str] = Field(None, description="设备编号")
    facility_name: Optional[str] = Field(None, description="设备名称（模糊查询）")
    category: Optional[str] = Field(None, description="设备分类")
    status: Optional[str] = Field(None, description="设备状态")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")


class FacilityListResponse(BaseModel):
    """设备列表响应模型"""
    success: bool
    message: str
    total: int = Field(description="总记录数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页数量")
    data: list[FacilityResponse] = Field(description="设备列表")


class FacilityUploadResponse(BaseModel):
    """设备上传响应模型"""
    success: bool
    message: str
    facility_id: Optional[str] = None
