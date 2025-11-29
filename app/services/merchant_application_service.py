from typing import List, Optional
from mysql.connector import pooling

from app.repository.merchant_application_repo import MerchantApplicationRepository
from app.models.merchant_application_models import (
    MerchantApplicationResponse,
    MerchantApplicationCreate,
    MerchantApplicationQueryRequest,
    MerchantApplicationListResponse,
    MerchantApplicationSubmitResponse,
    MerchantApplicationStatusUpdateRequest,
    MerchantApplicationStatusUpdateResponse,
    MerchantApplicationAuditRequest,
    MerchantApplicationAuditResponse,
    MerchantApplicationDeleteResponse
)


class MerchantApplicationService:
    """商户申请业务服务类"""

    def __init__(self, pool: pooling.MySQLConnectionPool):
        self.application_repo = MerchantApplicationRepository(pool)

    def query_merchant_applications(self, request: MerchantApplicationQueryRequest) -> MerchantApplicationListResponse:
        """
        查询商户申请列表
        
        Args:
            request: 查询请求参数
            
        Returns:
            商户申请列表响应
        """
        try:
            # 计算偏移量
            offset = (request.page - 1) * request.page_size
            
            # 查询商户申请列表
            applications = self.application_repo.get_merchant_applications(
                application_no=request.application_no,
                shop_name=request.shop_name,
                applicant_name=request.applicant_name,
                business_scope=request.business_scope,
                status=request.status,
                start_date=request.start_date,
                end_date=request.end_date,
                offset=offset,
                limit=request.page_size
            )
            
            # 查询总数
            total = self.application_repo.count_merchant_applications(
                application_no=request.application_no,
                shop_name=request.shop_name,
                applicant_name=request.applicant_name,
                business_scope=request.business_scope,
                status=request.status,
                start_date=request.start_date,
                end_date=request.end_date
            )
            
            # 转换为响应模型
            application_list = [
                MerchantApplicationResponse(
                    id=app['id'],
                    application_no=app['application_no'],
                    shop_name=app['shop_name'],
                    applicant_name=app['applicant_name'],
                    business_scope=app['business_scope'],
                    service_content=app.get('service_content'),
                    status=app['status'],
                    created_time=app['created_time'],
                    updated_time=app.get('updated_time'),
                    deleted=app['deleted']
                )
                for app in applications
            ]
            
            return MerchantApplicationListResponse(
                success=True,
                message="查询成功",
                total=total,
                page=request.page,
                page_size=request.page_size,
                data=application_list
            )
            
        except Exception as e:
            return MerchantApplicationListResponse(
                success=False,
                message=f"查询失败：{str(e)}",
                total=0,
                page=request.page,
                page_size=request.page_size,
                data=[]
            )

    def get_merchant_application_by_no(self, application_no: str) -> Optional[MerchantApplicationResponse]:
        """
        根据申请编号查询商户申请详情
        
        Args:
            application_no: 申请编号
            
        Returns:
            商户申请详情
        """
        try:
            application = self.application_repo.get_merchant_application_by_no(application_no)
            
            if not application:
                return None
            
            return MerchantApplicationResponse(
                id=application['id'],
                application_no=application['application_no'],
                shop_name=application['shop_name'],
                applicant_name=application['applicant_name'],
                business_scope=application['business_scope'],
                service_content=application.get('service_content'),
                status=application['status'],
                created_time=application['created_time'],
                updated_time=application.get('updated_time'),
                deleted=application['deleted']
            )
            
        except Exception as e:
            return None

    def submit_merchant_application(self, application: MerchantApplicationCreate) -> MerchantApplicationSubmitResponse:
        """
        提交商户申请
        
        Args:
            application: 商户申请信息
            
        Returns:
            提交响应
        """
        try:
            # 生成申请编号
            application_no = self.application_repo.generate_application_no()
            
            # 检查申请编号是否已存在
            existing_application = self.application_repo.get_merchant_application_by_no(application_no)
            
            if existing_application:
                # 如果编号已存在，重新生成
                application_no = self.application_repo.generate_application_no()
            
            application_data = {
                'application_no': application_no,
                'shop_name': application.shop_name,
                'applicant_name': application.applicant_name,
                'business_scope': application.business_scope,
                'service_content': application.service_content,
                'status': 0  # 默认状态为未完成
            }
            
            # 创建新申请
            rows_affected = self.application_repo.create_merchant_application(application_data)
            
            if rows_affected > 0:
                return MerchantApplicationSubmitResponse(
                    success=True,
                    message="商户申请提交成功",
                    application_no=application_no
                )
            else:
                return MerchantApplicationSubmitResponse(
                    success=False,
                    message="商户申请提交失败"
                )
                
        except Exception as e:
            return MerchantApplicationSubmitResponse(
                success=False,
                message=f"提交失败：{str(e)}"
            )

    def audit_merchant_application(self, audit_request: MerchantApplicationAuditRequest) -> MerchantApplicationAuditResponse:
        """
        审核商户申请
        
        业务规则：
        1. 只有状态为 1-审核中 的申请才能被审核
        2. 审核结果只能是 2-已完成（通过）或 3-已撤回（拒绝）
        3. 已完成或已撤回的申请不能再次审核
        
        Args:
            audit_request: 审核请求
            
        Returns:
            审核响应
        """
        try:
            # 检查申请是否存在
            existing_application = self.application_repo.get_merchant_application_by_no(audit_request.application_no)
            
            if not existing_application:
                return MerchantApplicationAuditResponse(
                    success=False,
                    message=f"商户申请不存在：{audit_request.application_no}"
                )
            
            # 检查当前状态是否可以审核
            current_status = existing_application['status']
            if current_status != 1:  # 只有审核中的申请才能被审核
                status_text = {0: "未完成", 1: "审核中", 2: "已完成", 3: "已撤回"}
                return MerchantApplicationAuditResponse(
                    success=False,
                    message=f"申请当前状态为'{status_text.get(current_status, '未知')}'，只有'审核中'的申请才能被审核"
                )
            
            # 检查审核结果状态是否有效（只能审核为完成或撤回）
            if audit_request.status not in [2, 3]:
                return MerchantApplicationAuditResponse(
                    success=False,
                    message="无效的审核结果，只能审核为：2-已完成（通过）, 3-已撤回（拒绝）"
                )
            
            # 更新申请状态
            rows_affected = self.application_repo.update_application_status(
                audit_request.application_no,
                audit_request.status
            )
            
            if rows_affected > 0:
                status_text = {2: "已完成", 3: "已撤回"}
                action_text = {2: "审核通过", 3: "审核拒绝"}
                return MerchantApplicationAuditResponse(
                    success=True,
                    message=f"商户申请{action_text[audit_request.status]}，状态已更新为：{status_text[audit_request.status]}",
                    application_no=audit_request.application_no
                )
            else:
                return MerchantApplicationAuditResponse(
                    success=False,
                    message="商户申请审核失败"
                )
                
        except Exception as e:
            return MerchantApplicationAuditResponse(
                success=False,
                message=f"审核失败：{str(e)}"
            )

    def delete_merchant_application(self, application_no: str) -> MerchantApplicationDeleteResponse:
        """
        删除商户申请信息
        
        Args:
            application_no: 申请编号
            
        Returns:
            删除响应
        """
        try:
            # 检查申请是否存在
            existing_application = self.application_repo.get_merchant_application_by_no(application_no)
            
            if not existing_application:
                return MerchantApplicationDeleteResponse(
                    success=False,
                    message=f"商户申请不存在：{application_no}"
                )
            
            # 删除申请（逻辑删除）
            rows_affected = self.application_repo.delete_merchant_application(application_no)
            
            if rows_affected > 0:
                return MerchantApplicationDeleteResponse(
                    success=True,
                    message="商户申请删除成功",
                    application_no=application_no
                )
            else:
                return MerchantApplicationDeleteResponse(
                    success=False,
                    message="商户申请删除失败"
                )
                
        except Exception as e:
            return MerchantApplicationDeleteResponse(
                success=False,
                message=f"删除失败：{str(e)}"
            )