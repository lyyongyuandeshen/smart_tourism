from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from app.models.merchant_application_models import (
    MerchantApplicationCreate,
    MerchantApplicationResponse,
    MerchantApplicationQueryRequest,
    MerchantApplicationListResponse,
    MerchantApplicationSubmitResponse,
    MerchantApplicationAuditRequest,
    MerchantApplicationAuditResponse,
    MerchantApplicationDeleteResponse
)
from app.services.merchant_application_service import MerchantApplicationService
from app.config.config import config

router = APIRouter()


def get_merchant_application_service() -> MerchantApplicationService:
    """获取商户申请服务实例"""
    pool = config.get_mysql_pool()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库连接池未初始化"
        )
    return MerchantApplicationService(pool)


@router.get("/list", response_model=MerchantApplicationListResponse)
async def query_merchant_applications(
        application_no: Optional[str] = Query(None, description="申请编号（精确匹配）"),
        shop_name: Optional[str] = Query(None, description="店名（模糊匹配）"),
        applicant_name: Optional[str] = Query(None, description="申请人名称（模糊匹配）"),
        business_scope: Optional[str] = Query(None, description="经营范围（模糊匹配）"),
        status: Optional[int] = Query(None, description="状态: 0-未完成, 1-审核中, 2-已完成, 3-已撤回"),
        start_date: Optional[str] = Query(None, description="开始日期 (YYYY-MM-DD)"),
        end_date: Optional[str] = Query(None, description="结束日期 (YYYY-MM-DD)"),
        page: int = Query(1, ge=1, description="页码"),
        page_size: int = Query(10, ge=1, le=100, description="每页数量"),
        application_service: MerchantApplicationService = Depends(get_merchant_application_service)
):
    """
    查询商户申请列表
    
    支持以下查询方式：
    - 全量查询：不传任何参数，返回所有申请（分页）
    - 根据店名查询：传入shop_name参数（支持模糊匹配）
    - 根据申请人查询：传入applicant_name参数（支持模糊匹配）
    - 根据经营范围查询：传入business_scope参数（支持模糊匹配）
    - 根据状态查询：传入status参数
    - 根据创建时间查询：传入start_date和end_date参数
    - 组合查询：可以同时传入多个参数
    
    注意：
    - 如需查询单个申请详情，建议使用 GET /{application_no} 接口
    - application_no参数仍然支持，但推荐使用详情接口获得更好的性能
    
    Args:
        application_no: 申请编号（建议使用详情接口）
        shop_name: 店名
        applicant_name: 申请人名称
        business_scope: 经营范围
        status: 状态
        start_date: 开始日期
        end_date: 结束日期
        page: 页码
        page_size: 每页数量
        application_service: 商户申请服务实例
        
    Returns:
        商户申请列表响应
    """
    try:
        request = MerchantApplicationQueryRequest(
            application_no=application_no,
            shop_name=shop_name,
            applicant_name=applicant_name,
            business_scope=business_scope,
            status=status,
            start_date=start_date,
            end_date=end_date,
            page=page,
            page_size=page_size
        )

        response = application_service.query_merchant_applications(request)
        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/{application_no}", response_model=MerchantApplicationResponse)
async def get_merchant_application_detail(
        application_no: str,
        application_service: MerchantApplicationService = Depends(get_merchant_application_service)
):
    """
    根据申请编号查询商户申请详情
    
    Args:
        application_no: 申请编号
        application_service: 商户申请服务实例
        
    Returns:
        商户申请详情
    """
    try:
        application = application_service.get_merchant_application_by_no(application_no)

        if not application:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"商户申请不存在：{application_no}"
            )

        return application

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.post("/submit", response_model=MerchantApplicationSubmitResponse)
async def submit_merchant_application(
        application: MerchantApplicationCreate,
        application_service: MerchantApplicationService = Depends(get_merchant_application_service)
):
    """
    提交商户申请
    
    用户可以提交新的商户申请，系统会自动生成申请编号。
    
    Args:
        application: 商户申请信息
        application_service: 商户申请服务实例
        
    Returns:
        提交响应
    """
    try:
        response = application_service.submit_merchant_application(application)

        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"提交失败：{str(e)}"
        )


@router.post("/audit", response_model=MerchantApplicationAuditResponse)
async def audit_merchant_application(
        audit_request: MerchantApplicationAuditRequest,
        application_service: MerchantApplicationService = Depends(get_merchant_application_service)
):
    """
    审核商户申请
    
    管理员可以审核用户的申请，给出最终的审核结果。
    
    业务规则：
    - 只有状态为 1-审核中 的申请才能被审核
    - 审核结果只能是 2-已完成（通过）或 3-已撤回（拒绝）
    - 已完成或已撤回的申请不能再次审核
    
    流程说明：
    1. 用户提交申请（状态：0-未完成）
    2. 管理员将申请纳入审核流程（使用 update-status 接口，状态变为：1-审核中）
    3. 管理员进行审核（使用此接口，状态变为：2-已完成 或 3-已撤回）
    
    Args:
        audit_request: 审核请求
        application_service: 商户申请服务实例
        
    Returns:
        审核响应
    """
    try:
        response = application_service.audit_merchant_application(audit_request)

        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND if "不存在" in response.message else status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"审核失败：{str(e)}"
        )


@router.delete("/{application_no}", response_model=MerchantApplicationDeleteResponse)
async def delete_merchant_application(
        application_no: str,
        application_service: MerchantApplicationService = Depends(get_merchant_application_service)
):
    """
    删除商户申请信息
    
    Args:
        application_no: 申请编号
        application_service: 商户申请服务实例
        
    Returns:
        删除响应
    """
    try:
        response = application_service.delete_merchant_application(application_no)

        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND if "不存在" in response.message else status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败：{str(e)}"
        )
