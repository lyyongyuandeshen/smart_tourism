from typing import Annotated, AsyncGenerator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_access_token
from app.db.session import get_session_factory


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_username(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    try:
        payload = decode_access_token(token)
        username: Optional[str] = payload.get("sub")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return username


async def get_current_user_id(token: Annotated[str, Depends(oauth2_scheme)]) -> str:
    """获取当前用户ID"""
    try:
        payload = decode_access_token(token)
        user_id: Optional[str] = payload.get("uid")
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user_id


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    session_factory = get_session_factory()
    async with session_factory() as session:
        yield session

