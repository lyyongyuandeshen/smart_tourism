from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum


class PublishStatus(str, Enum):
    """发布状态枚举"""
    DRAFT = "draft"  # 草稿
    PUBLISHED = "published"  # 已发布
    UNPUBLISHED = "unpublished"  # 未发布


class IntangibleCulturalHeritageBase(BaseModel):
    """非遗技艺基础模型"""
    heritage_number: str = Field(description="非遗编号")
    heritage_name: str = Field(description="非遗名称")
    interactive_question_bank: str = Field(description="互动题库")
    video_url: str = Field(description="视频URL地址链接")
    is_published: bool = Field(default=False, description="是否发布")


class IntangibleCulturalHeritageCreate(BaseModel):
    """创建非遗技艺请求模型"""
    heritage_name: str = Field(description="非遗名称")
    interactive_question_bank: str = Field(description="互动题库")
    video_file: Optional[str] = Field(None, description="视频文件路径（用于上传）")


class IntangibleCulturalHeritageUpdate(BaseModel):
    """更新非遗技艺请求模型"""
    heritage_name: Optional[str] = Field(None, description="非遗名称")
    interactive_question_bank: Optional[str] = Field(None, description="互动题库")
    video_url: Optional[str] = Field(None, description="视频URL地址链接")
    is_published: Optional[bool] = Field(None, description="是否发布")


class IntangibleCulturalHeritageLimitedUpdate(BaseModel):
    """
    非遗技艺有限更新请求模型
    
    注意：此模型只允许更新非遗名称和发布状态，
    其他字段（互动题库、视频URL）不可修改
    """
    heritage_number: str = Field(description="非遗编号（必传）")
    heritage_name: Optional[str] = Field(None, description="非遗名称")
    is_published: Optional[bool] = Field(None, description="是否发布")


class IntangibleCulturalHeritageNameUpdate(BaseModel):
    """非遗技艺名称更新请求模型
    
    注意：此模型只允许更新非遗名称，其他字段不可修改
    """
    heritage_number: str = Field(description="非遗编号（必传）")
    heritage_name: str = Field(description="非遗名称（必传）")


class IntangibleCulturalHeritagePublishUpdate(BaseModel):
    """非遗技艺发布状态更新请求模型
    
    注意：此模型只允许将非遗技艺从未发布状态更新为发布状态
    """
    heritage_number: str = Field(description="非遗编号（必传）")
    is_published: bool = Field(description="是否发布（只能设置为True）")


class IntangibleCulturalHeritageResponse(IntangibleCulturalHeritageBase):
    """非遗技艺响应模型"""
    id: int = Field(description="主键ID")
    created_at: datetime = Field(description="创建时间")
    updated_at: datetime = Field(description="更新时间")

    class Config:
        from_attributes = True


class IntangibleCulturalHeritageQueryRequest(BaseModel):
    """非遗技艺查询请求模型"""
    heritage_number: Optional[str] = Field(None, description="非遗编号（精确查询）")
    heritage_name: Optional[str] = Field(None, description="非遗名称（模糊查询）")
    interactive_question_bank: Optional[str] = Field(None, description="互动题库")
    is_published: Optional[bool] = Field(None, description="是否发布")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")


class IntangibleCulturalHeritagePublishResponse(BaseModel):
    """非遗技艺发布响应模型"""
    success: bool
    message: str
    heritage_number: Optional[str] = None


class IntangibleCulturalHeritageListResponse(BaseModel):
    """非遗技艺列表响应模型"""
    success: bool
    message: str
    total: int = Field(description="总记录数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页数量")
    data: List[IntangibleCulturalHeritageResponse] = Field(description="非遗技艺列表")


class IntangibleCulturalHeritageUploadResponse(BaseModel):
    """非遗技艺上传响应模型"""
    success: bool
    message: str
    heritage_number: Optional[str] = None
    video_url: Optional[str] = None


class IntangibleCulturalHeritageDeleteResponse(BaseModel):
    """非遗技艺删除响应模型"""
    success: bool
    message: str
    heritage_number: Optional[str] = None


class VideoUploadRequest(BaseModel):
    """视频上传请求模型"""
    heritage_name: str = Field(description="非遗名称")
    interactive_question_bank: str = Field(description="互动题库")


class WatchVideoRequest(BaseModel):
    """观看视频请求模型"""
    video_url: str = Field(description="视频存储在后台的URL地址")


class WatchVideoResponse(BaseModel):
    """观看视频响应模型"""
    success: bool
    message: str
    original_url: str = Field(description="原始视频URL")
    pre_signed_url: str = Field(description="预签名播放链接")
    expires_at: Optional[str] = Field(None, description="预签名链接过期时间")
