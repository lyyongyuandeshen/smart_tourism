import uuid
import hashlib
from datetime import datetime, date
from decimal import Decimal
from typing import List, Optional
from mysql.connector import pooling

from app.repository.ticket_repo import TicketRepository
from app.repository.order_repo import OrderRepository
from app.models.ticket_models import (
    TicketTimeSlotResponse, 
    PurchaseTicketRequest, 
    PurchaseTicketResponse
)


class TicketService:
    """票务业务服务类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        self.ticket_repo = TicketRepository(pool)
        self.order_repo = OrderRepository(pool)
    
    def get_available_time_slots(self, scenic_id: str, reservation_date: Optional[date] = None) -> List[TicketTimeSlotResponse]:
        """
        根据景点ID查询所有可用时段的余票信息
        
        Args:
            scenic_id: 景点ID
            reservation_date: 预约日期，为空则默认为当天日期
            
        Returns:
            时段余票列表
        """
        # 如果没有指定日期，默认为当天
        if reservation_date is None:
            reservation_date = date.today()
        
        time_slots = self.ticket_repo.get_time_slots_by_scenic_id(scenic_id, reservation_date)
        
        return [
            TicketTimeSlotResponse(
                id=slot['id'],
                ticket_id=slot['ticket_id'],
                scenic_id=slot['scenic_id'],
                reservation_date=slot['reservation_date'],
                start_time=slot['start_time'],
                end_time=slot['end_time'],
                total_quota=slot['total_quota'],
                used_quota=slot['used_quota'],
                remaining_quota=slot['remaining_quota']
            )
            for slot in time_slots
        ]
    
    def purchase_ticket(self, request: PurchaseTicketRequest) -> PurchaseTicketResponse:
        """
        购票接口
        
        Args:
            request: 购票请求
            
        Returns:
            购票响应
        """
        try:
            # 1. 根据景点ID、日期和时间段查询时段信息，验证余票是否充足
            time_slot = self.ticket_repo.get_time_slot_by_date_and_time(
                request.scenic_id,
                request.ticket_date,
                request.start_time,
                request.end_time
            )
            
            if not time_slot:
                return PurchaseTicketResponse(
                    success=False,
                    message="该时段不存在或已关闭预约"
                )
            
            if time_slot['remaining_quota'] < request.ticket_quantity:
                return PurchaseTicketResponse(
                    success=False,
                    message=f"余票不足，当前剩余 {time_slot['remaining_quota']} 张"
                )
            
            # 2. 更新时段余票数量
            updated_rows = self.ticket_repo.update_time_slot_quota(
                time_slot['id'], 
                request.ticket_quantity
            )
            
            if updated_rows == 0:
                return PurchaseTicketResponse(
                    success=False,
                    message="余票不足或更新失败，请重试"
                )
            
            # 3. 生成订单号
            order_no = self._generate_order_no()
            order_time = datetime.now()
            
            # 4. 计算总金额
            total_amount = request.ticket_price * request.ticket_quantity
            
            # 5. 创建订单记录
            order_id = str(uuid.uuid4())
            order_data = {
                'id': order_id,
                'order_no': order_no,
                'user_id': request.user_id,
                'scenic_id': request.scenic_id,
                'scenic_name': request.scenic_name,
                'order_title': request.order_title,
                'order_price': total_amount,
                'ticket_quantity': request.ticket_quantity,
                'reschedule_limit': 1,  # 默认改签次数上限为1
                'reschedule_used': 0,
                'order_time': order_time,
                'order_status': 2  # 2-已支付
            }
            self.order_repo.create_order(order_data)
            
            # 6. 创建票务销售记录
            sales_id = str(uuid.uuid4())
            sales_data = {
                'id': sales_id,
                'order_no': order_no,
                'sales_channel': request.sales_channel,
                'channel_name': request.channel_name,
                'scenic_id': request.scenic_id,
                'scenic_name': request.scenic_name,
                'ticket_type': 1,  # 默认为成人票
                'ticket_price': request.ticket_price,
                'ticket_quantity': request.ticket_quantity,
                'total_amount': total_amount,
                'payment_status': 1,  # 1-已支付
                'payment_time': order_time,
                'settlement_status': 1  # 1-未分账
            }
            self.ticket_repo.create_ticket_sales(sales_data)
            
            # 7. 生成电子票凭证（根据购票数量和游客信息生成多张）
            electronic_tickets = []
            for i in range(request.ticket_quantity):
                ticket_id = str(uuid.uuid4())
                verification_code = self._generate_verification_code(order_no, i)
                qr_code_url = self._generate_qr_code_url(ticket_id, verification_code)
                
                # 计算有效期：从票日期开始，到票日期结束
                valid_start_date = request.ticket_date
                valid_end_date = request.ticket_date
                
                ticket_data = {
                    'id': ticket_id,
                    'order_id': order_no,
                    'ticket_id': time_slot['ticket_id'],
                    'qr_code_url': qr_code_url,
                    'verification_code': verification_code,
                    'valid_start_date': valid_start_date,
                    'valid_end_date': valid_end_date,
                    'verification_status': 1,  # 1-未核销
                    'refund_status': 1  # 1-未退款
                }
                self.ticket_repo.create_electronic_ticket(ticket_data)
                
                # 添加游客信息到电子票响应中
                tourist_info = request.tourists[i] if i < len(request.tourists) else None
                ticket_info = {
                    'ticket_id': ticket_id,
                    'verification_code': verification_code,
                    'qr_code_url': qr_code_url,
                    'valid_start_date': str(valid_start_date),
                    'valid_end_date': str(valid_end_date),
                    'tourist_name': tourist_info.name if tourist_info else '',
                    'tourist_phone': tourist_info.phone if tourist_info else ''
                }
                electronic_tickets.append(ticket_info)
            
            return PurchaseTicketResponse(
                success=True,
                message="购票成功",
                order_no=order_no,
                electronic_tickets=electronic_tickets,
                total_amount=total_amount
            )
            
        except Exception as e:
            return PurchaseTicketResponse(
                success=False,
                message=f"购票失败：{str(e)}"
            )
    
    def _generate_order_no(self) -> str:
        """生成订单号"""
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        random_str = str(uuid.uuid4())[:8].upper()
        return f"ORD{timestamp}{random_str}"
    
    def _generate_verification_code(self, order_no: str, index: int) -> str:
        """生成核销码"""
        raw_str = f"{order_no}_{index}_{datetime.now().timestamp()}"
        hash_obj = hashlib.md5(raw_str.encode())
        return hash_obj.hexdigest()[:16].upper()
    
    def _generate_qr_code_url(self, ticket_id: str, verification_code: str) -> str:
        """生成二维码URL（实际项目中应该调用二维码生成服务）"""
        # TODO 实际应该生成真实的二维码图片并上传到OSS
        return f"https://qrcode.example.com/ticket/{ticket_id}?code={verification_code}"