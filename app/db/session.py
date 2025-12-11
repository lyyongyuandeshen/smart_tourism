from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings

_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker] = None


async def init_engine() -> None:
    global _engine, _session_factory
    if _engine is None:
        _engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
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


