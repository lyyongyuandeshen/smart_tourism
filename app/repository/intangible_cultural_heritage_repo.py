from typing import List, Optional, Dict, Any
from mysql.connector import pooling
from app.repository.base_repo import BaseRepository


class IntangibleCulturalHeritageRepository(BaseRepository):
    """非遗技艺数据仓储类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        super().__init__(pool)
    
    def get_intangible_cultural_heritages(
        self, 
        heritage_number: Optional[str] = None,
        heritage_name: Optional[str] = None,
        interactive_question_bank: Optional[str] = None,
        is_published: Optional[bool] = None,
        offset: int = 0,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        查询非遗技艺列表（支持多条件查询）
        
        Args:
            heritage_number: 非遗编号（精确匹配）
            heritage_name: 非遗名称（模糊匹配）
            interactive_question_bank: 互动题库（精确匹配）
            is_published: 是否发布（精确匹配）
            offset: 偏移量
            limit: 每页数量
            
        Returns:
            非遗技艺列表
        """
        # 构建动态查询条件
        conditions = []
        params = []
        
        if heritage_number:
            conditions.append("heritage_number = %s")
            params.append(heritage_number)
        
        if heritage_name:
            conditions.append("heritage_name LIKE %s")
            params.append(f"%{heritage_name}%")
        
        if interactive_question_bank:
            conditions.append("interactive_question_bank = %s")
            params.append(interactive_question_bank)
        
        if is_published is not None:
            conditions.append("is_published = %s")
            params.append(is_published)
        
        # 构建WHERE子句
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
        
        # 查询语句
        query = f"""
            SELECT id, heritage_number, heritage_name, interactive_question_bank, 
                   video_url, is_published, created_at, updated_at
            FROM t_intangible_cultural_heritage
            {where_clause}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        
        return self.execute_query(query, tuple(params))
    
    def count_intangible_cultural_heritages(
        self,
        heritage_number: Optional[str] = None,
        heritage_name: Optional[str] = None,
        interactive_question_bank: Optional[str] = None,
        is_published: Optional[bool] = None
    ) -> int:
        """
        统计非遗技艺总数（支持多条件查询）
        
        Args:
            heritage_number: 非遗编号
            heritage_name: 非遗名称
            interactive_question_bank: 互动题库
            is_published: 是否发布
            
        Returns:
            非遗技艺总数
        """
        # 构建动态查询条件
        conditions = []
        params = []
        
        if heritage_number:
            conditions.append("heritage_number = %s")
            params.append(heritage_number)
        
        if heritage_name:
            conditions.append("heritage_name LIKE %s")
            params.append(f"%{heritage_name}%")
        
        if interactive_question_bank:
            conditions.append("interactive_question_bank = %s")
            params.append(interactive_question_bank)
        
        if is_published is not None:
            conditions.append("is_published = %s")
            params.append(is_published)
        
        # 构建WHERE子句
        where_clause = ""
        if conditions:
            where_clause = "WHERE " + " AND ".join(conditions)
        
        query = f"""
            SELECT COUNT(*) as total
            FROM t_intangible_cultural_heritage
            {where_clause}
        """
        
        result = self.execute_query(query, tuple(params) if params else None)
        return result[0]['total'] if result else 0
    
    def get_intangible_cultural_heritage_by_number(self, heritage_number: str) -> Optional[Dict[str, Any]]:
        """
        根据非遗编号查询非遗技艺信息
        
        Args:
            heritage_number: 非遗编号
            
        Returns:
            非遗技艺信息
        """
        query = """
            SELECT id, heritage_number, heritage_name, interactive_question_bank, 
                   video_url, is_published, created_at, updated_at
            FROM t_intangible_cultural_heritage
            WHERE heritage_number = %s
        """
        result = self.execute_query(query, (heritage_number,))
        return result[0] if result else None
    
    def get_intangible_cultural_heritage_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """
        根据ID查询非遗技艺信息
        
        Args:
            id: 主键ID
            
        Returns:
            非遗技艺信息
        """
        query = """
            SELECT id, heritage_number, heritage_name, interactive_question_bank, 
                   video_url, is_published, created_at, updated_at
            FROM t_intangible_cultural_heritage
            WHERE id = %s
        """
        result = self.execute_query(query, (id,))
        return result[0] if result else None
    
    def create_intangible_cultural_heritage(self, heritage_data: Dict[str, Any]) -> int:
        """
        创建非遗技艺信息
        
        Args:
            heritage_data: 非遗技艺数据
            
        Returns:
            影响的行数
        """
        query = """
            INSERT INTO t_intangible_cultural_heritage 
            (heritage_number, heritage_name, interactive_question_bank, video_url, is_published)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (
            heritage_data['heritage_number'],
            heritage_data['heritage_name'],
            heritage_data['interactive_question_bank'],
            heritage_data['video_url'],
            heritage_data.get('is_published', False)
        )
        return self.execute_insert(query, params)
    
    def update_intangible_cultural_heritage(self, heritage_number: str, heritage_data: Dict[str, Any]) -> int:
        """
        更新非遗技艺信息
        
        Args:
            heritage_number: 非遗编号
            heritage_data: 非遗技艺数据
            
        Returns:
            影响的行数
        """
        # 构建动态SET子句
        set_clauses = []
        params = []
        
        if 'heritage_name' in heritage_data:
            set_clauses.append("heritage_name = %s")
            params.append(heritage_data['heritage_name'])
        
        if 'interactive_question_bank' in heritage_data:
            set_clauses.append("interactive_question_bank = %s")
            params.append(heritage_data['interactive_question_bank'])
        
        if 'is_published' in heritage_data:
            set_clauses.append("is_published = %s")
            params.append(heritage_data['is_published'])
        
        # 如果没有要更新的字段，直接返回0
        if not set_clauses:
            return 0
        
        # 添加updated_at字段
        set_clauses.append("updated_at = NOW()")
        
        # 构建完整的查询语句
        query = f"""
            UPDATE t_intangible_cultural_heritage
            SET {', '.join(set_clauses)}
            WHERE heritage_number = %s
        """
        params.append(heritage_number)
        
        return self.execute_update(query, tuple(params))
    
    def delete_intangible_cultural_heritage(self, heritage_number: str) -> int:
        """
        删除非遗技艺信息
        
        Args:
            heritage_number: 非遗编号
            
        Returns:
            影响的行数
        """
        query = "DELETE FROM t_intangible_cultural_heritage WHERE heritage_number = %s"
        return self.execute_update(query, (heritage_number,))
    
    def get_max_heritage_number(self) -> Optional[str]:
        """
        获取最大的非遗编号，用于生成新编号
        
        Returns:
            最大的非遗编号
        """
        query = """
            SELECT heritage_number 
            FROM t_intangible_cultural_heritage 
            ORDER BY id DESC 
            LIMIT 1
        """
        result = self.execute_query(query)
        return result[0]['heritage_number'] if result else None