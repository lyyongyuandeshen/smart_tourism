from typing import List, Optional, Dict, Any
from datetime import date
from mysql.connector import pooling
from app.repository.base_repo import BaseRepository


class ScheduleRepository(BaseRepository):
    """排班数据仓储类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        super().__init__(pool)
    
    # ==================== 员工相关 ====================
    
    def get_all_employees(self) -> List[Dict[str, Any]]:
        """获取所有员工列表"""
        query = """
            SELECT employee_id, name, employee_code, phone, created_at
            FROM t_scenic_employee
            ORDER BY employee_id
        """
        return self.execute_query(query)
    
    def get_employee_by_id(self, employee_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取员工信息"""
        query = """
            SELECT employee_id, name, employee_code, phone, created_at
            FROM t_scenic_employee
            WHERE employee_id = %s
        """
        result = self.execute_query(query, (employee_id,))
        return result[0] if result else None
    
    # ==================== 岗位相关 ====================
    
    def get_all_positions(self) -> List[Dict[str, Any]]:
        """获取所有岗位列表"""
        query = """
            SELECT position_id, position_name, description, created_at
            FROM t_scenic_position
            ORDER BY position_id
        """
        return self.execute_query(query)
    
    def get_position_by_id(self, position_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取岗位信息"""
        query = """
            SELECT position_id, position_name, description, created_at
            FROM t_scenic_position
            WHERE position_id = %s
        """
        result = self.execute_query(query, (position_id,))
        return result[0] if result else None
    
    # ==================== 班次相关 ====================
    
    def get_all_shifts(self) -> List[Dict[str, Any]]:
        """获取所有班次列表"""
        query = """
            SELECT s.shift_id, s.shift_name, s.start_time, s.end_time, 
                   s.position_id, p.position_name, s.created_at
            FROM t_scenic_shift s
            LEFT JOIN t_scenic_position p ON s.position_id = p.position_id
            ORDER BY s.shift_id
        """
        return self.execute_query(query)
    
    def get_shift_by_id(self, shift_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取班次信息"""
        query = """
            SELECT s.shift_id, s.shift_name, s.start_time, s.end_time, 
                   s.position_id, p.position_name, s.created_at
            FROM t_scenic_shift s
            LEFT JOIN t_scenic_position p ON s.position_id = p.position_id
            WHERE s.shift_id = %s
        """
        result = self.execute_query(query, (shift_id,))
        return result[0] if result else None
    
    # ==================== 排班记录相关 ====================
    
    def create_schedule(self, schedule_data: Dict[str, Any]) -> int:
        """创建排班记录"""
        query = """
            INSERT INTO t_scenic_schedule 
            (schedule_date, shift_id, position_id)
            VALUES (%s, %s, %s)
        """
        params = (
            schedule_data['schedule_date'],
            schedule_data['shift_id'],
            schedule_data['position_id']
        )
        return self.execute_insert(query, params)
    
    def add_schedule_employee(self, schedule_id: int, employee_id: int, is_leader: bool = False) -> int:
        """添加排班员工关联"""
        query = """
            INSERT INTO t_scenic_schedule_employee 
            (schedule_id, employee_id, is_leader)
            VALUES (%s, %s, %s)
        """
        return self.execute_insert(query, (schedule_id, employee_id, is_leader))
    
    def get_schedules_by_date_range(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        position_id: Optional[int] = None,
        employee_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        根据日期范围查询排班记录
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            position_id: 岗位ID
            employee_id: 员工ID
            
        Returns:
            排班记录列表
        """
        conditions = []
        params = []
        
        if start_date:
            conditions.append("sc.schedule_date >= %s")
            params.append(start_date)
        
        if end_date:
            conditions.append("sc.schedule_date <= %s")
            params.append(end_date)
        
        if position_id:
            conditions.append("sc.position_id = %s")
            params.append(position_id)
        
        if employee_id:
            conditions.append("se.employee_id = %s")
            params.append(employee_id)
        
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
        
        query = f"""
            SELECT DISTINCT sc.schedule_id, sc.schedule_date, sc.shift_id, 
                   sh.shift_name, sh.start_time, sh.end_time,
                   sc.position_id, p.position_name, sc.created_at
            FROM t_scenic_schedule sc
            INNER JOIN t_scenic_shift sh ON sc.shift_id = sh.shift_id
            INNER JOIN t_scenic_position p ON sc.position_id = p.position_id
            LEFT JOIN t_scenic_schedule_employee se ON sc.schedule_id = se.schedule_id
            {where_clause}
            ORDER BY sc.schedule_date, sc.schedule_id
        """
        
        return self.execute_query(query, tuple(params) if params else None)
    
    def get_schedule_employees(self, schedule_id: int) -> List[Dict[str, Any]]:
        """获取排班的员工列表"""
        query = """
            SELECT se.schedule_employee_id, se.schedule_id, 
                   se.employee_id, e.name as employee_name, 
                   e.employee_code, se.is_leader
            FROM t_scenic_schedule_employee se
            INNER JOIN t_scenic_employee e ON se.employee_id = e.employee_id
            WHERE se.schedule_id = %s
            ORDER BY se.is_leader DESC, se.employee_id
        """
        return self.execute_query(query, (schedule_id,))
    
    def get_schedule_by_id(self, schedule_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取排班详情"""
        query = """
            SELECT sc.schedule_id, sc.schedule_date, sc.shift_id, 
                   sh.shift_name, sh.start_time, sh.end_time,
                   sc.position_id, p.position_name, sc.created_at
            FROM t_scenic_schedule sc
            INNER JOIN t_scenic_shift sh ON sc.shift_id = sh.shift_id
            INNER JOIN t_scenic_position p ON sc.position_id = p.position_id
            WHERE sc.schedule_id = %s
        """
        result = self.execute_query(query, (schedule_id,))
        return result[0] if result else None
    
    def delete_schedule(self, schedule_id: int) -> int:
        """删除排班记录"""
        # 先删除员工关联
        self.execute_update(
            "DELETE FROM t_scenic_schedule_employee WHERE schedule_id = %s",
            (schedule_id,)
        )
        # 再删除排班记录
        return self.execute_update(
            "DELETE FROM t_scenic_schedule WHERE schedule_id = %s",
            (schedule_id,)
        )
    
    def update_schedule(self, schedule_id: int, schedule_data: Dict[str, Any]) -> int:
        """更新排班记录"""
        query = """
            UPDATE t_scenic_schedule
            SET schedule_date = %s,
                shift_id = %s,
                position_id = %s
            WHERE schedule_id = %s
        """
        params = (
            schedule_data['schedule_date'],
            schedule_data['shift_id'],
            schedule_data['position_id'],
            schedule_id
        )
        return self.execute_update(query, params)
    
    def delete_schedule_employees(self, schedule_id: int) -> int:
        """删除排班的所有员工关联"""
        query = "DELETE FROM t_scenic_schedule_employee WHERE schedule_id = %s"
        return self.execute_update(query, (schedule_id,))
    
    def search_schedules_by_keyword(
        self,
        keyword: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None
    ) -> List[Dict[str, Any]]:
        """
        根据关键词搜索排班（搜索员工姓名、岗位名称）
        
        Args:
            keyword: 搜索关键词
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            排班记录列表
        """
        conditions = ["(e.name LIKE %s OR p.position_name LIKE %s)"]
        params = [f"%{keyword}%", f"%{keyword}%"]
        
        if start_date:
            conditions.append("sc.schedule_date >= %s")
            params.append(start_date)
        
        if end_date:
            conditions.append("sc.schedule_date <= %s")
            params.append(end_date)
        
        where_clause = "WHERE " + " AND ".join(conditions)
        
        query = f"""
            SELECT DISTINCT sc.schedule_id, sc.schedule_date, sc.shift_id, 
                   sh.shift_name, sh.start_time, sh.end_time,
                   sc.position_id, p.position_name, sc.created_at
            FROM t_scenic_schedule sc
            INNER JOIN t_scenic_shift sh ON sc.shift_id = sh.shift_id
            INNER JOIN t_scenic_position p ON sc.position_id = p.position_id
            LEFT JOIN t_scenic_schedule_employee se ON sc.schedule_id = se.schedule_id
            LEFT JOIN t_scenic_employee e ON se.employee_id = e.employee_id
            {where_clause}
            ORDER BY sc.schedule_date, sc.schedule_id
        """
        
        return self.execute_query(query, tuple(params))
    
    def check_schedule_exists(
        self,
        schedule_date: date,
        position_id: int,
        exclude_schedule_id: Optional[int] = None
    ) -> bool:
        """
        检查指定日期和岗位是否已有排班
        
        Args:
            schedule_date: 排班日期
            position_id: 岗位ID
            exclude_schedule_id: 排除的排班ID（用于更新时）
            
        Returns:
            是否存在
        """
        query = """
            SELECT COUNT(*) as count
            FROM t_scenic_schedule
            WHERE schedule_date = %s AND position_id = %s
        """
        params = [schedule_date, position_id]
        
        if exclude_schedule_id:
            query += " AND schedule_id != %s"
            params.append(exclude_schedule_id)
        
        result = self.execute_query(query, tuple(params))
        return result[0]['count'] > 0 if result else False
