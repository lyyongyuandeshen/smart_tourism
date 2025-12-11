import os
from venv import logger

import redis
from dotenv import load_dotenv
from mysql.connector import pooling

from app.config.mysql_config import MySqlConfig
from app.config.redis_config import RedisConfig
from app.config.tos_config import TosConfig


class ConfigManager:
    """
    全局配置管理类，包括：
        1、mysql
        2、redis
        3、kafka
        4、agent配置
        5、TOS对象存储
    """

    def __init__(self):
        self._mysql_pool: pooling.MySQLConnectionPool = None
        self._redis_pool: redis.ConnectionPool = None
        self._mysql_config = self._load_mysql_config()
        self._tos_config = self._load_tos_config()
        self._tos_service = None

    def _load_mysql_config(self) -> MySqlConfig:
        """从环境变量加载MySQL配置"""
        logger.info(f"os.getenv('MYSQL_HOST'): {os.getenv('MYSQL_HOST')}")
        return MySqlConfig(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DATABASE", ""),
            pool_size=int(os.getenv("MYSQL_POOL_SIZE", "5")),
            pool_timeout=int(os.getenv("MYSQL_POOL_TIMEOUT", "30")),
            charset=os.getenv("MYSQL_CHARSET", "utf8mb4"),
            auth_plugin="mysql_native_password",
            use_pure=True,
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

    def get_tos_config(self) -> TosConfig:
        """获取TOS配置"""
        if self._tos_config is None:
            self._tos_config = self._load_tos_config()
        return self._tos_config

    def get_tos_service(self):
        """获取TOS服务实例"""
        if self._tos_service is None:
            # 延迟导入避免循环依赖
            from app.services.tos_service import TosService
            tos_config = self.get_tos_config()
            self._tos_service = TosService(tos_config)
        return self._tos_service

    def _load_tos_config(self) -> TosConfig:
        """从环境变量加载TOS配置"""
        return TosConfig(
            endpoint=os.getenv("endpoint"),
            access_key=os.getenv("access_key"),
            secret_key=os.getenv("secret_key"),
            bucket_name=os.getenv("bucket_name"),
            region=os.getenv("region"),
        )

    def _init_mysql_pool(self, database=None):
        """初始化MySQL配置信息，创建连接池"""
        mysql_conf: MySqlConfig = self.get_mysql_config()
        logger.info(f"mysql_conf: {mysql_conf}")
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
                connect_timeout=mysql_conf.pool_timeout)
            logger.info(
                f"init mysql connection pool, host: {mysql_conf.host}, "
                f"port: {mysql_conf.port}, db: {mysql_conf.database}"
            )
        except Exception as e:
            logger.error(f"init mysql connection pool failed: {str(e)}")
            raise

    def inject(self):
        """注入配置管理器"""
        # self._init_redis_config()
        self._init_mysql_pool()


# 加载环境变量
load_dotenv(dotenv_path=".env")
# 创建全局单例实例
config = ConfigManager()
