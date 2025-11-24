from dataclasses import Field
from typing import Optional


class RedisConfig:
    host: str = Field(default="127.0.0.1", description="Redis 主机地址")
    port: int = Field(default=6379, description="Redis 端口")
    password: Optional[str] = Field(default="", description="Redis 密码")
    db: int = Field(default=1, description="Redis 数据库编号")
    max_connections: int = Field(default=10, description="Redis 连接池最大连接数")
