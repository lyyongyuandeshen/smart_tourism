from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ScenicGuide(BaseModel):
    """景点导览数据库模型"""
    id: str
    scenic_id: str
    guide_title: str
    historical_background: Optional[str] = None
    cultural_value: Optional[str] = None
    architectural_features: Optional[str] = None
    historical_stories: Optional[str] = None
    ecological_science: Optional[str] = None
    open_status: int = Field(description="开放状态：0-关闭，1-开放")
    last_bus_time: Optional[str] = None
    evacuation_route_url: Optional[str] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None

    class Config:
        from_attributes = True


class ScenicGuideCreateRequest(BaseModel):
    """创建景点导览请求模型"""
    scenic_id: str = Field(description="景点ID")
    guide_title: str = Field(description="导览标题")
    historical_background: Optional[str] = Field(default=None, description="历史背景")
    cultural_value: Optional[str] = Field(default=None, description="文化价值")
    architectural_features: Optional[str] = Field(default=None, description="建筑特色")
    historical_stories: Optional[str] = Field(default=None, description="历史故事")
    ecological_science: Optional[str] = Field(default=None, description="生态科普")
    open_status: int = Field(default=1, description="开放状态：0-关闭，1-开放")
    last_bus_time: Optional[str] = Field(default=None, description="末班车时间")
    evacuation_route_url: Optional[str] = Field(default=None, description="应急疏散路线URL")


class ScenicGuideUpdateRequest(BaseModel):
    """更新景点导览请求模型"""
    guide_title: Optional[str] = Field(default=None, description="导览标题")
    historical_background: Optional[str] = Field(default=None, description="历史背景")
    cultural_value: Optional[str] = Field(default=None, description="文化价值")
    architectural_features: Optional[str] = Field(default=None, description="建筑特色")
    historical_stories: Optional[str] = Field(default=None, description="历史故事")
    ecological_science: Optional[str] = Field(default=None, description="生态科普")
    open_status: Optional[int] = Field(default=None, description="开放状态：0-关闭，1-开放")
    last_bus_time: Optional[str] = Field(default=None, description="末班车时间")
    evacuation_route_url: Optional[str] = Field(default=None, description="应急疏散路线URL")


class ScenicGuideResponse(BaseModel):
    """景点导览响应模型"""
    id: str
    scenic_id: str
    guide_title: str
    historical_background: Optional[str] = None
    cultural_value: Optional[str] = None
    architectural_features: Optional[str] = None
    historical_stories: Optional[str] = None
    ecological_science: Optional[str] = None
    open_status: int
    last_bus_time: Optional[str] = None
    evacuation_route_url: Optional[str] = None
    create_time: Optional[datetime] = None
    update_time: Optional[datetime] = None


class TimeSlotCreateRequest(BaseModel):
    """创建时段请求模型"""
    ticket_id: str = Field(description="票务ID")
    scenic_id: str = Field(description="景点ID")
    reservation_date: str = Field(description="预约日期，格式：YYYY-MM-DD")
    start_time: str = Field(description="开始时间，格式：HH:MM")
    end_time: str = Field(description="结束时间，格式：HH:MM")
    total_quota: int = Field(description="总配额", ge=0)


class TimeSlotUpdateRequest(BaseModel):
    """更新时段请求模型"""
    total_quota: Optional[int] = Field(default=None, description="总配额", ge=0)
    used_quota: Optional[int] = Field(default=None, description="已用配额", ge=0)
    remaining_quota: Optional[int] = Field(default=None, description="剩余配额", ge=0)


class TimeSlotBatchCreateRequest(BaseModel):
    """批量创建时段请求模型"""
    ticket_id: str = Field(description="票务ID")
    scenic_id: str = Field(description="景点ID")
    reservation_dates: list[str] = Field(description="预约日期列表，格式：YYYY-MM-DD")
    time_slots: list[dict] = Field(description="时段列表，每个时段包含start_time、end_time、total_quota")
    
    class Config:
        json_schema_extra = {
            "example": {
                "ticket_id": "ticket-001",
                "scenic_id": "scenic-001",
                "reservation_dates": ["2025-11-26", "2025-11-27"],
                "time_slots": [
                    {"start_time": "09:00", "end_time": "11:00", "total_quota": 100},
                    {"start_time": "14:00", "end_time": "16:00", "total_quota": 100}
                ]
            }
        }


class CommonResponse(BaseModel):
    """通用响应模型"""
    success: bool
    message: str
    data: Optional[dict] = None
