import uuid
from typing import List, Optional
from mysql.connector import pooling

from app.repository.scenic_repo import ScenicRepository
from app.models.scenic_models import (
    ScenicGuideCreateRequest,
    ScenicGuideUpdateRequest,
    ScenicGuideResponse,
    TimeSlotCreateRequest,
    TimeSlotUpdateRequest,
    TimeSlotBatchCreateRequest,
    CommonResponse
)
from app.models.ticket_models import TicketTimeSlotResponse


class ScenicService:
    """景点导览业务服务类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        self.scenic_repo = ScenicRepository(pool)
    
    # ========== 景点导览相关服务 ==========
    
    def create_scenic_guide(self, request: ScenicGuideCreateRequest) -> CommonResponse:
        """创建景点导览"""
        try:
            # 检查景点是否已存在导览信息
            existing = self.scenic_repo.get_scenic_guide_by_scenic_id(request.scenic_id)
            if existing:
                return CommonResponse(
                    success=False,
                    message=f"景点 {request.scenic_id} 已存在导览信息"
                )
            
            guide_id = str(uuid.uuid4())
            guide_data = {
                'id': guide_id,
                'scenic_id': request.scenic_id,
                'guide_title': request.guide_title,
                'historical_background': request.historical_background,
                'cultural_value': request.cultural_value,
                'architectural_features': request.architectural_features,
                'historical_stories': request.historical_stories,
                'ecological_science': request.ecological_science,
                'open_status': request.open_status,
                'last_bus_time': request.last_bus_time,
                'evacuation_route_url': request.evacuation_route_url
            }
            
            self.scenic_repo.create_scenic_guide(guide_data)
            
            return CommonResponse(
                success=True,
                message="创建成功",
                data={'id': guide_id}
            )
        except Exception as e:
            return CommonResponse(
                success=False,
                message=f"创建失败：{str(e)}"
            )
    
    def get_scenic_guide(self, guide_id: str) -> Optional[ScenicGuideResponse]:
        """根据ID查询景点导览"""
        guide = self.scenic_repo.get_scenic_guide_by_id(guide_id)
        if not guide:
            return None
        
        return ScenicGuideResponse(**guide)
    
    def get_scenic_guide_by_scenic_id(self, scenic_id: str) -> Optional[ScenicGuideResponse]:
        """根据景点ID查询景点导览"""
        guide = self.scenic_repo.get_scenic_guide_by_scenic_id(scenic_id)
        if not guide:
            return None
        
        return ScenicGuideResponse(**guide)
    
    def get_all_scenic_guides(self, open_status: Optional[int] = None) -> List[ScenicGuideResponse]:
        """查询所有景点导览"""
        guides = self.scenic_repo.get_all_scenic_guides(open_status)
        return [ScenicGuideResponse(**guide) for guide in guides]
    
    def update_scenic_guide(self, guide_id: str, request: ScenicGuideUpdateRequest) -> CommonResponse:
        """更新景点导览"""
        try:
            # 检查导览是否存在
            existing = self.scenic_repo.get_scenic_guide_by_id(guide_id)
            if not existing:
                return CommonResponse(
                    success=False,
                    message="景点导览不存在"
                )
            
            # 构建更新数据（只更新非None的字段）
            update_data = {}
            if request.guide_title is not None:
                update_data['guide_title'] = request.guide_title
            if request.historical_background is not None:
                update_data['historical_background'] = request.historical_background
            if request.cultural_value is not None:
                update_data['cultural_value'] = request.cultural_value
            if request.architectural_features is not None:
                update_data['architectural_features'] = request.architectural_features
            if request.historical_stories is not None:
                update_data['historical_stories'] = request.historical_stories
            if request.ecological_science is not None:
                update_data['ecological_science'] = request.ecological_science
            if request.open_status is not None:
                update_data['open_status'] = request.open_status
            if request.last_bus_time is not None:
                update_data['last_bus_time'] = request.last_bus_time
            if request.evacuation_route_url is not None:
                update_data['evacuation_route_url'] = request.evacuation_route_url
            
            if not update_data:
                return CommonResponse(
                    success=False,
                    message="没有需要更新的字段"
                )
            
            rows_affected = self.scenic_repo.update_scenic_guide(guide_id, update_data)
            
            if rows_affected > 0:
                return CommonResponse(
                    success=True,
                    message="更新成功"
                )
            else:
                return CommonResponse(
                    success=False,
                    message="更新失败"
                )
        except Exception as e:
            return CommonResponse(
                success=False,
                message=f"更新失败：{str(e)}"
            )
    
    def delete_scenic_guide(self, guide_id: str) -> CommonResponse:
        """删除景点导览"""
        try:
            # 检查导览是否存在
            existing = self.scenic_repo.get_scenic_guide_by_id(guide_id)
            if not existing:
                return CommonResponse(
                    success=False,
                    message="景点导览不存在"
                )
            
            rows_affected = self.scenic_repo.delete_scenic_guide(guide_id)
            
            if rows_affected > 0:
                return CommonResponse(
                    success=True,
                    message="删除成功"
                )
            else:
                return CommonResponse(
                    success=False,
                    message="删除失败"
                )
        except Exception as e:
            return CommonResponse(
                success=False,
                message=f"删除失败：{str(e)}"
            )
    
    # ========== 票务时段管理相关服务 ==========
    
    def create_time_slot(self, request: TimeSlotCreateRequest) -> CommonResponse:
        """按时段创建票务时段"""
        try:
            slot_id = str(uuid.uuid4())
            slot_data = {
                'id': slot_id,
                'ticket_id': request.ticket_id,
                'scenic_id': request.scenic_id,
                'reservation_date': request.reservation_date,
                'start_time': request.start_time,
                'end_time': request.end_time,
                'total_quota': request.total_quota,
                'used_quota': 0,
                'remaining_quota': request.total_quota
            }
            
            self.scenic_repo.create_time_slot(slot_data)
            
            return CommonResponse(
                success=True,
                message="创建成功",
                data={'id': slot_id}
            )
        except Exception as e:
            return CommonResponse(
                success=False,
                message=f"创建失败：{str(e)}"
            )
    
    def batch_create_time_slots(self, request: TimeSlotBatchCreateRequest) -> CommonResponse:
        """批量创建票务时段"""
        try:
            created_count = 0
            created_ids = []
            
            for reservation_date in request.reservation_dates:
                for time_slot in request.time_slots:
                    slot_id = str(uuid.uuid4())
                    slot_data = {
                        'id': slot_id,
                        'ticket_id': request.ticket_id,
                        'scenic_id': request.scenic_id,
                        'reservation_date': reservation_date,
                        'start_time': time_slot['start_time'],
                        'end_time': time_slot['end_time'],
                        'total_quota': time_slot['total_quota'],
                        'used_quota': 0,
                        'remaining_quota': time_slot['total_quota']
                    }
                    
                    self.scenic_repo.create_time_slot(slot_data)
                    created_count += 1
                    created_ids.append(slot_id)
            
            return CommonResponse(
                success=True,
                message=f"批量创建成功，共创建 {created_count} 个时段",
                data={'count': created_count, 'ids': created_ids}
            )
        except Exception as e:
            return CommonResponse(
                success=False,
                message=f"批量创建失败：{str(e)}"
            )
    
    def get_time_slots_by_scenic(
        self, 
        scenic_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[TicketTimeSlotResponse]:
        """根据景点ID查询时段"""
        slots = self.scenic_repo.get_time_slots_by_scenic_and_date(
            scenic_id, start_date, end_date
        )
        
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
            for slot in slots
        ]
    
    def update_time_slot(self, slot_id: str, request: TimeSlotUpdateRequest) -> CommonResponse:
        """更新时段"""
        try:
            update_data = {}
            if request.total_quota is not None:
                update_data['total_quota'] = request.total_quota
            if request.used_quota is not None:
                update_data['used_quota'] = request.used_quota
            if request.remaining_quota is not None:
                update_data['remaining_quota'] = request.remaining_quota
            
            if not update_data:
                return CommonResponse(
                    success=False,
                    message="没有需要更新的字段"
                )
            
            rows_affected = self.scenic_repo.update_time_slot(slot_id, update_data)
            
            if rows_affected > 0:
                return CommonResponse(
                    success=True,
                    message="更新成功"
                )
            else:
                return CommonResponse(
                    success=False,
                    message="时段不存在或更新失败"
                )
        except Exception as e:
            return CommonResponse(
                success=False,
                message=f"更新失败：{str(e)}"
            )
    
    def delete_time_slot(self, slot_id: str) -> CommonResponse:
        """删除时段"""
        try:
            rows_affected = self.scenic_repo.delete_time_slot(slot_id)
            
            if rows_affected > 0:
                return CommonResponse(
                    success=True,
                    message="删除成功"
                )
            else:
                return CommonResponse(
                    success=False,
                    message="时段不存在或删除失败"
                )
        except Exception as e:
            return CommonResponse(
                success=False,
                message=f"删除失败：{str(e)}"
            )
    
    def delete_time_slots_by_scenic(self, scenic_id: str) -> CommonResponse:
        """删除景点的所有时段"""
        try:
            rows_affected = self.scenic_repo.delete_time_slots_by_scenic(scenic_id)
            
            return CommonResponse(
                success=True,
                message=f"删除成功，共删除 {rows_affected} 个时段",
                data={'count': rows_affected}
            )
        except Exception as e:
            return CommonResponse(
                success=False,
                message=f"删除失败：{str(e)}"
            )