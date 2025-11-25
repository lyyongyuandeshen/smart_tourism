from typing import List, Optional, Dict, Any
from datetime import date
from mysql.connector import pooling
from app.repository.base_repo import BaseRepository


class ScenicRepository(BaseRepository):
    """景点导览数据仓储类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        super().__init__(pool)
    
    # ========== 景点导览相关操作 ==========
    
    def create_scenic_guide(self, guide_data: Dict[str, Any]) -> int:
        """创建景点导览"""
        query = """
            INSERT INTO t_scenic_guide 
            (id, scenic_id, guide_title, historical_background, cultural_value,
             architectural_features, historical_stories, ecological_science,
             open_status, last_bus_time, evacuation_route_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            guide_data['id'],
            guide_data['scenic_id'],
            guide_data['guide_title'],
            guide_data.get('historical_background'),
            guide_data.get('cultural_value'),
            guide_data.get('architectural_features'),
            guide_data.get('historical_stories'),
            guide_data.get('ecological_science'),
            guide_data.get('open_status', 1),
            guide_data.get('last_bus_time'),
            guide_data.get('evacuation_route_url')
        )
        return self.execute_insert(query, params)
    
    def get_scenic_guide_by_id(self, guide_id: str) -> Optional[Dict[str, Any]]:
        """根据ID查询景点导览"""
        query = """
            SELECT id, scenic_id, guide_title, historical_background, cultural_value,
                   architectural_features, historical_stories, ecological_science,
                   open_status, last_bus_time, evacuation_route_url,
                   create_time, update_time
            FROM t_scenic_guide
            WHERE id = %s
        """
        result = self.execute_query(query, (guide_id,))
        return result[0] if result else None
    
    def get_scenic_guide_by_scenic_id(self, scenic_id: str) -> Optional[Dict[str, Any]]:
        """根据景点ID查询景点导览"""
        query = """
            SELECT id, scenic_id, guide_title, historical_background, cultural_value,
                   architectural_features, historical_stories, ecological_science,
                   open_status, last_bus_time, evacuation_route_url,
                   create_time, update_time
            FROM t_scenic_guide
            WHERE scenic_id = %s
        """
        result = self.execute_query(query, (scenic_id,))
        return result[0] if result else None
    
    def get_all_scenic_guides(self, open_status: Optional[int] = None) -> List[Dict[str, Any]]:
        """查询所有景点导览"""
        if open_status is not None:
            query = """
                SELECT id, scenic_id, guide_title, historical_background, cultural_value,
                       architectural_features, historical_stories, ecological_science,
                       open_status, last_bus_time, evacuation_route_url,
                       create_time, update_time
                FROM t_scenic_guide
                WHERE open_status = %s
                ORDER BY create_time DESC
            """
            return self.execute_query(query, (open_status,))
        else:
            query = """
                SELECT id, scenic_id, guide_title, historical_background, cultural_value,
                       architectural_features, historical_stories, ecological_science,
                       open_status, last_bus_time, evacuation_route_url,
                       create_time, update_time
                FROM t_scenic_guide
                ORDER BY create_time DESC
            """
            return self.execute_query(query)
    
    def update_scenic_guide(self, guide_id: str, update_data: Dict[str, Any]) -> int:
        """更新景点导览"""
        # 构建动态更新语句
        update_fields = []
        params = []
        
        field_mapping = {
            'guide_title': 'guide_title',
            'historical_background': 'historical_background',
            'cultural_value': 'cultural_value',
            'architectural_features': 'architectural_features',
            'historical_stories': 'historical_stories',
            'ecological_science': 'ecological_science',
            'open_status': 'open_status',
            'last_bus_time': 'last_bus_time',
            'evacuation_route_url': 'evacuation_route_url'
        }
        
        for key, db_field in field_mapping.items():
            if key in update_data and update_data[key] is not None:
                update_fields.append(f"{db_field} = %s")
                params.append(update_data[key])
        
        if not update_fields:
            return 0
        
        update_fields.append("update_time = NOW()")
        params.append(guide_id)
        
        query = f"""
            UPDATE t_scenic_guide
            SET {', '.join(update_fields)}
            WHERE id = %s
        """
        return self.execute_update(query, tuple(params))
    
    def delete_scenic_guide(self, guide_id: str) -> int:
        """删除景点导览"""
        query = "DELETE FROM t_scenic_guide WHERE id = %s"
        return self.execute_update(query, (guide_id,))
    
    # ========== 时段管理相关操作 ==========
    
    def create_time_slot(self, slot_data: Dict[str, Any]) -> int:
        """创建时段"""
        query = """
            INSERT INTO t_ticket_time_slot 
            (id, ticket_id, scenic_id, reservation_date, start_time, end_time,
             total_quota, used_quota, remaining_quota)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            slot_data['id'],
            slot_data['ticket_id'],
            slot_data['scenic_id'],
            slot_data['reservation_date'],
            slot_data['start_time'],
            slot_data['end_time'],
            slot_data['total_quota'],
            slot_data.get('used_quota', 0),
            slot_data.get('remaining_quota', slot_data['total_quota'])
        )
        return self.execute_insert(query, params)
    
    def get_time_slots_by_scenic_and_date(
        self, 
        scenic_id: str, 
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """根据景点ID和日期范围查询时段"""
        if start_date and end_date:
            query = """
                SELECT id, ticket_id, scenic_id, reservation_date, start_time, end_time,
                       total_quota, used_quota, remaining_quota, create_time, update_time
                FROM t_ticket_time_slot
                WHERE scenic_id = %s AND reservation_date BETWEEN %s AND %s
                ORDER BY reservation_date, start_time
            """
            return self.execute_query(query, (scenic_id, start_date, end_date))
        else:
            query = """
                SELECT id, ticket_id, scenic_id, reservation_date, start_time, end_time,
                       total_quota, used_quota, remaining_quota, create_time, update_time
                FROM t_ticket_time_slot
                WHERE scenic_id = %s
                ORDER BY reservation_date, start_time
            """
            return self.execute_query(query, (scenic_id,))
    
    def update_time_slot(self, slot_id: str, update_data: Dict[str, Any]) -> int:
        """更新时段信息"""
        update_fields = []
        params = []
        
        if 'total_quota' in update_data and update_data['total_quota'] is not None:
            update_fields.append("total_quota = %s")
            params.append(update_data['total_quota'])
        
        if 'used_quota' in update_data and update_data['used_quota'] is not None:
            update_fields.append("used_quota = %s")
            params.append(update_data['used_quota'])
        
        if 'remaining_quota' in update_data and update_data['remaining_quota'] is not None:
            update_fields.append("remaining_quota = %s")
            params.append(update_data['remaining_quota'])
        
        if not update_fields:
            return 0
        
        update_fields.append("update_time = NOW()")
        params.append(slot_id)
        
        query = f"""
            UPDATE t_ticket_time_slot
            SET {', '.join(update_fields)}
            WHERE id = %s
        """
        return self.execute_update(query, tuple(params))
    
    def delete_time_slot(self, slot_id: str) -> int:
        """删除时段"""
        query = "DELETE FROM t_ticket_time_slot WHERE id = %s"
        return self.execute_update(query, (slot_id,))
    
    def delete_time_slots_by_scenic(self, scenic_id: str) -> int:
        """删除景点的所有时段"""
        query = "DELETE FROM t_ticket_time_slot WHERE scenic_id = %s"
        return self.execute_update(query, (scenic_id,))
