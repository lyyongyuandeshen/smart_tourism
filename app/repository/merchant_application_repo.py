from typing import List, Optional, Dict, Any
from mysql.connector import pooling
from app.repository.base_repo import BaseRepository


class MerchantApplicationRepository(BaseRepository):
    """商户申请数据仓储类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        super().__init__(pool)
    
    def get_merchant_applications(
        self, 
        application_no: Optional[str] = None,
        shop_name: Optional[str] = None,
        applicant_name: Optional[str] = None,
        business_scope: Optional[str] = None,
        status: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        offset: int = 0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        查询商户申请列表（支持多条件查询）
        
        Args:
            application_no: 申请编号（精确匹配）
            shop_name: 店名（模糊匹配）
            applicant_name: 申请人名称（模糊匹配）
            business_scope: 经营范围（模糊匹配）
            status: 状态（精确匹配）
            start_date: 开始日期
            end_date: 结束日期
            offset: 偏移量
            limit: 每页数量
            
        Returns:
            商户申请列表
        """
        # 构建动态查询条件
        conditions = ["deleted = 0"]  # 只查询未删除的记录
        params = []
        
        if application_no:
            conditions.append("application_no = %s")
            params.append(application_no)
        
        if shop_name:
            conditions.append("shop_name LIKE %s")
            params.append(f"%{shop_name}%")
        
        if applicant_name:
            conditions.append("applicant_name LIKE %s")
            params.append(f"%{applicant_name}%")
        
        if business_scope:
            conditions.append("business_scope LIKE %s")
            params.append(f"%{business_scope}%")
        
        if status is not None:
            conditions.append("status = %s")
            params.append(status)
        
        if start_date:
            conditions.append("DATE(created_time) >= %s")
            params.append(start_date)
        
        if end_date:
            conditions.append("DATE(created_time) <= %s")
            params.append(end_date)
        
        # 构建WHERE子句
        where_clause = "WHERE " + " AND ".join(conditions)
        
        # 查询语句
        query = f"""
            SELECT id, application_no, shop_name, applicant_name, business_scope,
                   service_content, status, created_time, updated_time, deleted
            FROM t_merchant_application
            {where_clause}
            ORDER BY created_time DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        
        return self.execute_query(query, params)
    
    def count_merchant_applications(
        self,
        application_no: Optional[str] = None,
        shop_name: Optional[str] = None,
        applicant_name: Optional[str] = None,
        business_scope: Optional[str] = None,
        status: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> int:
        """
        统计商户申请总数
        
        Args:
            application_no: 申请编号
            shop_name: 店名
            applicant_name: 申请人名称
            business_scope: 经营范围
            status: 状态
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            总记录数
        """
        # 构建动态查询条件
        conditions = ["deleted = 0"]  # 只统计未删除的记录
        params = []
        
        if application_no:
            conditions.append("application_no = %s")
            params.append(application_no)
        
        if shop_name:
            conditions.append("shop_name LIKE %s")
            params.append(f"%{shop_name}%")
        
        if applicant_name:
            conditions.append("applicant_name LIKE %s")
            params.append(f"%{applicant_name}%")
        
        if business_scope:
            conditions.append("business_scope LIKE %s")
            params.append(f"%{business_scope}%")
        
        if status is not None:
            conditions.append("status = %s")
            params.append(status)
        
        if start_date:
            conditions.append("DATE(created_time) >= %s")
            params.append(start_date)
        
        if end_date:
            conditions.append("DATE(created_time) <= %s")
            params.append(end_date)
        
        # 构建WHERE子句
        where_clause = "WHERE " + " AND ".join(conditions)
        
        query = f"""
            SELECT COUNT(*) as total
            FROM t_merchant_application
            {where_clause}
        """
        
        result = self.execute_query(query, params)
        return result[0]['total'] if result else 0
    
    def get_merchant_application_by_no(self, application_no: str) -> Optional[Dict[str, Any]]:
        """
        根据申请编号查询商户申请信息
        
        Args:
            application_no: 申请编号
            
        Returns:
            商户申请信息
        """
        query = """
            SELECT id, application_no, shop_name, applicant_name, business_scope,
                   service_content, status, created_time, updated_time, deleted
            FROM t_merchant_application
            WHERE application_no = %s AND deleted = 0
        """
        result = self.execute_query(query, (application_no,))
        return result[0] if result else None
    
    def create_merchant_application(self, application_data: Dict[str, Any]) -> int:
        """
        创建商户申请信息
        
        Args:
            application_data: 申请数据
            
        Returns:
            影响的行数
        """
        query = """
            INSERT INTO t_merchant_application 
            (application_no, shop_name, applicant_name, business_scope, 
             service_content, status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            application_data['application_no'],
            application_data['shop_name'],
            application_data['applicant_name'],
            application_data['business_scope'],
            application_data.get('service_content'),
            application_data['status']
        )
        
        return self.execute_update(query, params)
    
    def update_merchant_application(self, application_no: str, application_data: Dict[str, Any]) -> int:
        """
        更新商户申请信息
        
        Args:
            application_no: 申请编号
            application_data: 申请数据
            
        Returns:
            影响的行数
        """
        query = """
            UPDATE t_merchant_application 
            SET shop_name = %s, applicant_name = %s, business_scope = %s,
                service_content = %s, status = %s, updated_time = CURRENT_TIMESTAMP
            WHERE application_no = %s AND deleted = 0
        """
        params = (
            application_data['shop_name'],
            application_data['applicant_name'],
            application_data['business_scope'],
            application_data.get('service_content'),
            application_data['status'],
            application_no
        )
        
        return self.execute_update(query, params)
    
    def update_application_status(self, application_no: str, status: int) -> int:
        """
        更新申请状态
        
        Args:
            application_no: 申请编号
            status: 新状态
            
        Returns:
            影响的行数
        """
        query = """
            UPDATE t_merchant_application 
            SET status = %s, updated_time = CURRENT_TIMESTAMP
            WHERE application_no = %s AND deleted = 0
        """
        
        return self.execute_update(query, (status, application_no))
    
    def delete_merchant_application(self, application_no: str) -> int:
        """
        删除商户申请信息（逻辑删除）
        
        Args:
            application_no: 申请编号
            
        Returns:
            影响的行数
        """
        query = """
            UPDATE t_merchant_application 
            SET deleted = 1, updated_time = CURRENT_TIMESTAMP
            WHERE application_no = %s AND deleted = 0
        """
        
        return self.execute_update(query, (application_no,))
    
    def generate_application_no(self) -> str:
        """
        生成申请编号
        格式：SN + YYYYMMDD + XJ + 4位序号
        
        Returns:
            申请编号
        """
        from datetime import datetime
        
        # 获取当前日期
        today = datetime.now().strftime('%Y%m%d')
        prefix = f"SN{today}XJ"
        
        # 查询当天最大序号
        query = """
            SELECT MAX(CAST(SUBSTRING(application_no, -4) AS UNSIGNED)) as max_seq
            FROM t_merchant_application
            WHERE application_no LIKE %s
        """
        
        result = self.execute_query(query, (f"{prefix}%",))
        max_seq = result[0]['max_seq'] if result and result[0]['max_seq'] else 0
        
        # 生成新序号
        new_seq = max_seq + 1
        return f"{prefix}{new_seq:04d}"