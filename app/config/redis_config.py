from typing import Optional


class RedisConfig:
    """Redis数据库配置"""
    
    def __init__(self, **kwargs):
        """
        从关键字参数初始化配置
        
        Args:
            **kwargs: 配置参数，如host, port, password等
        """
        # 默认值
        self.host: str = kwargs.get('host', "127.0.0.1")
        self.port: int = kwargs.get('port', 6379)
        self.password: Optional[str] = kwargs.get('password', "")
        self.db: int = kwargs.get('db', 1)
        self.max_connections: int = kwargs.get('max_connections', 10)
