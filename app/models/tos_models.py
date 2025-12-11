from typing import Optional, List
from pydantic import BaseModel, Field
from datetime import datetime


class UploadFileRequest(BaseModel):
    """文件上传请求模型"""
    file_type: str = Field(..., description="文件类型：image 或 video")
    custom_path: Optional[str] = Field(None, description="自定义存储路径")
    generate_thumbnail: Optional[bool] = Field(False, description="是否生成缩略图（仅图片）")


class UploadFileResponse(BaseModel):
    """文件上传响应模型"""
    success: bool = Field(..., description="上传是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional['UploadFileData'] = Field(None, description="上传结果数据")


class GetPreViewResponse(BaseModel):
    """获取预览URL响应模型"""
    success: bool = Field(..., description="获取是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional[List['PreViewData']] = Field(None, description="预览URL数据列表")


class UploadFileData(BaseModel):
    """上传文件数据"""
    file_id: str = Field(..., description="文件唯一标识")
    original_name: str = Field(..., description="原始文件名")
    file_name: str = Field(..., description="存储文件名")
    file_path: str = Field(..., description="文件存储路径")
    file_url: str = Field(..., description="文件访问URL")
    file_size: int = Field(..., description="文件大小（字节）")
    # file_type: str = Field(..., description="文件类型")
    mime_type: str = Field(..., description="MIME类型")
    upload_time: datetime = Field(..., description="上传时间")
    thumbnail_url: Optional[str] = Field(None, description="缩略图URL（仅图片）")


class PreViewData(BaseModel):
    """预览文件数据"""
    key: str = Field(..., description="文件key")
    url: str = Field(..., description="预览文件URL")


class BatchUploadRequest(BaseModel):
    """批量上传请求模型"""
    file_type: str = Field(..., description="文件类型：image 或 video")
    custom_path: Optional[str] = Field(None, description="自定义存储路径")
    generate_thumbnail: Optional[bool] = Field(False, description="是否生成缩略图（仅图片）")


class BatchUploadResponse(BaseModel):
    """批量上传响应模型"""
    success: bool = Field(..., description="批量上传是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional['BatchUploadData'] = Field(None, description="批量上传结果数据")


class BatchUploadData(BaseModel):
    """批量上传数据"""
    total_count: int = Field(..., description="总文件数")
    success_count: int = Field(..., description="成功上传数")
    failed_count: int = Field(..., description="失败上传数")
    success_files: list[UploadFileData] = Field(default_factory=list, description="成功上传的文件列表")
    failed_files: list['FailedFileInfo'] = Field(default_factory=list, description="失败上传的文件列表")


class FailedFileInfo(BaseModel):
    """失败文件信息"""
    original_name: str = Field(..., description="原始文件名")
    error_message: str = Field(..., description="错误信息")


class DeleteFileRequest(BaseModel):
    """删除文件请求模型"""
    file_path: str = Field(..., description="文件存储路径")


class DeleteFileResponse(BaseModel):
    """删除文件响应模型"""
    success: bool = Field(..., description="删除是否成功")
    message: str = Field(..., description="响应消息")


class FileInfoRequest(BaseModel):
    """获取文件信息请求模型"""
    file_path: str = Field(..., description="文件存储路径")


class FileInfoResponse(BaseModel):
    """获取文件信息响应模型"""
    success: bool = Field(..., description="获取是否成功")
    message: str = Field(..., description="响应消息")
    data: Optional['FileInfo'] = Field(None, description="文件信息")


class FileInfo(BaseModel):
    """文件信息"""
    file_name: str = Field(..., description="文件名")
    file_path: str = Field(..., description="文件路径")
    file_size: int = Field(..., description="文件大小（字节）")
    last_modified: datetime = Field(..., description="最后修改时间")
    content_type: str = Field(..., description="内容类型")
    etag: str = Field(..., description="文件ETag")


class GetPreViewRequest(BaseModel):
    """获取预览文件请求模型"""
    file_path: str = Field(..., description="文件存储路径")


# 更新前向引用
UploadFileResponse.model_rebuild()
BatchUploadResponse.model_rebuild()
BatchUploadData.model_rebuild()
FileInfoResponse.model_rebuild()
GetPreViewResponse.model_rebuild()
PreViewData.model_rebuild()
GetPreViewRequest.model_rebuild()
