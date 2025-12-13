import httpx
import logging
from typing import Optional, Dict, Any
from app.models.sso_models import (
    AccessTokenRequest, UserInfoRequest, SSOLoginRequest,
    AccessTokenResponse, UserInfoResponse, SSOLoginResponse,
    SSOErrorResponse, UserInfo
)
from app.config.config import config

logger = logging.getLogger(__name__)


class SSOService:
    """SSO集成服务"""

    def __init__(self):
        # SSO服务配置
        self.sso_auth_url = "https://test-api.smdata.com.cn/wisdomSimingApp/sso"
        self.sso_api_base_url = "http://115.190.160.216/api/v1"
        self.client_id = "qoos2xwcpl0svmf7"
        self.client_secret = "b5hjzmqc62u0wx861q89t8mcjvh9f5gu"

        # HTTP客户端配置
        self.timeout = 30.0
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "SmartTourism/1.0"
        }

    def generate_auth_url(self, callback_url: str) -> str:
        """
        生成SSO授权URL
        
        Args:
            callback_url: 回调地址
            
        Returns:
            str: 授权URL
        """
        return f"{self.sso_auth_url}?appClientId={self.client_id}&callBackUrl={callback_url}"

    async def get_access_token(self, code: str) -> AccessTokenResponse:
        """
        获取访问令牌
        
        Args:
            code: 授权码
            
        Returns:
            AccessTokenResponse: 访问令牌响应
            
        Raises:
            Exception: 请求失败时抛出异常
        """
        url = f"{self.sso_api_base_url}/accessToken"
        payload = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()

                result = response.json()
                logger.info(f"获取访问令牌成功: {result}")

                return AccessTokenResponse(**result)

        except httpx.HTTPStatusError as e:
            logger.error(f"获取访问令牌HTTP错误: {e.response.status_code} - {e.response.text}")
            raise Exception(f"获取访问令牌失败: HTTP {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"获取访问令牌请求错误: {e}")
            raise Exception(f"获取访问令牌请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"获取访问令牌未知错误: {e}")
            raise Exception(f"获取访问令牌失败: {str(e)}")

    async def get_user_info(self, code: str, access_token: str) -> UserInfoResponse:
        """
        获取用户信息
        
        Args:
            code: 授权码
            access_token: 访问令牌
            
        Returns:
            UserInfoResponse: 用户信息响应
            
        Raises:
            Exception: 请求失败时抛出异常
        """
        url = f"{self.sso_api_base_url}/userInfo"
        payload = {
            "code": code,
            "access_token": access_token
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()

                result = response.json()
                logger.info(f"获取用户信息成功: {result}")

                return UserInfoResponse(**result)

        except httpx.HTTPStatusError as e:
            logger.error(f"获取用户信息HTTP错误: {e.response.status_code} - {e.response.text}")
            raise Exception(f"获取用户信息失败: HTTP {e.response.status_code}")
        except httpx.RequestError as e:
            logger.error(f"获取用户信息请求错误: {e}")
            raise Exception(f"获取用户信息请求失败: {str(e)}")
        except Exception as e:
            logger.error(f"获取用户信息未知错误: {e}")
            raise Exception(f"获取用户信息失败: {str(e)}")

    async def sso_login(self, code: str) -> SSOLoginResponse:
        """
        SSO一键登录（封装获取Token和用户信息的操作）
        
        Args:
            code: 授权码
            
        Returns:
            SSOLoginResponse: 登录响应
        """
        url = f"{self.sso_api_base_url}/sso_login"
        payload = {
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload, headers=self.headers)
                response.raise_for_status()

                result = response.json()
                logger.info(f"SSO登录成功: {result}")

                # 解析用户信息
                user_info = None
                access_token = None

                if result.get("code") == 0 and result.get("data"):
                    data = result["data"]
                    if "user_info" in data:
                        try:
                            user_info = UserInfo(**data["user_info"])
                            # 将用户信息插入到sys_user表
                            await self._insert_user_to_db(user_info)
                        except Exception as e:
                            logger.warning(f"解析用户信息失败: {e}")

                token_result = await self.get_access_token(code)
                access_token = token_result.data.get("access_token")
                return SSOLoginResponse(
                    success=result.get("code") == 0,
                    message=result.get("msg", "登录成功"),
                    data=result.get("data"),
                    access_token=access_token,
                    user_info=user_info
                )

        except httpx.HTTPStatusError as e:
            logger.error(f"SSO登录HTTP错误: {e.response.status_code} - {e.response.text}")
            return SSOLoginResponse(
                success=False,
                message=f"SSO登录失败: HTTP {e.response.status_code}",
                data=None
            )
        except httpx.RequestError as e:
            logger.error(f"SSO登录请求错误: {e}")
            return SSOLoginResponse(
                success=False,
                message=f"SSO登录请求失败: {str(e)}",
                data=None
            )
        except Exception as e:
            logger.error(f"SSO登录未知错误: {e}")
            return SSOLoginResponse(
                success=False,
                message=f"SSO登录失败: {str(e)}",
                data=None
            )

    async def validate_token(self, access_token: str) -> bool:
        """
        验证访问令牌是否有效
        
        Args:
            access_token: 访问令牌
            
        Returns:
            bool: 令牌是否有效
        """
        # 这里可以实现令牌验证逻辑
        # 目前简单返回True，实际项目中应该调用SSO服务验证
        return bool(access_token and len(access_token) > 0)

    def extract_user_basic_info(self, user_info: UserInfo) -> Dict[str, Any]:
        """
        提取用户基本信息
        
        Args:
            user_info: 完整用户信息
            
        Returns:
            Dict[str, Any]: 基本用户信息
        """
        return {
            "user_id": user_info.id,
            "username": user_info.user_name,
            "real_name": user_info.user_real_name,
            "mobile": user_info.user_mobile,
            "email": user_info.user_biz_email,
            "credit_id": user_info.credit_id,
            "company": user_info.user_remarks,
            "gender": user_info.user_gender,
            "status": user_info.user_status,
            "departments": [
                {
                    "dept_id": dept.dept_id,
                    "dept_name": dept.dept_name,
                    "dept_code": dept.dept_code,
                    "is_leader": dept.leader_status == 1,
                    "is_main": dept.main_dept == "1"
                }
                for dept in user_info.user_depts
            ]
        }

    async def _insert_user_to_db(self, user_info: UserInfo) -> None:
        """
        将用户信息插入到sys_user表
        
        Args:
            user_info: 用户信息对象
        """
        try:
            from app.config.config import config
            from datetime import datetime
            
            pool = config.get_mysql_pool()
            if not pool:
                logger.error("数据库连接池未初始化")
                return
            
            conn = None
            cursor = None
            try:
                conn = pool.get_connection()
                cursor = conn.cursor()
                
                # 先检查用户是否已存在
                check_query = "SELECT user_id FROM sys_user WHERE user_id = %s"
                cursor.execute(check_query, (user_info.id,))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    logger.info(f"用户已存在，跳过插入: {user_info.id}")
                    return
                
                # 插入用户信息
                insert_query = """
                    INSERT INTO sys_user (
                        user_id, user_name, nick_name, user_type, email, 
                        phonenumber, status, del_flag, create_time
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                
                params = (
                    user_info.id,  # user_id
                    user_info.userRealName,  # user_name
                    user_info.userRealName,  # nick_name
                    '00',  # user_type 默认值
                    user_info.userBizEmail or None,  # email
                    user_info.userMobile or None,  # phonenumber
                    user_info.userStatus or '0',  # status
                    '0',  # del_flag 默认值
                    datetime.now()  # create_time
                )
                
                cursor.execute(insert_query, params)
                conn.commit()
                logger.info(f"成功插入用户信息到sys_user表: {user_info.id}")
                
            except Exception as e:
                if conn:
                    conn.rollback()
                logger.error(f"插入用户信息到数据库失败: {e}")
                raise
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
                    
        except Exception as e:
            logger.error(f"处理用户信息插入失败: {e}")
