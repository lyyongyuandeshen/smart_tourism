"""
API 依赖项
"""
from typing import Optional, AsyncGenerator
from fastapi import Depends, HTTPException, status, Header
from app.config.config import config
from app.core.security import decode_access_token
from app.db.session import AsyncSessionAdapter
import aiomysql
import logging

logger = logging.getLogger(__name__)


async def get_db_session() -> AsyncGenerator:
    """
    获取数据库会话（异步生成器）
    
    注意：这里使用aiomysql连接池，返回的是适配器对象
    """
    pool = config.get_aiomysql_pool()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库连接池未初始化"
        )
    
    async with pool.acquire() as conn:
        session = AsyncSessionAdapter(conn)
        try:
            yield session
        finally:
            await session.close()


async def get_current_user_id(authorization: Optional[str] = Header(None)) -> str:
    """
    从请求头中获取当前用户ID
    
    Args:
        authorization: Authorization 请求头
        
    Returns:
        用户ID
        
    Raises:
        HTTPException: 如果token无效或不存在
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="未提供认证信息",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 提取token（格式：Bearer <token>）
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证方案",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证格式",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 解码token获取用户ID
    try:
        payload = decode_access_token(token)
        user_id: Optional[str] = payload.get("uid")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token中缺少用户ID",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id
    except Exception as e:
        logger.error(f"Token解码失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )