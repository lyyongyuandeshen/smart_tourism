"""
安全相关工具
"""
import jwt
from datetime import datetime, timedelta
from typing import Dict, Optional
import logging

logger = logging.getLogger(__name__)

# JWT配置（应该从配置文件中读取）
SECRET_KEY = "your-secret-key-here"  # TODO: 从配置文件读取
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    创建访问令牌
    
    Args:
        data: 要编码的数据
        expires_delta: 过期时间增量
        
    Returns:
        JWT token字符串
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Dict:
    """
    解码访问令牌
    
    Args:
        token: JWT token字符串
        
    Returns:
        解码后的数据字典
        
    Raises:
        jwt.PyJWTError: 如果token无效
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        logger.error("Token已过期")
        raise
    except jwt.JWTError as e:
        logger.error(f"Token解码失败: {e}")
        raise
