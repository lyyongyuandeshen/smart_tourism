import os
from venv import logger

import redis
from mysql.connector import pooling

from app.config.mysql_config import MySqlConfig
from app.config.redis_config import RedisConfig


class ConfigManager:
    """
    全局配置管理类，包括：
        1、mysql
        2、redis
        3、kafka
        4、agent配置
    """

    def __init__(self):
        self._mysql_pool: pooling.MySQLConnectionPool = None
        self._redis_pool: redis.ConnectionPool = None
        self._mysql_config = self._load_mysql_config()

    def _load_mysql_config(self) -> MySqlConfig:
        """从环境变量加载MySQL配置"""
        return MySqlConfig(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE", ""),
            pool_size=int(os.getenv("MYSQL_POOL_SIZE", "5")),
            pool_timeout=int(os.getenv("MYSQL_POOL_TIMEOUT", "30")),
            charset=os.getenv("MYSQL_CHARSET", "utf8mb4"),
            autocommit=os.getenv("MYSQL_AUTOCOMMIT", "true").lower() == "true"
        )

    def _load_redis_config(self) -> RedisConfig:
        """从环境变量加载Redis配置"""
        return RedisConfig(
            host=os.getenv("REDIS_HOST", "127.0.0.1"),
            port=int(os.getenv("REDIS_PORT", "6379")),
            password=os.getenv("REDIS_PASSWORD"),
            db=int(os.getenv("REDIS_DB", "0")),
            max_connections=int(os.getenv("REDIS_MAX_CONNECTIONS", "10")),
        )

    def get_mysql_config(self) -> MySqlConfig:
        """获取MySQL配置"""
        return self._mysql_config

    def get_mysql_pool(self) -> pooling.MySQLConnectionPool:
        """获取MySQL连接池"""
        return self._mysql_pool

    def get_redis_client(self) -> redis.Redis:
        """获取Redis客户端实例"""
        return self._redis_client

    def _init_redis_config(self):
        """初始化redis配置信息，创建redis连接池"""
        self._redis_config = self._load_redis_config()
        # 创建redis连接池
        redis_pool = redis.ConnectionPool(
            host=self._redis_config.host,
            port=self._redis_config.port,
            password=self._redis_config.password,
            db=self._redis_config.db,
            max_connections=self._redis_config.max_connections
        )
        # 获取一个实例对象，全局只有一个，可能存在并发瓶颈，后续可优化多个连接client
        self._redis_client = redis.Redis(connection_pool=redis_pool)

    def _init_mysql_pool(self, database=None):
        """初始化MySQL配置信息，创建连接池"""
        mysql_conf: MySqlConfig = self.get_mysql_config()
        if not mysql_conf:
            raise ValueError("MySQL configuration is missing")
        required_fields = ['host', 'port', 'user', 'password', 'database']
        for field in required_fields:
            if not getattr(mysql_conf, field, None):
                raise ValueError(f"MySQL configuration missing required field: {field}")
        try:
            self._mysql_pool = pooling.MySQLConnectionPool(
                pool_name="samrt_tourism_pool",
                pool_size=mysql_conf.pool_size,
                pool_reset_session=True,
                host=mysql_conf.host,
                port=mysql_conf.port,
                user=mysql_conf.user,
                password=mysql_conf.password,
                database=mysql_conf.database if database is None else database,
                connect_timeout=mysql_conf.pool_timeout
            )
            logger.info(
                f"init mysql connection pool, host: {mysql_conf.host}, "
                f"port: {mysql_conf.port}, db: {mysql_conf.database}"
            )
        except Exception as e:
            logger.error(f"init mysql connection pool failed: {str(e)}")
            raise
