import json
from typing import Any, Dict, Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File, Query
from fastapi.responses import StreamingResponse, RedirectResponse, Response
from pydantic import BaseModel, Field

from app.api.constant import ErrorResponse
from app.services.proxy_config import get_proxy_config_or_default

router = APIRouter(
    responses={
        404: {"description": "接口不存在"},
        500: {"description": "服务器内部错误"},
    }
)


class ProxyRequest(BaseModel):
    """代理请求模型
    
    用于代理转发请求到 HiAgent 服务，后端会根据 config_name 从数据库获取对应的 base_url 和 api_key。
    action 和 body 字段会原样转发到目标服务，不做任何处理。
    """
    action: str = Field(
        ...,
        title = "动作名称",
        description="动作名称，如 'create_conversation'、'send_message' 等",
        example="create_conversation",
        min_length=1,
        max_length=100
    )
    body: Dict[str, Any] = Field(
        ...,
        description="请求体，后端不做处理直接转发到目标服务",
        example={
            "UserID": "default",
            "Inputs": {
                "var": "variable"
            }
        }
    )
    config_name: Optional[str] = Field(
        default="default",
        description="配置名称，用于从数据库获取对应的 base_url 和 api_key。如果不提供，默认使用 'default' 配置",
        example="default",
        max_length=100
    )

    class Config:
        json_schema_extra = {
            "example": {
                "action": "create_conversation",
                "body": {
                    "UserID": "default",
                    "Inputs": {
                        "var": "variable"
                    }
                },
                "config_name": "default"
            }
        }


async def _make_proxy_request(
    action: str, 
    body: Dict[str, Any], 
    base_url: str,
    api_key: str,
    stream: bool = False
) -> httpx.Response:
    """
    发起代理请求
    
    Args:
        action: 动作名称
        body: 请求体
        base_url: 代理基础URL（从数据库获取）
        api_key: API密钥（从数据库获取）
        stream: 是否流式返回
    
    Returns:
        httpx.Response: 响应对象
    """
    url = f"{base_url.rstrip('/')}/{action}"
    headers = {
        "Apikey": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        async with httpx.AsyncClient(timeout=300.0) as client:
            response = await client.post(
                url,
                headers=headers,
                json=body,
                follow_redirects=True
            )
            response.raise_for_status()
            return response
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"代理请求失败: {e.response.text}"
        )
    except httpx.RequestError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"代理请求网络错误: {str(e)}"
        )


@router.post(
    "/agent/proxy",
    summary="智能体-非流式代理接口",
    description="""
    非流式代理接口，用于转发请求到 HiAgent 服务并返回完整响应。
    
    **工作流程：**
    1. 根据 `config_name` 从数据库获取对应的 `base_url` 和 `api_key`
    2. 将 `action` 和 `body` 原样转发到目标服务
    3. 返回目标服务的完整响应
    
    **使用场景：**
    - 创建会话
    - 发送消息（需要完整响应）
    - 查询状态
    - 其他需要完整响应的操作
    
    **注意事项：**
    - `body` 字段的内容会原样转发，不做任何验证或处理
    - 如果数据库中没有对应的配置，会使用默认配置（从配置文件读取）
    - 响应格式取决于目标服务的实际返回
    """,
    response_model=Dict[str, Any],
    responses={
        200: {
            "description": "请求成功，返回目标服务的响应数据",
            "content": {
                "application/json": {
                    "example": {
                        "Conversation": {
                            "AppConversationID": "conv-123456"
                        }
                    }
                }
            }
        },
        400: {
            "description": "请求参数错误",
            "model": ErrorResponse
        },
        401: {
            "description": "认证失败（API Key 无效）",
            "model": ErrorResponse
        },
        404: {
            "description": "配置不存在或目标服务不存在",
            "model": ErrorResponse
        },
        502: {
            "description": "代理请求网络错误",
            "model": ErrorResponse
        }
    },
    status_code=status.HTTP_200_OK
)
async def proxy_request(request: ProxyRequest) -> Dict[str, Any]:
    """
    非流式代理接口
    
    接收 action 和请求体，从数据库获取 base_url 和 api_key，转发到 HiAgent 并返回完整响应
    
    Args:
        request: 包含 action、body 和 config_name 的请求对象
    
    Returns:
        完整的响应数据，格式取决于目标服务的实际返回
    """
    # 从数据库获取配置
    base_url, api_key = await get_proxy_config_or_default(request.config_name)
    
    response = await _make_proxy_request(
        request.action, 
        request.body, 
        base_url=base_url,
        api_key=api_key,
        stream=False
    )
    
    try:
        return response.json()
    except json.JSONDecodeError:
        # 如果不是 JSON，返回文本
        return {"text": response.text}


@router.post(
    "/agent/stream",
    summary="智能体-流式代理接口",
    description="""
    流式代理接口，用于转发请求到 HiAgent 服务并流式返回响应（SSE 格式）。
    
    **工作流程：**
    1. 根据 `config_name` 从数据库获取对应的 `base_url` 和 `api_key`
    2. 将 `action` 和 `body` 原样转发到目标服务（请求头为 application/json）
    3. 流式读取代理返回的数据并流式返回给前端（SSE 格式）
    
    **返回方式：**
    - 标准的 SSE 格式（`data: {chunk}\\n\\n`），Content-Type: text/event-stream
    
    **使用场景：**
    - 实时对话（流式返回）
    - 长文本生成（流式返回）
    - 需要实时反馈的操作
    
    **注意事项：**
    - `body` 字段的内容会原样转发，不做任何验证或处理
    - 如果数据库中没有对应的配置，会使用默认配置（从配置文件读取）
    - 代理的 URL 返回是流式的，我们会流式读取并流式返回
    - 前端请求格式为 application/json，返回格式为 text/event-stream
    """,
    responses={
        200: {
            "description": "流式响应（SSE 格式），数据会分块返回",
            "content": {
                "text/event-stream": {
                    "example": "data: {chunk}\n\n"
                }
            }
        },
        400: {
            "description": "请求参数错误",
            "model": ErrorResponse
        },
        401: {
            "description": "认证失败（API Key 无效）",
            "model": ErrorResponse
        },
        404: {
            "description": "配置不存在或目标服务不存在",
            "model": ErrorResponse
        },
        502: {
            "description": "代理请求网络错误",
            "model": ErrorResponse
        }
    },
    status_code=status.HTTP_200_OK
)
async def proxy_request_stream(request: ProxyRequest):
    """
    流式代理接口
    
    接收 action 和请求体，从数据库获取 base_url 和 api_key，转发到 HiAgent 并流式返回响应（SSE 格式）
    
    Args:
        request: 包含 action、body 和 config_name 的请求对象
    
    Returns:
        流式响应（StreamingResponse，SSE 格式）
    """
    # 从数据库获取配置
    base_url, api_key = await get_proxy_config_or_default(request.config_name)
    
    url = f"{base_url.rstrip('/')}/{request.action}"
    headers = {
        "Accept": "text/event-stream",
        "Apikey": api_key,
        "Content-Type": "application/json",
        "Connection": "keep-alive"
    }

    stream_headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive"
    }
    
    # 流式返回（SSE 格式）
    async def generate():
        """生成流式响应(SSE 格式)"""
        try:
            async with httpx.AsyncClient(timeout=300.0) as client:
                async with client.stream(
                    "POST",
                    url,
                    headers=headers,
                    json=request.body,
                    follow_redirects=True
                ) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        if chunk:
                            try:
                                # 尝试解码为文本
                                chunk_text = chunk.decode("utf-8", errors="ignore")
                                # SSE 格式：data: {content}\n\n
                                sse_data = f"data: {chunk_text}\n\n"
                                yield sse_data.encode("utf-8")
                            except Exception:
                                # 如果解码失败，直接作为二进制数据返回（不常见）
                                sse_data = f"data: {chunk.hex()}\n\n"
                                yield sse_data.encode("utf-8")
        except httpx.HTTPStatusError as e:
            error_data = json.dumps({
                "error": f"代理请求失败: {e.response.status_code}",
                "detail": e.response.text
            })
            sse_error = f"data: {error_data}\n\n"
            yield sse_error.encode("utf-8")
        except httpx.RequestError as e:
            error_data = json.dumps({
                "error": "代理请求网络错误",
                "detail": str(e)
            })
            sse_error = f"data: {error_data}\n\n"
            yield sse_error.encode("utf-8")
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers=stream_headers
    )
