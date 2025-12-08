from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse
from typing import Optional
import logging

from app.models.sso_models import (
    SSOAuthRequest, AccessTokenRequest, UserInfoRequest, SSOLoginRequest,
    SSOLoginResponse, SSOErrorResponse
)
from app.services.sso_service import SSOService

logger = logging.getLogger(__name__)

router = APIRouter()

# SSO服务实例
sso_service = SSOService()


@router.get("/auth-url", summary="获取SSO授权URL")
async def get_auth_url(
    callback_url: str = Query(..., description="回调地址")
):
    """
    获取SSO授权URL
    
    Args:
        callback_url: 授权成功后的回调地址
        
    Returns:
        dict: 包含授权URL的响应
    """
    try:
        auth_url = sso_service.generate_auth_url(callback_url)
        
        return {
            "success": True,
            "message": "获取授权URL成功",
            "data": {
                "auth_url": auth_url,
                "client_id": sso_service.client_id,
                "callback_url": callback_url
            }
        }
    except Exception as e:
        logger.error(f"获取授权URL失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"获取授权URL失败: {str(e)}"
        )


@router.get("/redirect", summary="重定向到SSO授权页面")
async def redirect_to_sso(
    callback_url: str = Query(..., description="回调地址")
):
    """
    直接重定向到SSO授权页面
    
    Args:
        callback_url: 授权成功后的回调地址
        
    Returns:
        RedirectResponse: 重定向响应
    """
    try:
        auth_url = sso_service.generate_auth_url(callback_url)
        return RedirectResponse(url=auth_url)
    except Exception as e:
        logger.error(f"重定向到SSO失败: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"重定向到SSO失败: {str(e)}"
        )


@router.post("/access-token", summary="获取访问令牌")
async def get_access_token(request: AccessTokenRequest):
    """
    使用授权码获取访问令牌
    
    Args:
        request: 访问令牌请求
        
    Returns:
        dict: 访问令牌响应
    """
    try:
        result = await sso_service.get_access_token(request.code)
        
        return {
            "success": result.code == 0,
            "message": result.msg,
            "data": result.data
        }
    except Exception as e:
        logger.error(f"获取访问令牌失败: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"获取访问令牌失败: {str(e)}"
        )


@router.post("/user-info", summary="获取用户信息")
async def get_user_info(request: UserInfoRequest):
    """
    使用授权码和访问令牌获取用户信息
    
    Args:
        request: 用户信息请求
        
    Returns:
        dict: 用户信息响应
    """
    try:
        result = await sso_service.get_user_info(request.code, request.access_token)
        
        return {
            "success": result.code == 0,
            "message": result.msg,
            "data": result.data
        }
    except Exception as e:
        logger.error(f"获取用户信息失败: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"获取用户信息失败: {str(e)}"
        )


@router.post("/login", summary="SSO一键登录", response_model=SSOLoginResponse)
async def sso_login(request: SSOLoginRequest):
    """
    SSO一键登录（推荐使用）
    
    使用授权码直接获取用户信息，封装了获取Token和用户信息的步骤
    
    Args:
        request: SSO登录请求
        
    Returns:
        SSOLoginResponse: 登录响应
    """
    try:
        # 验证客户端信息
        if request.client_id != sso_service.client_id:
            return SSOLoginResponse(
                success=False,
                message="客户端标识不正确",
                data=None
            )
        
        if request.client_secret != sso_service.client_secret:
            return SSOLoginResponse(
                success=False,
                message="客户端密钥不正确",
                data=None
            )
        
        # 执行SSO登录
        result = await sso_service.sso_login(request.code)
        
        # 如果登录成功，提取基本用户信息
        if result.success and result.user_info:
            basic_info = sso_service.extract_user_basic_info(result.user_info)
            result.data = {
                **(result.data or {}),
                "basic_info": basic_info
            }
        
        return result
        
    except Exception as e:
        logger.error(f"SSO登录失败: {e}")
        return SSOLoginResponse(
            success=False,
            message=f"SSO登录失败: {str(e)}",
            data=None
        )


@router.get("/callback", summary="SSO授权回调处理")
async def sso_callback(
    code: Optional[str] = Query(None, description="授权码"),
    error: Optional[str] = Query(None, description="错误信息"),
    error_description: Optional[str] = Query(None, description="错误描述")
):
    """
    处理SSO授权回调
    
    Args:
        code: 授权码（成功时返回）
        error: 错误代码（失败时返回）
        error_description: 错误描述（失败时返回）
        
    Returns:
        dict: 回调处理结果
    """
    if error:
        logger.error(f"SSO授权失败: {error} - {error_description}")
        return {
            "success": False,
            "message": f"授权失败: {error}",
            "error_description": error_description
        }
    
    if not code:
        return {
            "success": False,
            "message": "未收到授权码"
        }
    
    return {
        "success": True,
        "message": "授权成功",
        "data": {
            "code": code,
            "next_step": "使用此授权码调用 /api/v1/sso/login 接口完成登录"
        }
    }


@router.post("/validate-token", summary="验证访问令牌")
async def validate_token(
    access_token: str = Query(..., description="访问令牌")
):
    """
    验证访问令牌是否有效
    
    Args:
        access_token: 访问令牌
        
    Returns:
        dict: 验证结果
    """
    try:
        is_valid = await sso_service.validate_token(access_token)
        
        return {
            "success": True,
            "message": "令牌验证完成",
            "data": {
                "is_valid": is_valid,
                "access_token": access_token
            }
        }
    except Exception as e:
        logger.error(f"验证令牌失败: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"验证令牌失败: {str(e)}"
        )


@router.get("/config", summary="获取SSO配置信息")
async def get_sso_config():
    """
    获取SSO配置信息（不包含敏感信息）
    
    Returns:
        dict: SSO配置信息
    """
    return {
        "success": True,
        "message": "获取SSO配置成功",
        "data": {
            "auth_url": sso_service.sso_auth_url,
            "api_base_url": sso_service.sso_api_base_url,
            "client_id": sso_service.client_id,
            "timeout": sso_service.timeout,
            "support_endpoints": [
                "/auth-url - 获取授权URL",
                "/redirect - 重定向到授权页面",
                "/access-token - 获取访问令牌",
                "/user-info - 获取用户信息",
                "/login - 一键登录（推荐）",
                "/callback - 授权回调处理",
                "/validate-token - 验证令牌",
                "/config - 获取配置信息"
            ]
        }
    }