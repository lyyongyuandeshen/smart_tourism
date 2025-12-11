from typing import Optional


class TosConfig:
    """火山云TOS对象存储配置"""

    def __init__(self, **kwargs):
        """
        从关键字参数初始化配置
        
        Args:
            **kwargs: 配置参数，如access_key, secret_key, endpoint等
        """
        # 基础配置
        self.access_key: str = kwargs.get('access_key', "")
        self.secret_key: str = kwargs.get('secret_key', "")
        self.endpoint: str = kwargs.get('endpoint', "")
        self.region: str = kwargs.get('region', "")
        self.bucket_name: str = kwargs.get('bucket_name', "")
        
        # 上传配置
        self.max_file_size: int = kwargs.get('max_file_size', 100 * 1024 * 1024)  # 100MB
        self.allowed_image_types: list = kwargs.get('allowed_image_types', [
            'jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp'
        ])
        self.allowed_video_types: list = kwargs.get('allowed_video_types', [
            'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm'
        ])
        
        # 存储路径配置
        self.image_prefix: str = kwargs.get('image_prefix', "images/")
        self.video_prefix: str = kwargs.get('video_prefix', "videos/")
        
        # CDN配置（可选）
        self.cdn_domain: Optional[str] = kwargs.get('cdn_domain', None)
        
        # 安全配置
        self.enable_https: bool = kwargs.get('enable_https', True)
        self.connection_timeout: int = kwargs.get('connection_timeout', 30)
        self.socket_timeout: int = kwargs.get('socket_timeout', 30)
        self.enable_verify_ssl: bool = kwargs.get("enable_verify_ssl", False)  # 默认禁用SSL验证
        self.max_retry_count: int = kwargs.get("max_retry_count", 3)  # 重试次数
    def __str__(self):
        return f"TosConfig(endpoint={self.endpoint}, bucket={self.bucket_name}, region={self.region})"

    def __repr__(self):
        return self.__str__()