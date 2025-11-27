from typing import Dict, Any, Optional
from datetime import datetime
from mysql.connector import pooling
from app.repository.base_repo import BaseRepository


class OrderRepository(BaseRepository):
    """订单数据仓储类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        super().__init__(pool)
    
    def create_order(self, order_data: Dict[str, Any]) -> int:
        """创建订单
        
        Args:
            order_data: 订单数据字典
            
        Returns:
            影响的行数
        """
        query = """
            INSERT INTO t_order 
            (id, order_no, user_id, scenic_id, scenic_name, order_title,
             order_price, ticket_quantity, reschedule_limit, reschedule_used,
             order_time, order_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            order_data['id'],
            order_data['order_no'],
            order_data['user_id'],
            order_data['scenic_id'],
            order_data['scenic_name'],
            order_data['order_title'],
            order_data['order_price'],
            order_data['ticket_quantity'],
            order_data.get('reschedule_limit', 1),
            order_data.get('reschedule_used', 0),
            order_data['order_time'],
            order_data.get('order_status', 2)  # 默认2-已支付
        )
        return self.execute_insert(query, params)
    
    def get_order_by_order_no(self, order_no: str) -> Optional[Dict[str, Any]]:
        """根据订单号查询订单
        
        Args:
            order_no: 订单号
            
        Returns:
            订单信息字典，不存在则返回None
        """
        query = """
            SELECT id, order_no, user_id, scenic_id, scenic_name, order_title,
                   order_price, ticket_quantity, reschedule_limit, reschedule_used,
                   order_time, order_status, create_time, update_time
            FROM t_order
            WHERE order_no = %s
        """
        result = self.execute_query(query, (order_no,))
        return result[0] if result else None
    
    def update_reschedule_count(self, order_no: str) -> int:
        """更新订单改签次数
        
        Args:
            order_no: 订单号
            
        Returns:
            影响的行数
        """
        query = """
            UPDATE t_order
            SET reschedule_used = reschedule_used + 1,
                update_time = NOW()
            WHERE order_no = %s AND reschedule_used < reschedule_limit
        """
        return self.execute_update(query, (order_no,))
