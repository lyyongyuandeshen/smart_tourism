"""
数据库会话适配器
将aiomysql连接包装成类似AsyncSession的接口
"""
import aiomysql
from typing import Any, Dict, List
import logging

logger = logging.getLogger(__name__)


class AsyncSessionAdapter:
    """异步会话适配器，将aiomysql连接包装成类似SQLAlchemy AsyncSession的接口"""
    
    def __init__(self, conn: aiomysql.Connection):
        self.conn = conn
        self._cursor = None
    
    async def execute(self, query, params=None):
        """执行SQL查询"""
        if self._cursor is None:
            self._cursor = await self.conn.cursor(aiomysql.DictCursor)
        
        # 处理sqlalchemy的text()对象
        if hasattr(query, 'text'):
            query_str = str(query)
        else:
            query_str = str(query)
        
        # 转换参数格式（从:name到%(name)s）
        if params:
            # 将:param格式转换为%(param)s格式
            for key, value in params.items():
                query_str = query_str.replace(f':{key}', f'%({key})s')
        
        await self._cursor.execute(query_str, params or {})
        return self
    
    async def commit(self):
        """提交事务"""
        await self.conn.commit()
    
    async def close(self):
        """关闭会话"""
        if self._cursor:
            await self._cursor.close()
    
    def mappings(self):
        """返回self以支持链式调用"""
        return self
    
    async def first(self):
        """获取第一行结果"""
        if self._cursor:
            row = await self._cursor.fetchone()
            return row
        return None
    
    async def all(self):
        """获取所有结果"""
        if self._cursor:
            rows = await self._cursor.fetchall()
            return rows
        return []
    
    def scalar(self):
        """获取标量值（用于COUNT等）"""
        # 这个方法需要在调用first()后使用
        return self._last_scalar
    
    async def fetchone(self):
        """获取一行"""
        if self._cursor:
            return await self._cursor.fetchone()
        return None
    
    async def fetchall(self):
        """获取所有行"""
        if self._cursor:
            return await self._cursor.fetchall()
        return []


def text(query_str: str):
    """模拟SQLAlchemy的text()函数"""
    return query_str


def get_session_factory():
    """
    获取会话工厂函数
    返回一个可以创建AsyncSessionAdapter的工厂
    """
    from app.config.config import config
    
    class SessionFactory:
        def __call__(self):
            """返回一个异步上下文管理器"""
            pool = config.get_aiomysql_pool()
            
            class AsyncContextManager:
                async def __aenter__(self):
                    self.conn = await pool.acquire()
                    self.session = AsyncSessionAdapter(self.conn)
                    return self.session
                
                async def __aexit__(self, exc_type, exc_val, exc_tb):
                    await self.session.close()
                    pool.release(self.conn)
            
            return AsyncContextManager()
    
    return SessionFactory()
