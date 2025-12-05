from mysql.connector import pooling
from mysql.connector.pooling import PooledMySQLConnection
from typing import Optional, List, Dict, Any


class BaseRepository:
    """基础仓储类"""
    
    def __init__(self, pool: pooling.MySQLConnectionPool):
        self.pool = pool
    
    def get_connection(self) -> PooledMySQLConnection:
        """获取数据库连接"""
        return self.pool.get_connection()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        """执行查询并返回结果"""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def execute_update(self, query: str, params: tuple = None) -> int:
        """执行更新操作并返回影响的行数"""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def execute_insert(self, query: str, params: tuple = None) -> int:
        """执行插入操作并返回影响的行数"""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            # 对于非自增主键表，返回影响的行数更有意义
            return cursor.rowcount
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()

    def execute_insert_with_id(self, query: str, params: tuple = None) -> int:
        """执行插入操作并返回最后插入的自增ID（仅用于自增主键表）"""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute(query, params or ())
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()