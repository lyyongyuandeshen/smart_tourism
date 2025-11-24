from dataclasses import Field
from typing import Optional


class MySqlConfig():
    """MySQL数据库配置"""
    host: str = Field(default="127.0.0.1", description="MySQL主机地址")
    port: int = Field(default=3306, description="MySQL端口")
    user: str = Field(default="root", description="MySQL用户名")
    password: Optional[str] = Field(default=None, description="MySQL密码")
    database: str = Field(default="", description="MySQL数据库名")
    pool_size: int = Field(default=5, description="连接池大小")
    pool_timeout: int = Field(default=30, description="连接超时时间(秒)")
    charset: str = Field(default="utf8mb4", description="数据库字符集")
    autocommit: bool = Field(default=True, description="是否自动提交事务")

    def __init__(self, **kwargs):
        """
        从关键字参数初始化配置
        
        Args:
            **kwargs: 配置参数，如host, port, user等
        """
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)