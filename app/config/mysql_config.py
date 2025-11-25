from typing import Optional


class MySqlConfig:
    """MySQL数据库配置"""

    def __init__(self, **kwargs):
        """
        从关键字参数初始化配置
        
        Args:
            **kwargs: 配置参数，如host, port, user等
        """
        # 默认值
        self.host: str = kwargs.get('host', "")
        self.port: int = kwargs.get('port', 3306)
        self.user: str = kwargs.get('user', "root")
        self.password: str = kwargs.get('password', "")
        self.database: str = kwargs.get('database', "")
        self.pool_size: int = kwargs.get('pool_size', 5)
        self.pool_timeout: int = kwargs.get('pool_timeout', 30)
        self.charset: str = kwargs.get('charset', "utf8mb4")
        self.autocommit: bool = kwargs.get('autocommit', True)
