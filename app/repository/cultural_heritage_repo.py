from typing import List, Optional, Dict, Any
from mysql.connector import pooling
from app.repository.base_repo import BaseRepository


class CulturalHeritageRepository(BaseRepository):
    """文化遗产数据仓储类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        super().__init__(pool)
    
    def get_cultural_heritages(
        self, 
        file_id: Optional[str] = None,
        file_name: Optional[str] = None,
        file_type: Optional[str] = None,
        tag: Optional[str] = None,
        offset: int = 0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        查询文化遗产列表（支持多条件查询）
        
        Args:
            file_id: 文件编号（精确匹配）
            file_name: 文件名称（模糊匹配）
            file_type: 文件类型（精确匹配）
            tag: 所属标签（精确匹配）
            offset: 偏移量
            limit: 每页数量
            
        Returns:
            文化遗产列表
        """
        # 构建动态查询条件
        conditions = []
        params = []
        
        if file_id:
            conditions.append("file_id = %s")
            params.append(file_id)
        
        if file_name:
            conditions.append("file_name LIKE %s")
            params.append(f"%{file_name}%")
        
        if file_type:
            conditions.append("file_type = %s")
            params.append(file_type)
        
        if tag:
            conditions.append("tag = %s")
            params.append(tag)
        
        # 构建WHERE子句
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
        
        # 查询语句
        query = f"""
            SELECT file_id, file_name, file_type, tag, url, 
                   created_at, updated_at
            FROM t_cultural_heritage
            {where_clause}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        
        return self.execute_query(query, tuple(params))
    
    def count_cultural_heritages(
        self,
        file_id: Optional[str] = None,
        file_name: Optional[str] = None,
        file_type: Optional[str] = None,
        tag: Optional[str] = None
    ) -> int:
        """
        统计文化遗产总数（支持多条件查询）
        
        Args:
            file_id: 文件编号
            file_name: 文件名称
            file_type: 文件类型
            tag: 所属标签
            
        Returns:
            文化遗产总数
        """
        # 构建动态查询条件
        conditions = []
        params = []
        
        if file_id:
            conditions.append("file_id = %s")
            params.append(file_id)
        
        if file_name:
            conditions.append("file_name LIKE %s")
            params.append(f"%{file_name}%")
        
        if file_type:
            conditions.append("file_type = %s")
            params.append(file_type)
        
        if tag:
            conditions.append("tag = %s")
            params.append(tag)
        
        # 构建WHERE子句
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
        
        query = f"""
            SELECT COUNT(*) as total
            FROM t_cultural_heritage
            {where_clause}
        """
        
        result = self.execute_query(query, tuple(params) if params else None)
        return result[0]['total'] if result else 0
    
    def get_cultural_heritage_by_id(self, file_id: str) -> Optional[Dict[str, Any]]:
        """
        根据文件ID查询文化遗产信息
        
        Args:
            file_id: 文件ID
            
        Returns:
            文化遗产信息
        """
        query = """
            SELECT file_id, file_name, file_type, tag, url,
                   created_at, updated_at
            FROM t_cultural_heritage
            WHERE file_id = %s
        """
        result = self.execute_query(query, (file_id,))
        return result[0] if result else None
    
    def create_cultural_heritage(self, heritage_data: Dict[str, Any]) -> int:
        """
        创建文化遗产信息
        
        Args:
            heritage_data: 文化遗产数据
            
        Returns:
            影响的行数
        """
        query = """
            INSERT INTO t_cultural_heritage 
            (file_id, file_name, file_type, tag, url)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            heritage_data['file_id'],
            heritage_data['file_name'],
            heritage_data['file_type'],
            heritage_data['tag'],
            heritage_data['url']
        )
        return self.execute_insert(query, params)
    
    def update_cultural_heritage(self, file_id: str, heritage_data: Dict[str, Any]) -> int:
        """
        更新文化遗产信息
        
        Args:
            file_id: 文件ID
            heritage_data: 文化遗产数据
            
        Returns:
            影响的行数
        """
        query = """
            UPDATE t_cultural_heritage
            SET file_name = %s,
                file_type = %s,
                tag = %s,
                url = %s,
                updated_at = NOW()
            WHERE file_id = %s
        """
        params = (
            heritage_data['file_name'],
            heritage_data['file_type'],
            heritage_data['tag'],
            heritage_data['url'],
            file_id
        )
        return self.execute_update(query, params)
    
    def delete_cultural_heritage(self, file_id: str) -> int:
        """
        删除文化遗产信息
        
        Args:
            file_id: 文件ID
            
        Returns:
            影响的行数
        """
        query = "DELETE FROM t_cultural_heritage WHERE file_id = %s"
        return self.execute_update(query, (file_id,))
