from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class CulturalHeritageBase(BaseModel):
    """文化遗产基础模型"""
    file_id: str = Field(description="文件编号")
    file_name: str = Field(description="文件名称")
    file_type: str = Field(description="文件类型：文件、图片、视频")
    tag: str = Field(description="所属标签（如'非遗'、'古建'、'民俗'、'文献'）")
    url: str = Field(description="文件存储链接URL")


class CulturalHeritageCreate(CulturalHeritageBase):
    """创建文化遗产请求模型"""
    pass


class CulturalHeritageResponse(CulturalHeritageBase):
    """文化遗产响应模型"""
    created_at: datetime = Field(description="上传时间")
    updated_at: datetime = Field(description="更新时间")

    class Config:
        from_attributes = True


class CulturalHeritageQueryRequest(BaseModel):
    """文化遗产查询请求模型"""
    file_id: Optional[str] = Field(None, description="文件编号")
    file_name: Optional[str] = Field(None, description="文件名称（模糊查询）")
    file_type: Optional[str] = Field(None, description="文件类型")
    tag: Optional[str] = Field(None, description="所属标签")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")


class CulturalHeritageListResponse(BaseModel):
    """文化遗产列表响应模型"""
    success: bool
    message: str
    total: int = Field(description="总记录数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页数量")
    data: list[CulturalHeritageResponse] = Field(description="文化遗产列表")


class CulturalHeritageUploadResponse(BaseModel):
    """文化遗产上传响应模型"""
    success: bool
    message: str
    file_id: Optional[str] = None


class CulturalHeritageDeleteResponse(BaseModel):
    """文化遗产删除响应模型"""
    success: bool
    message: str
    file_id: Optional[str] = None
