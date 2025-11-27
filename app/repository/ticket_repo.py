from typing import List, Optional, Dict, Any
from datetime import date, datetime
from mysql.connector import pooling
from app.repository.base_repo import BaseRepository


class TicketRepository(BaseRepository):
    """票务数据仓储类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        super().__init__(pool)
    
    def get_time_slots_by_scenic_id(self, scenic_id: str, reservation_date: Optional[date] = None) -> List[Dict[str, Any]]:
        """根据景点ID查询所有时段的余票信息
        
        Args:
            scenic_id: 景点ID
            reservation_date: 预约日期，为空则查询所有日期
            
        Returns:
            时段余票列表
        """
        if reservation_date:
            query = """
                SELECT id, ticket_id, scenic_id, reservation_date, start_time, end_time,
                       total_quota, used_quota, remaining_quota, create_time, update_time
                FROM t_ticket_time_slot
                WHERE scenic_id = %s AND reservation_date = %s AND remaining_quota > 0
                ORDER BY start_time
            """
            return self.execute_query(query, (scenic_id, reservation_date))
        else:
            query = """
                SELECT id, ticket_id, scenic_id, reservation_date, start_time, end_time,
                       total_quota, used_quota, remaining_quota, create_time, update_time
                FROM t_ticket_time_slot
                WHERE scenic_id = %s AND remaining_quota > 0
                ORDER BY reservation_date, start_time
            """
            return self.execute_query(query, (scenic_id,))
    
    def get_time_slot_by_id(self, time_slot_id: str) -> Optional[Dict[str, Any]]:
        """根据时段ID查询时段信息"""
        query = """
            SELECT id, ticket_id, scenic_id, reservation_date, start_time, end_time,
                   total_quota, used_quota, remaining_quota, create_time, update_time
            FROM t_ticket_time_slot
            WHERE id = %s
        """
        result = self.execute_query(query, (time_slot_id,))
        return result[0] if result else None
    
    def get_time_slot_by_date_and_time(self, scenic_id: str, reservation_date: date, 
                                       start_time: str, end_time: str) -> Optional[Dict[str, Any]]:
        """根据景点ID、日期和时间段查询时段信息
        
        Args:
            scenic_id: 景点ID
            reservation_date: 预约日期
            start_time: 开始时间（格式：HH:MM）
            end_time: 结束时间（格式：HH:MM）
            
        Returns:
            时段信息字典，不存在则返回None
        """
        query = """
            SELECT id, ticket_id, scenic_id, reservation_date, start_time, end_time,
                   total_quota, used_quota, remaining_quota, create_time, update_time
            FROM t_ticket_time_slot
            WHERE scenic_id = %s AND reservation_date = %s 
                  AND start_time = %s AND end_time = %s
        """
        result = self.execute_query(query, (scenic_id, reservation_date, start_time, end_time))
        return result[0] if result else None
    
    def update_time_slot_quota(self, time_slot_id: str, quantity: int) -> int:
        """更新时段余票数量（减少余票，增加已用）"""
        query = """
            UPDATE t_ticket_time_slot
            SET used_quota = used_quota + %s,
                remaining_quota = remaining_quota - %s,
                update_time = NOW()
            WHERE id = %s AND remaining_quota >= %s
        """
        return self.execute_update(query, (quantity, quantity, time_slot_id, quantity))
    
    def create_electronic_ticket(self, ticket_data: Dict[str, Any]) -> int:
        """创建电子票凭证"""
        query = """
            INSERT INTO t_electronic_ticket 
            (id, order_id, ticket_id, qr_code_url, verification_code, 
             valid_start_date, valid_end_date, verification_status, refund_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            ticket_data['id'],
            ticket_data['order_id'],
            ticket_data['ticket_id'],
            ticket_data['qr_code_url'],
            ticket_data['verification_code'],
            ticket_data['valid_start_date'],
            ticket_data['valid_end_date'],
            ticket_data.get('verification_status', 1),
            ticket_data.get('refund_status', 1)
        )
        return self.execute_insert(query, params)
    
    def create_ticket_sales(self, sales_data: Dict[str, Any]) -> int:
        """创建票务销售记录"""
        query = """
            INSERT INTO t_ticket_sales 
            (id, order_no, sales_channel, channel_name, scenic_id, scenic_name,
             ticket_type, ticket_price, ticket_quantity, total_amount, 
             payment_status, payment_time, settlement_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            sales_data['id'],
            sales_data['order_no'],
            sales_data['sales_channel'],
            sales_data['channel_name'],
            sales_data['scenic_id'],
            sales_data['scenic_name'],
            sales_data['ticket_type'],
            sales_data['ticket_price'],
            sales_data['ticket_quantity'],
            sales_data['total_amount'],
            sales_data.get('payment_status', 1),
            sales_data.get('payment_time'),
            sales_data.get('settlement_status', 1)
        )
        return self.execute_insert(query, params)
    
    def get_electronic_tickets_by_order(self, order_no: str) -> List[Dict[str, Any]]:
        """根据订单号查询电子票"""
        query = """
            SELECT id, order_id, ticket_id, qr_code_url, verification_code,
                   valid_start_date, valid_end_date, verification_status, refund_status
            FROM t_electronic_ticket
            WHERE order_id = %s
        """
        return self.execute_query(query, (order_no,))