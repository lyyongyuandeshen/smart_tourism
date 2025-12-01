from typing import List, Optional, Dict, Any
from mysql.connector import pooling
from app.repository.base_repo import BaseRepository


class MemberLevelRepository(BaseRepository):
    """会员等级数据仓储类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        super().__init__(pool)
    
    def get_member_levels(
        self, 
        level: Optional[int] = None,
        keyword: Optional[str] = None,
        offset: int = 0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        查询会员等级列表（支持多条件查询）
        
        Args:
            level: 会员等级（精确匹配）
            keyword: 关键词（等级名称模糊匹配）
            offset: 偏移量
            limit: 每页数量
            
        Returns:
            会员等级列表
        """
        # 构建动态查询条件
        conditions = ["is_deleted = 0"]  # 只查询未删除的记录
        params = []
        
        if level is not None:
            conditions.append("level = %s")
            params.append(level)
        
        if keyword:
            conditions.append("level_name LIKE %s")
            params.append(f"%{keyword}%")
        
        # 构建WHERE子句
        where_clause = "WHERE " + " AND ".join(conditions)
        
        # 查询语句
        query = f"""
            SELECT id, level, level_name, points_min, points_max,
                   discount_rate, priority_booking, is_deleted,
                   create_time, update_time
            FROM t_member_level
            {where_clause}
            ORDER BY level ASC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        
        return self.execute_query(query, tuple(params))
    
    def count_member_levels(
        self,
        level: Optional[int] = None,
        keyword: Optional[str] = None
    ) -> int:
        """
        统计会员等级总数（支持多条件查询）
        
        Args:
            level: 会员等级
            keyword: 关键词
            
        Returns:
            会员等级总数
        """
        # 构建动态查询条件
        conditions = ["is_deleted = 0"]  # 只统计未删除的记录
        params = []
        
        if level is not None:
            conditions.append("level = %s")
            params.append(level)
        
        if keyword:
            conditions.append("level_name LIKE %s")
            params.append(f"%{keyword}%")
        
        # 构建WHERE子句
        where_clause = "WHERE " + " AND ".join(conditions)
        
        query = f"""
            SELECT COUNT(*) as total
            FROM t_member_level
            {where_clause}
        """
        
        result = self.execute_query(query, tuple(params) if params else None)
        return result[0]['total'] if result else 0
    
    def get_member_level_by_id(self, level_id: str) -> Optional[Dict[str, Any]]:
        """
        根据会员等级ID查询会员等级信息
        
        Args:
            level_id: 会员等级ID
            
        Returns:
            会员等级信息
        """
        query = """
            SELECT id, level, level_name, points_min, points_max,
                   discount_rate, priority_booking, is_deleted,
                   create_time, update_time
            FROM t_member_level
            WHERE id = %s AND is_deleted = 0
        """
        result = self.execute_query(query, (level_id,))
        return result[0] if result else None
    
    def get_member_level_by_level(self, level: int) -> Optional[Dict[str, Any]]:
        """
        根据等级数字查询会员等级信息
        
        Args:
            level: 会员等级（1-10）
            
        Returns:
            会员等级信息
        """
        query = """
            SELECT id, level, level_name, points_min, points_max,
                   discount_rate, priority_booking, is_deleted,
                   create_time, update_time
            FROM t_member_level
            WHERE level = %s AND is_deleted = 0
        """
        result = self.execute_query(query, (level,))
        return result[0] if result else None
    
    def create_member_level(self, level_data: Dict[str, Any]) -> int:
        """
        创建会员等级信息
        
        Args:
            level_data: 会员等级数据
            
        Returns:
            影响的行数
        """
        query = """
            INSERT INTO t_member_level 
            (level, level_name, points_min, points_max, 
             discount_rate, priority_booking)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (
            level_data['level'],
            level_data['level_name'],
            level_data['points_min'],
            level_data['points_max'],
            level_data['discount_rate'],
            level_data['priority_booking']
        )
        return self.execute_insert(query, params)
    
    def update_member_level(self, level_id: str, level_data: Dict[str, Any]) -> int:
        """
        更新会员等级信息
        
        Args:
            level_id: 会员等级ID
            level_data: 会员等级数据
            
        Returns:
            影响的行数
        """
        # 构建动态更新字段
        update_fields = []
        params = []
        
        if 'level_name' in level_data:
            update_fields.append("level_name = %s")
            params.append(level_data['level_name'])
        
        if 'points_min' in level_data:
            update_fields.append("points_min = %s")
            params.append(level_data['points_min'])
        
        if 'points_max' in level_data:
            update_fields.append("points_max = %s")
            params.append(level_data['points_max'])
        
        if 'discount_rate' in level_data:
            update_fields.append("discount_rate = %s")
            params.append(level_data['discount_rate'])
        
        if 'priority_booking' in level_data:
            update_fields.append("priority_booking = %s")
            params.append(level_data['priority_booking'])
        
        if not update_fields:
            return 0
        
        update_fields.append("update_time = NOW()")
        params.append(level_id)
        
        query = f"""
            UPDATE t_member_level
            SET {', '.join(update_fields)}
            WHERE id = %s AND is_deleted = 0
        """
        
        return self.execute_update(query, tuple(params))
    
    def soft_delete_member_level(self, level_id: str) -> int:
        """
        软删除会员等级信息
        
        Args:
            level_id: 会员等级ID
            
        Returns:
            影响的行数
        """
        query = """
            UPDATE t_member_level
            SET is_deleted = 1,
                update_time = NOW()
            WHERE id = %s AND is_deleted = 0
        """
        return self.execute_update(query, (level_id,))
