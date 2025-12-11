from typing import Optional, Tuple
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ProxyConfig
from app.db.session import get_session_factory


async def get_proxy_config(config_name: str = "default") -> Optional[ProxyConfig]:
    """
    从数据库获取代理配置
    
    Args:
        config_name: 配置名称，默认为 "default"
    
    Returns:
        ProxyConfig 对象，如果不存在则返回 None
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        stmt = select(ProxyConfig).where(
            ProxyConfig.name == config_name,
            ProxyConfig.is_active == True
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def get_proxy_config_or_default(config_name: str = "default") -> Tuple[str, str]:
    """
    获取代理配置，如果不存在则使用默认值
    
    Args:
        config_name: 配置名称，默认为 "default"
    
    Returns:
        (base_url, api_key) 元组
    """
    config = await get_proxy_config(config_name)
    if config:
        return config.base_url, config.api_key
    
    # 如果数据库中没有配置，使用默认值（从配置文件或硬编码）
    from app.core.config import settings
    return settings.HIAGENT_BASE_URL, settings.HIAGENT_API_KEY

