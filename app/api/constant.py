
from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """错误响应模型"""
    detail: str = Field(..., description="错误详情", example="代理请求失败: 404")