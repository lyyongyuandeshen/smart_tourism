from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=False)

    PROJECT_NAME: str = "Smart Tourism Backend"
    VERSION: str = "0.1.0"

    # Database
    MYSQL_USER: str = "root"
    # 对密码中的 @ 进行 URL 编码
    # @ 在 URL 中的编码是 %40，所以正确的 URL 应该是：
    MYSQL_PASSWORD: str = ""
    MYSQL_HOST: str = ""
    MYSQL_PORT: int = 3306
    MYSQL_DB: str = "db_smart_tourism"

    @property
    def DATABASE_URL(self) -> str:
        print( f"mysql+asyncmy://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"+"?charset=utf8mb4")
        return (
            f"mysql+asyncmy://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}"+"?charset=utf8mb4"
        )

    # Redis
    REDIS_URL: str = "redis://172.16.65.62:6379/9"

    # Kafka
    KAFKA_BOOTSTRAP_SERVERS: str = ""
    KAFKA_CLIENT_ID: str = ""
    KAFKA_HEALTH_TOPIC: str = ""

    # Security / JWT
    SECRET_KEY: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600
    JWT_ALGORITHM: str = "HS256"

    # 火山引擎SDK 的AK及SK。
    VOLC_ACCESSKEY: str = "Your AK" 
    VOLC_SECRETKEY: str = 'Your SK'  # 标注为字符串类型
    
    # 平台 API 代理配置（火山引擎签名方式）
    PLATFORM_API_HOST: str = ""  # 平台 API 主机地址，top 的端口默认为：30040
    PLATFORM_API_IP: str = ""
    PLATFORM_API_AK: str = ""  # 平台 API AccessKey
    PLATFORM_API_SK: str = ""  # 平台 API SecretKey
    PLATFORM_API_REGION: str = ""  # 平台 API 区域
    PLATFORM_API_SERVICE: str = ""  # 平台 API 服务名称
    
    # 火山引擎 TOS（对象存储）配置
    TOS_ENDPOINT: str = ""  # TOS 端点
    TOS_REGION: str = ""  # TOS 区域
    TOS_BUCKET: str = ""  # TOS 存储桶名称
    TOS_ACCESS_KEY: str = ""  # TOS AccessKey（如果为空则使用 VOLC_ACCESSKEY）
    TOS_SECRET_KEY: str = "=="  # TOS SecretKey（如果为空则使用 VOLC_SECRETKEY）

    # 思明服务平台客户端配置(主要用于单点登录)
    SM_SSO_CLIENT_ID: str = ""
    SM_SSO_CLIENT_SECRET: str = ""
    SM_SSO_DOMAIN: str = ""
    # SM_SSO_CLIENT_ID: str = ""

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()


