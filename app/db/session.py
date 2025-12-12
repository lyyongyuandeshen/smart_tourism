from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.config.config import config
from app.config.mysql_config import MySqlConfig

_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker] = None


async def init_engine() -> None:
    global _engine, _session_factory
    if _engine is None:
        mysql_config = config.get_mysql_config()
        # 构建异步MySQL连接URL
        database_url = f"mysql+aiomysql://{mysql_config.user}:{mysql_config.password}@{mysql_config.host}:{mysql_config.port}/{mysql_config.database}?charset=utf8mb4"
        _engine = create_async_engine(database_url, pool_pre_ping=True)
        _session_factory = async_sessionmaker(bind=_engine, expire_on_commit=False)


def get_engine() -> AsyncEngine:
    assert _engine is not None, "Engine not initialized. Call init_engine() on startup."
    return _engine


def get_session_factory() -> async_sessionmaker:
    assert _session_factory is not None, "Session factory not initialized."
    return _session_factory


async def dispose_engine() -> None:
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None


