from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime
from datetime import datetime


class Base(DeclarativeBase):
    pass


class ProxyConfig(Base):
    """代理配置表"""
    __tablename__ = "tbkf_proxy_config_info"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, comment="配置名称")
    base_url: Mapped[str] = mapped_column(String(500), nullable=False, comment="代理基础URL")
    api_key: Mapped[str] = mapped_column(String(200), nullable=False, comment="API密钥")
    is_active: Mapped[bool] = mapped_column(default=True, comment="是否启用")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, comment="创建时间")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment="更新时间")


