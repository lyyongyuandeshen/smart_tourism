from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MerchantApplicationBase(BaseModel):
    """商户申请基础模型"""
    application_no: str = Field(description="申请编号")
    shop_name: str = Field(description="店名")
    applicant_name: str = Field(description="申请人名称")
    business_scope: str = Field(description="经营范围")
    service_content: Optional[str] = Field(None, description="服务内容")
    status: int = Field(description="状态: 0-未完成, 1-审核中, 2-已完成, 3-已撤回")


class MerchantApplicationCreate(MerchantApplicationBase):
    """创建商户申请请求模型"""
    pass


class MerchantApplicationResponse(MerchantApplicationBase):
    """商户申请响应模型"""
    id: int = Field(description="主键ID")
    created_time: datetime = Field(description="创建时间")
    updated_time: Optional[datetime] = Field(None, description="最后更新时间")
    deleted: int = Field(description="逻辑删除: 0-未删除, 1-已删除")

    class Config:
        from_attributes = True


class MerchantApplicationQueryRequest(BaseModel):
    """商户申请查询请求模型"""
    application_no: Optional[str] = Field(None, description="申请编号")
    shop_name: Optional[str] = Field(None, description="店名（模糊查询）")
    applicant_name: Optional[str] = Field(None, description="申请人名称（模糊查询）")
    business_scope: Optional[str] = Field(None, description="经营范围（模糊查询）")
    status: Optional[int] = Field(None, description="状态")
    start_date: Optional[str] = Field(None, description="开始日期 (YYYY-MM-DD)")
    end_date: Optional[str] = Field(None, description="结束日期 (YYYY-MM-DD)")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(10, ge=1, le=100, description="每页数量")


class MerchantApplicationListResponse(BaseModel):
    """商户申请列表响应模型"""
    success: bool
    message: str
    total: int = Field(description="总记录数")
    page: int = Field(description="当前页码")
    page_size: int = Field(description="每页数量")
    data: list[MerchantApplicationResponse] = Field(description="商户申请列表")


class MerchantApplicationSubmitResponse(BaseModel):
    """商户申请提交响应模型"""
    success: bool
    message: str
    application_no: Optional[str] = None


class MerchantApplicationStatusUpdateRequest(BaseModel):
    """商户申请状态更新请求模型"""
    application_no: str = Field(description="申请编号")
    status: int = Field(description="新状态: 1-审核中")
    comment: Optional[str] = Field(None, description="状态变更说明")


class MerchantApplicationAuditRequest(BaseModel):
    """商户申请审核请求模型"""
    application_no: str = Field(description="申请编号")
    status: int = Field(description="审核结果: 2-已完成（通过）, 3-已撤回（拒绝）")
    audit_comment: Optional[str] = Field(None, description="审核意见")


class MerchantApplicationStatusUpdateResponse(BaseModel):
    """商户申请状态更新响应模型"""
    success: bool
    message: str
    application_no: Optional[str] = None


class MerchantApplicationAuditResponse(BaseModel):
    """商户申请审核响应模型"""
    success: bool
    message: str
    application_no: Optional[str] = None


class MerchantApplicationDeleteResponse(BaseModel):
    """商户申请删除响应模型"""
    success: bool
    message: str
    application_no: Optional[str] = None