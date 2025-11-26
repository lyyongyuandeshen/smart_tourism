from typing import List, Optional, Dict, Any
from mysql.connector import pooling
from app.repository.base_repo import BaseRepository


class FacilityRepository(BaseRepository):
    """景区设备数据仓储类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        super().__init__(pool)
    
    def get_facilities(
        self, 
        facility_id: Optional[str] = None,
        facility_name: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None,
        offset: int = 0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        查询设备列表（支持多条件查询）
        
        Args:
            facility_id: 设备编号（精确匹配）
            facility_name: 设备名称（模糊匹配）
            category: 设备分类（精确匹配）
            status: 设备状态（精确匹配）
            offset: 偏移量
            limit: 每页数量
            
        Returns:
            设备列表
        """
        # 构建动态查询条件
        conditions = []
        params = []
        
        if facility_id:
            conditions.append("facility_id = %s")
            params.append(facility_id)
        
        if facility_name:
            conditions.append("facility_name LIKE %s")
            params.append(f"%{facility_name}%")
        
        if category:
            conditions.append("category = %s")
            params.append(category)
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        # 构建WHERE子句
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
        
        # 查询语句
        query = f"""
            SELECT facility_id, facility_name, category, icon, position_desc,
                   longitude, latitude, status, created_at, updated_at
            FROM t_scenic_facility
            {where_clause}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        
        return self.execute_query(query, tuple(params))
    
    def count_facilities(
        self,
        facility_id: Optional[str] = None,
        facility_name: Optional[str] = None,
        category: Optional[str] = None,
        status: Optional[str] = None
    ) -> int:
        """
        统计设备总数（支持多条件查询）
        
        Args:
            facility_id: 设备编号
            facility_name: 设备名称
            category: 设备分类
            status: 设备状态
            
        Returns:
            设备总数
        """
        # 构建动态查询条件
        conditions = []
        params = []
        
        if facility_id:
            conditions.append("facility_id = %s")
            params.append(facility_id)
        
        if facility_name:
            conditions.append("facility_name LIKE %s")
            params.append(f"%{facility_name}%")
        
        if category:
            conditions.append("category = %s")
            params.append(category)
        
        if status:
            conditions.append("status = %s")
            params.append(status)
        
        # 构建WHERE子句
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
        
        query = f"""
            SELECT COUNT(*) as total
            FROM t_scenic_facility
            {where_clause}
        """
        
        result = self.execute_query(query, tuple(params) if params else None)
        return result[0]['total'] if result else 0
    
    def get_facility_by_id(self, facility_id: str) -> Optional[Dict[str, Any]]:
        """
        根据设备ID查询设备信息
        
        Args:
            facility_id: 设备ID
            
        Returns:
            设备信息
        """
        query = """
            SELECT facility_id, facility_name, category, icon, position_desc,
                   longitude, latitude, status, created_at, updated_at
            FROM t_scenic_facility
            WHERE facility_id = %s
        """
        result = self.execute_query(query, (facility_id,))
        return result[0] if result else None
    
    def create_facility(self, facility_data: Dict[str, Any]) -> int:
        """
        创建设备信息
        
        Args:
            facility_data: 设备数据
            
        Returns:
            影响的行数
        """
        query = """
            INSERT INTO t_scenic_facility 
            (facility_id, facility_name, category, icon, position_desc, 
             longitude, latitude, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            facility_data['facility_id'],
            facility_data['facility_name'],
            facility_data['category'],
            facility_data.get('icon'),
            facility_data['position_desc'],
            facility_data.get('longitude'),
            facility_data.get('latitude'),
            facility_data['status']
        )
        return self.execute_insert(query, params)
    
    def update_facility(self, facility_id: str, facility_data: Dict[str, Any]) -> int:
        """
        更新设备信息
        
        Args:
            facility_id: 设备ID
            facility_data: 设备数据
            
        Returns:
            影响的行数
        """
        query = """
            UPDATE t_scenic_facility
            SET facility_name = %s,
                category = %s,
                icon = %s,
                position_desc = %s,
                longitude = %s,
                latitude = %s,
                status = %s,
                updated_at = NOW()
            WHERE facility_id = %s
        """
        params = (
            facility_data['facility_name'],
            facility_data['category'],
            facility_data.get('icon'),
            facility_data['position_desc'],
            facility_data.get('longitude'),
            facility_data.get('latitude'),
            facility_data['status'],
            facility_id
        )
        return self.execute_update(query, params)
    
    def delete_facility(self, facility_id: str) -> int:
        """
        删除设备信息
        
        Args:
            facility_id: 设备ID
            
        Returns:
            影响的行数
        """
        query = "DELETE FROM t_scenic_facility WHERE facility_id = %s"
        return self.execute_update(query, (facility_id,))
