"""
实时聊天 WebSocket 接口
支持 AI 对话和转人工功能
"""
import json
import uuid
import logging
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session
from app.services.websocket_manager import manager
from app.services.proxy_config import get_proxy_config_or_default
import httpx

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/ws/info", summary="WebSocket 连接说明", include_in_schema=True)
async def websocket_info():
    """
    WebSocket 实时聊天接口说明
    
    **连接地址**: `ws://your-domain/api/chat/ws?user_id=uid&session_id=可选`
    
    **连接参数**:
    - `user_id` (必需): 用户ID，用于身份验证
    - `session_id` (可选): 会话ID，如果不存在则自动创建新会话
    
    **消息格式**:
    
    **发送消息**:
    ```json
    {
        "type": "message",  // 消息类型：message-发送消息, transfer-转人工, ping-心跳
        "content": "用户消息内容",
        "message_type": "text"  // 消息类型：text-文本, image-图片, file-文件
    }
    ```
    
    **接收消息**:
    ```json
    {
        "type": "message",  // 消息类型：message-普通消息, system-系统消息, error-错误, pong-心跳响应
        "sender_type": "ai",  // 发送者类型：user-用户, ai-AI助手, agent-人工客服, system-系统
        "content": "消息内容",
        "message_id": "消息ID",
        "timestamp": "2024-01-01T00:00:00"
    }
    ```
    
    **功能特性**:
    - ✅ AI 对话：自动创建 AI 会话并获取回复
    - ✅ 转人工：发送 `{"type": "transfer"}` 可转接人工客服并自动创建工单
    - ✅ 消息存储：所有消息保存到数据库
    - ✅ 心跳检测：支持 ping/pong 心跳保持连接
    
    **前端连接示例**:
    ```javascript
    const user_id = "your_user_id";
    const sessionId = "chat_123456"; // 可选
    const ws = new WebSocket(`ws://localhost:8000/api/chat/ws?user_id=${user_id}&session_id=${sessionId}`);
    
    // 接收消息
    ws.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log("收到消息:", message);
    };
    
    // 发送消息
    ws.send(JSON.stringify({
        type: "message",
        content: "你好",
        message_type: "text"
    }));
    
    // 转人工
    ws.send(JSON.stringify({
        type: "transfer"
    }));
    
    // 心跳
    setInterval(() => {
        ws.send(JSON.stringify({ type: "ping" }));
    }, 30000);
    ```
    """
    return {
        "websocket_url": "ws://your-domain/api/chat/ws",
        "description": "WebSocket 实时聊天接口",
        "authentication": "需要在查询参数中提供 user_id",
        "features": [
            "AI 对话",
            "转人工客服",
            "消息持久化",
            "心跳检测"
        ],
        "message_formats": {
            "send": {
                "type": "message|transfer|ping",
                "content": "消息内容（type=message 时必需）",
                "message_type": "text|image|file（type=message 时可选）"
            },
            "receive": {
                "type": "message|system|error|pong",
                "sender_type": "user|ai|agent|system",
                "content": "消息内容",
                "message_id": "消息ID",
                "timestamp": "ISO 8601 格式时间戳"
            }
        }
    }


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket,
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
):
    """
    WebSocket 实时聊天接口
    
    连接参数:
    - user_id: 用户ID（必需，用于身份验证）
    - session_id: 会话ID（可选，如果不存在则创建新会话）
    
    消息格式:
    发送消息:
    {
        "type": "message",  // 消息类型：message-发送消息, transfer-转人工, ping-心跳
        "content": "用户消息内容",
        "message_type": "text"  // 消息类型：text-文本, image-图片, file-文件
    }
    
    接收消息:
    {
        "type": "message",  // 消息类型：message-普通消息, system-系统消息, error-错误
        "sender_type": "ai",  // 发送者类型：user-用户, ai-AI助手, agent-人工客服, system-系统
        "content": "消息内容",
        "message_id": "消息ID",
        "timestamp": "2024-01-01T00:00:00"
    }
    """
    # 验证 user_id
    if not user_id:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="缺少 user_id")
        return
    
    # 获取或创建会话ID
    if not session_id:
        session_id = f"chat_{uuid.uuid4().hex[:30]}"
    
    # 建立连接
    await manager.connect(websocket, user_id, session_id)
    
    # 获取数据库会话
    from app.db.session import get_session_factory
    session_factory = get_session_factory()
    session = session_factory()
    
    try:
        # 检查会话是否存在，不存在则创建
        check_session_sql = text("""
            SELECT session_id FROM tbkf_chat_session WHERE session_id = :session_id
        """)
        result = await session.execute(check_session_sql, {"session_id": session_id})
        if not result.first():
            # 获取用户信息
            user_sql = text("""
                SELECT user_name FROM sys_user WHERE user_id = :user_id
            """)
            user_result = await session.execute(user_sql, {"user_id": user_id})
            user_row = user_result.mappings().first()
            user_name = user_row["user_name"] if user_row else None
            
            # 创建新会话
            create_session_sql = text("""
                INSERT INTO tbkf_chat_session (
                    session_id, user_id, user_name, chat_type, status
                ) VALUES (
                    :session_id, :user_id, :user_name, 'ai', 'active'
                )
            """)
            await session.execute(create_session_sql, {
                "session_id": session_id,
                "user_id": user_id,
                "user_name": user_name
            })
            await session.commit()
        
        # 发送连接成功消息
        await websocket.send_json({
            "type": "system",
            "sender_type": "system",
            "content": "连接成功",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        })
        
        # 接收消息循环
        while True:
            try:
                # 接收客户端消息
                data = await websocket.receive_json()
                message_type = data.get("type", "message")
                
                if message_type == "ping":
                    # 心跳消息
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    })
                    continue
                
                elif message_type == "message":
                    # 处理用户消息
                    content = data.get("content", "")
                    msg_type = data.get("message_type", "text")
                    
                    if not content:
                        await websocket.send_json({
                            "type": "error",
                            "content": "消息内容不能为空"
                        })
                        continue
                    
                    # 保存用户消息到数据库
                    message_id = f"msg_{uuid.uuid4().hex[:30]}"
                    insert_message_sql = text("""
                        INSERT INTO tbkf_chat_message (
                            message_id, session_id, sender_type, sender_id, sender_name,
                            content, message_type
                        ) VALUES (
                            :message_id, :session_id, 'user', :user_id, :user_name,
                            :content, :message_type
                        )
                    """)
                    user_name = data.get("user_name")
                    await session.execute(insert_message_sql, {
                        "message_id": message_id,
                        "session_id": session_id,
                        "user_id": user_id,
                        "user_name": user_name,
                        "content": content,
                        "message_type": msg_type
                    })
                    await session.commit()
                    
                    # 获取会话信息
                    session_sql = text("""
                        SELECT chat_type, conversation_id, status FROM tbkf_chat_session
                        WHERE session_id = :session_id
                    """)
                    session_result = await session.execute(session_sql, {"session_id": session_id})
                    session_info = session_result.mappings().first()
                    
                    if session_info and session_info["chat_type"] == "ai" and session_info["status"] == "active":
                        # AI 对话模式，调用 AI 接口
                        conversation_id = session_info["conversation_id"]
                        
                        # 如果没有 conversation_id，先创建会话
                        if not conversation_id:
                            conversation_id = await _create_ai_conversation(session)
                            if conversation_id:
                                # 更新会话的 conversation_id
                                update_sql = text("""
                                    UPDATE tbkf_chat_session SET conversation_id = :conversation_id
                                    WHERE session_id = :session_id
                                """)
                                await session.execute(update_sql, {
                                    "conversation_id": conversation_id,
                                    "session_id": session_id
                                })
                                await session.commit()
                        
                        # 调用 AI 接口获取回复
                        ai_response = await _get_ai_response(conversation_id, content)
                        
                        if ai_response:
                            # 保存 AI 回复到数据库
                            ai_message_id = f"msg_{uuid.uuid4().hex[:30]}"
                            insert_ai_sql = text("""
                                INSERT INTO tbkf_chat_message (
                                    message_id, session_id, sender_type, content, message_type
                                ) VALUES (
                                    :message_id, :session_id, 'ai', :content, 'text'
                                )
                            """)
                            await session.execute(insert_ai_sql, {
                                "message_id": ai_message_id,
                                "session_id": session_id,
                                "content": ai_response
                            })
                            await session.commit()
                            
                            # 发送 AI 回复给客户端
                            await websocket.send_json({
                                "type": "message",
                                "sender_type": "ai",
                                "content": ai_response,
                                "message_id": ai_message_id,
                                "timestamp": datetime.now().isoformat()
                            })
                    else:
                        # 人工客服模式，消息需要转发给客服
                        await websocket.send_json({
                            "type": "system",
                            "sender_type": "system",
                            "content": "消息已发送给人工客服，请稍候",
                            "timestamp": datetime.now().isoformat()
                        })
                
                elif message_type == "transfer":
                    # 转人工功能
                    await _transfer_to_human(session, session_id, user_id, websocket)
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"处理消息时出错: {e}", exc_info=True)
                await websocket.send_json({
                    "type": "error",
                    "content": f"处理消息时出错: {str(e)}"
                })
    
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket 连接错误: {e}", exc_info=True)
    finally:
        # 清理连接
        manager.disconnect(user_id)
        await session.close()


async def _create_ai_conversation(session: AsyncSession) -> Optional[str]:
    """创建 AI 对话会话"""
    try:
        base_url, api_key = await get_proxy_config_or_default("default")
        url = f"{base_url.rstrip('/')}/create_conversation"
        
        headers = {
            "Apikey": api_key,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                url,
                headers=headers,
                json={"UserID": "default"}
            )
            response.raise_for_status()
            data = response.json()
            conversation_id = data.get("Conversation", {}).get("AppConversationID")
            return conversation_id
    except Exception as e:
        logger.error(f"创建 AI 会话失败: {e}", exc_info=True)
        return None


async def _get_ai_response(conversation_id: str, user_message: str) -> Optional[str]:
    """获取 AI 回复"""
    try:
        base_url, api_key = await get_proxy_config_or_default("default")
        url = f"{base_url.rstrip('/')}/send_message"
        
        headers = {
            "Apikey": api_key,
            "Content-Type": "application/json"
        }
        
        body = {
            "ConversationID": conversation_id,
            "Message": user_message
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                url,
                headers=headers,
                json=body
            )
            response.raise_for_status()
            data = response.json()
            # 根据实际 API 响应格式提取回复内容
            # 这里需要根据实际的 HiAgent API 响应格式进行调整
            return data.get("Response", {}).get("Message") or data.get("message") or str(data)
    except Exception as e:
        logger.error(f"获取 AI 回复失败: {e}", exc_info=True)
        return None


async def _transfer_to_human(
    session: AsyncSession,
    session_id: str,
    user_id: str,
    websocket: WebSocket
):
    """转人工功能"""
    try:
        # 更新会话状态为已转人工
        update_sql = text("""
            UPDATE tbkf_chat_session
            SET chat_type = 'human', status = 'transferred'
            WHERE session_id = :session_id
        """)
        await session.execute(update_sql, {"session_id": session_id})
        
        # 创建工单
        order_id = f"order_{uuid.uuid4().hex[:24]}"
        order_no = f"WO{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6]}"
        
        # 获取用户信息
        user_sql = text("""
            SELECT user_name FROM sys_user WHERE user_id = :user_id
        """)
        user_result = await session.execute(user_sql, {"user_id": user_id})
        user_row = user_result.mappings().first()
        user_name = user_row["user_name"] if user_row else "用户"
        
        create_order_sql = text("""
            INSERT INTO tbkf_work_order_info (
                order_id, order_no, creator_user_id, creator_name, title, detail, priority, status, expected_time,current_node_id
            ) VALUES (
                :order_id, :order_no, :creator_user_id, :creator_name, :title, :detail, :priority, 'pending', :expected_time,:current_node_id
            )
        """)
        node_id = f"node_{uuid.uuid4().hex[:25]}"
        from datetime import timedelta
        expected_time = datetime.now() + timedelta(hours=24)
        await session.execute(create_order_sql, {
            "order_id": order_id,
            "order_no": order_no,
            "creator_user_id": user_id,
            "creator_name": user_name,
            "title": "用户转人工服务请求",
            "detail": f"会话 {session_id} 的用户请求转人工服务",
            "priority": "high",  # 高优先级
            "expected_time": expected_time,
            "current_node_id":node_id
        })
        
        # 创建初始节点
       
        create_node_sql = text("""
            INSERT INTO tbkf_work_order_node_info (
                node_id, order_id, node_name, node_type, handler_id, handler_name,
                node_status, start_time
            ) VALUES (
                :node_id, :order_id, :node_name, 'create', :handler_id, :handler_name,
                'completed', NOW()
            )
        """)
        await session.execute(create_node_sql, {
            "node_id": node_id,
            "order_id": order_id,
            "node_name": "创建工单",
            "handler_id": user_id,
            "handler_name": user_name
        })
        
        # 更新会话的工单ID
        update_order_sql = text("""
            UPDATE tbkf_chat_session SET order_id = :order_id
            WHERE session_id = :session_id
        """)
        await session.execute(update_order_sql, {
            "order_id": order_id,
            "session_id": session_id
        })
        
        await session.commit()
        
        # 发送系统消息
        system_message_id = f"msg_{uuid.uuid4().hex[:26]}"
        insert_system_sql = text("""
            INSERT INTO tbkf_chat_message (
                message_id, session_id, sender_type, content, message_type
            ) VALUES (
                :message_id, :session_id, 'system', :content, 'system'
            )
        """)
        system_content = f"已为您转接人工客服，工单号：{order_no}，客服将尽快为您服务"
        await session.execute(insert_system_sql, {
            "message_id": system_message_id,
            "session_id": session_id,
            "content": system_content
        })
        await session.commit()
        
        await websocket.send_json({
            "type": "system",
            "sender_type": "system",
            "content": system_content,
            "message_id": system_message_id,
            "order_id": order_id,
            "order_no": order_no,
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"转人工失败: {e}", exc_info=True)
        await websocket.send_json({
            "type": "error",
            "content": f"转人工失败: {str(e)}"
        })


async def _get_customer_service_users(session: AsyncSession) -> list:
    """获取有客服权限的用户ID列表"""
    # 角色表没有数据，直接返回用户表
    sql = text("""
        SELECT DISTINCT u.user_id, u.user_name
        FROM sys_user u
        WHERE u.del_flag = '0' AND u.status = '0'
    """)
    result = await session.execute(sql)
    return [dict(row) for row in result.mappings().all()]


async def _notify_customer_service(session: AsyncSession, session_id: str, user_name: str, content: str):
    """通知客服有新的公开聊天消息"""
    try:
        # 获取有客服权限的用户
        service_users = await _get_customer_service_users(session)
        
        if not service_users:
            logger.warning("没有找到有客服权限的用户")
            return
        
        # 为每个客服创建消息通知
        for service_user in service_users:
            message_id = f"msg_{uuid.uuid4().hex[:30]}"
            insert_sql = text("""
                INSERT INTO tbkf_message_info (
                    message_id, user_id, message_type, title, content, related_id, priority
                ) VALUES (
                    :message_id, :user_id, 'chat_message', :title, :content, :related_id, 'high'
                )
            """)
            await session.execute(insert_sql, {
                "message_id": message_id,
                "user_id": service_user["user_id"],
                "title": f"新的公开聊天消息",
                "content": f"用户 {user_name} 发送了消息：{content[:50]}...",
                "related_id": session_id
            })
            
            # 如果客服在线，通过WebSocket发送实时通知
            if manager.is_connected(service_user["user_id"]):
                await manager.send_personal_message({
                    "type": "chat_notification",
                    "sender_type": "system",
                    "content": f"收到新的公开聊天消息",
                    "session_id": session_id,
                    "user_name": user_name,
                    "message_preview": content[:50],
                    "timestamp": datetime.now().isoformat()
                }, service_user["user_id"])
        
        await session.commit()
    except Exception as e:
        logger.error(f"通知客服失败: {e}", exc_info=True)


@router.websocket("/public/ws")
async def public_websocket_endpoint(
    websocket: WebSocket,
    session_id: Optional[str] = None,
    user_name: Optional[str] = None,
):
    """
    公开聊天 WebSocket 接口（无需认证）
    
    任何用户可以通过该连接发起和客服的聊天
    
    连接参数:
    - session_id: 会话ID（可选，如果不存在则创建新会话）
    - user_name: 用户名称（可选，默认为"访客"）
    
    消息格式同普通聊天接口
    """
    # 生成匿名用户ID
    anonymous_user_id = f"public_{uuid.uuid4().hex[:23]}"
    
    # 获取或创建会话ID
    if not session_id:
        session_id = f"public_chat_{uuid.uuid4().hex[:19]}"
    
    # 设置默认用户名
    if not user_name:
        user_name = "访客"
    
    # 建立连接
    await manager.connect(websocket, anonymous_user_id, session_id)
    
    # 获取数据库会话
    from app.db.session import get_session_factory
    session_factory = get_session_factory()
    session = session_factory()
    
    try:
        # 检查会话是否存在，不存在则创建
        check_session_sql = text("""
            SELECT session_id FROM tbkf_chat_session WHERE session_id = :session_id
        """)
        result = await session.execute(check_session_sql, {"session_id": session_id})
        if not result.first():
            # 创建新公开聊天会话
            create_session_sql = text("""
                INSERT INTO tbkf_chat_session (
                    session_id, user_id, user_name, chat_type, status
                ) VALUES (
                    :session_id, :user_id, :user_name, 'human', 'waiting'
                )
            """)
            await session.execute(create_session_sql, {
                "session_id": session_id,
                "user_id": anonymous_user_id,
                "user_name": user_name
            })
            await session.commit()
        
        # 发送连接成功消息
        await websocket.send_json({
            "type": "system",
            "sender_type": "system",
            "content": "连接成功，等待客服接入",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        })
        
        # 接收消息循环
        while True:
            try:
                # 接收客户端消息
                data = await websocket.receive_json()
                message_type = data.get("type", "message")
                
                if message_type == "ping":
                    # 心跳消息
                    await websocket.send_json({
                        "type": "pong",
                        "timestamp": datetime.now().isoformat()
                    })
                    continue
                
                elif message_type == "message":
                    # 处理用户消息
                    content = data.get("content", "")
                    msg_type = data.get("message_type", "text")
                    
                    if not content:
                        await websocket.send_json({
                            "type": "error",
                            "content": "消息内容不能为空"
                        })
                        continue
                    
                    # 保存用户消息到数据库
                    message_id = f"msg_{uuid.uuid4().hex[:30]}"
                    insert_message_sql = text("""
                        INSERT INTO tbkf_chat_message (
                            message_id, session_id, sender_type, sender_id, sender_name,
                            content, message_type
                        ) VALUES (
                            :message_id, :session_id, 'user', :user_id, :user_name,
                            :content, :message_type
                        )
                    """)
                    await session.execute(insert_message_sql, {
                        "message_id": message_id,
                        "session_id": session_id,
                        "user_id": anonymous_user_id,
                        "user_name": user_name,
                        "content": content,
                        "message_type": msg_type
                    })
                    await session.commit()
                    
                    # 通知客服有新消息
                    await _notify_customer_service(session, session_id, user_name, content)
                    
                    # 检查是否有客服接入
                    session_sql = text("""
                        SELECT agent_id, status FROM tbkf_chat_session
                        WHERE session_id = :session_id
                    """)
                    session_result = await session.execute(session_sql, {"session_id": session_id})
                    session_info = session_result.mappings().first()
                    
                    if session_info and session_info["agent_id"]:
                        # 有客服接入，消息转发给客服
                        agent_id = session_info["agent_id"]
                        if manager.is_connected(agent_id):
                            await manager.send_personal_message({
                                "type": "message",
                                "sender_type": "user",
                                "sender_id": anonymous_user_id,
                                "sender_name": user_name,
                                "content": content,
                                "message_id": message_id,
                                "session_id": session_id,
                                "timestamp": datetime.now().isoformat()
                            }, agent_id)
                    else:
                        # 没有客服接入，提示等待
                        await websocket.send_json({
                            "type": "system",
                            "sender_type": "system",
                            "content": "消息已发送，等待客服接入",
                            "timestamp": datetime.now().isoformat()
                        })
                
            except WebSocketDisconnect:
                break
            except Exception as e:
                logger.error(f"处理消息时出错: {e}", exc_info=True)
                await websocket.send_json({
                    "type": "error",
                    "content": f"处理消息时出错: {str(e)}"
                })
    
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket 连接错误: {e}", exc_info=True)
    finally:
        # 清理连接
        manager.disconnect(anonymous_user_id)
        await session.close()


@router.get(
    "/public/sessions",
    summary="获取待处理的公开聊天会话列表",
    description="获取所有待处理的公开聊天会话列表，仅客服可见。支持按状态筛选（waiting-等待中、active-进行中、closed-已关闭）。默认返回等待中和进行中的会话。每个会话包含最新消息和未读消息数。",
    response_description="返回公开聊天会话列表，包含：会话ID、用户信息、会话状态、接入客服信息、最新消息内容、未读消息数、创建和更新时间等。"
)
async def list_public_sessions(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    status: Optional[str] = Query(None, description="会话状态：waiting-等待中, active-进行中, closed-已关闭"),
    session: AsyncSession = Depends(get_db_session),
    current_user_id: Optional[str] = Query(None, description="当前用户ID"),
) -> dict:
    """
    获取待处理的公开聊天会话列表（仅客服可见）
    
    需要客服权限才能访问
    """
    offset = (page - 1) * page_size
    
    # 构建查询条件
    conditions = ["user_id LIKE 'public_%'"]
    params = {}
    
    if status:
        conditions.append("status = :status")
        params["status"] = status
    else:
        # 默认只显示等待中和进行中的会话
        conditions.append("status IN ('waiting', 'active')")
    
    where_clause = " AND ".join(conditions)
    
    # 查询总数
    count_sql = text(f"SELECT COUNT(*) as total FROM tbkf_chat_session WHERE {where_clause}")
    count_result = await session.execute(count_sql, params)
    total = count_result.scalar()
    
    # 查询列表
    list_sql = text(f"""
        SELECT session_id, user_id, user_name, chat_type, status, agent_id, agent_name,
               create_time, update_time
        FROM tbkf_chat_session
        WHERE {where_clause}
        ORDER BY update_time DESC
        LIMIT :limit OFFSET :offset
    """)
    params.update({"limit": page_size, "offset": offset})
    result = await session.execute(list_sql, params)
    sessions = [dict(row) for row in result.mappings().all()]
    
    # 为每个会话查询最新消息
    for sess in sessions:
        latest_msg_sql = text("""
            SELECT content, create_time
            FROM tbkf_chat_message
            WHERE session_id = :session_id
            ORDER BY create_time DESC
            LIMIT 1
        """)
        msg_result = await session.execute(latest_msg_sql, {"session_id": sess["session_id"]})
        latest_msg = msg_result.mappings().first()
        sess["latest_message"] = latest_msg["content"] if latest_msg else None
        sess["latest_message_time"] = latest_msg["create_time"] if latest_msg else None
        
        # 查询未读消息数
        unread_sql = text("""
            SELECT COUNT(*) as count
            FROM tbkf_chat_message
            WHERE session_id = :session_id AND sender_type = 'user' AND is_read = 0
        """)
        unread_result = await session.execute(unread_sql, {"session_id": sess["session_id"]})
        sess["unread_count"] = unread_result.scalar() or 0
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": sessions
    }


@router.post(
    "/public/sessions/{session_id}/join",
    summary="客服接入公开聊天会话",
    description="客服通过此接口接入指定的公开聊天会话。接入后会话状态会变为'active'，并发送系统消息通知用户客服已接入。只有等待中的会话才能被接入。",
    response_description="返回接入结果，包含会话ID、客服ID和客服姓名。"
)
async def join_public_session(
    session_id: str,
    session: AsyncSession = Depends(get_db_session),
    current_user_id: Optional[str] = Query(None, description="当前用户ID")
) -> dict:
    """
    客服接入公开聊天会话
    
    客服点击消息后，通过此接口接入对应的聊天会话
    """
    # 检查会话是否存在
    check_sql = text("""
        SELECT session_id, user_id, user_name, status, agent_id
        FROM tbkf_chat_session
        WHERE session_id = :session_id AND user_id LIKE 'public_%'
    """)
    result = await session.execute(check_sql, {"session_id": session_id})
    chat_session = result.mappings().first()
    
    if not chat_session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 获取客服信息
    agent_sql = text("""
        SELECT user_name FROM sys_user WHERE user_id = :user_id
    """)
    agent_result = await session.execute(agent_sql, {"user_id": current_user_id})
    agent_row = agent_result.mappings().first()
    agent_name = agent_row["user_name"] if agent_row else "客服"
    
    # 更新会话状态
    update_sql = text("""
        UPDATE tbkf_chat_session
        SET agent_id = :agent_id, agent_name = :agent_name, status = 'active'
        WHERE session_id = :session_id
    """)
    await session.execute(update_sql, {
        "agent_id": current_user_id,
        "agent_name": agent_name,
        "session_id": session_id
    })
    
    # 发送系统消息
    system_message_id = f"msg_{uuid.uuid4().hex[:30]}"
    insert_system_sql = text("""
        INSERT INTO tbkf_chat_message (
            message_id, session_id, sender_type, sender_id, sender_name, content, message_type
        ) VALUES (
            :message_id, :session_id, 'system', :sender_id, :sender_name, :content, 'system'
        )
    """)
    await session.execute(insert_system_sql, {
        "message_id": system_message_id,
        "session_id": session_id,
        "sender_id": current_user_id,
        "sender_name": agent_name,
        "content": f"客服 {agent_name} 已接入"
    })
    
    await session.commit()
    
    # 通知公开用户客服已接入
    public_user_id = chat_session["user_id"]
    if manager.is_connected(public_user_id):
        await manager.send_personal_message({
            "type": "system",
            "sender_type": "system",
            "content": f"客服 {agent_name} 已接入，可以开始对话",
            "session_id": session_id,
            "agent_id": current_user_id,
            "agent_name": agent_name,
            "timestamp": datetime.now().isoformat()
        }, public_user_id)
    
    return {
        "message": "成功接入会话",
        "session_id": session_id,
        "agent_id": current_user_id,
        "agent_name": agent_name
    }


@router.get(
    "/public/sessions/{session_id}/messages",
    summary="获取公开聊天会话的消息列表",
    description="获取指定公开聊天会话的所有消息记录，支持分页查询。只有接入该会话的客服才能查看消息。查看消息后会自动将用户发送的未读消息标记为已读。",
    response_description="返回消息列表及总数，包含每条消息的详细信息（消息ID、发送者、内容、类型、是否已读、时间等）。"
)
async def get_public_session_messages(
    session_id: str,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(50, ge=1, le=100, description="每页数量"),
    session: AsyncSession = Depends(get_db_session),
    current_user_id: Optional[str] = Query(None, description="当前用户ID")
) -> dict:
    """
    获取公开聊天会话的消息列表（客服查看）
    """
    # 检查会话是否存在且是公开聊天
    check_sql = text("""
        SELECT session_id, user_id, user_name, agent_id
        FROM tbkf_chat_session
        WHERE session_id = :session_id AND user_id LIKE 'public_%'
    """)
    result = await session.execute(check_sql, {"session_id": session_id})
    chat_session = result.mappings().first()
    
    if not chat_session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 检查是否是接入的客服
    if chat_session["agent_id"] and chat_session["agent_id"] != current_user_id:
        raise HTTPException(status_code=403, detail="无权访问此会话")
    
    offset = (page - 1) * page_size
    
    # 查询消息
    messages_sql = text("""
        SELECT message_id, session_id, sender_type, sender_id, sender_name,
               content, message_type, is_read, create_time
        FROM tbkf_chat_message
        WHERE session_id = :session_id
        ORDER BY create_time DESC
        LIMIT :limit OFFSET :offset
    """)
    result = await session.execute(messages_sql, {
        "session_id": session_id,
        "limit": page_size,
        "offset": offset
    })
    messages = [dict(row) for row in result.mappings().all()]
    
    # 标记消息为已读
    if messages:
        update_read_sql = text("""
            UPDATE tbkf_chat_message
            SET is_read = 1
            WHERE session_id = :session_id AND sender_type = 'user' AND is_read = 0
        """)
        await session.execute(update_read_sql, {"session_id": session_id})
        await session.commit()
    
    # 查询总数
    count_sql = text("""
        SELECT COUNT(*) as total FROM tbkf_chat_message WHERE session_id = :session_id
    """)
    count_result = await session.execute(count_sql, {"session_id": session_id})
    total = count_result.scalar()
    
    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "items": list(reversed(messages))  # 按时间正序返回
    }


class ReplyRequest(BaseModel):
    """回复请求"""
    content: str = Field(..., description="回复内容", min_length=1)


@router.post(
    "/public/sessions/{session_id}/reply",
    summary="客服回复公开聊天消息",
    description="客服回复公开聊天会话中的消息。回复内容会保存到数据库，并通过WebSocket实时推送给用户。只有已接入该会话的客服才能回复。",
    response_description="返回回复结果，包含消息ID和成功消息。"
)
async def reply_public_session(
    session_id: str,
    reply_data: ReplyRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user_id: Optional[str] = Query(None, description="当前用户ID")
) -> dict:
    """
    客服回复公开聊天消息
    
    客服通过此接口回复公开用户的消息
    """
    # 检查会话是否存在且是公开聊天
    check_sql = text("""
        SELECT session_id, user_id, user_name, agent_id, status
        FROM tbkf_chat_session
        WHERE session_id = :session_id AND user_id LIKE 'public_%'
    """)
    result = await session.execute(check_sql, {"session_id": session_id})
    chat_session = result.mappings().first()
    
    if not chat_session:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    # 检查是否是接入的客服
    if not chat_session["agent_id"] or chat_session["agent_id"] != current_user_id:
        raise HTTPException(status_code=403, detail="无权回复此会话，请先接入会话")
    
    content = reply_data.content
    if not content:
        raise HTTPException(status_code=400, detail="回复内容不能为空")
    
    # 获取客服信息
    agent_sql = text("""
        SELECT user_name FROM sys_user WHERE user_id = :user_id
    """)
    agent_result = await session.execute(agent_sql, {"user_id": current_user_id})
    agent_row = agent_result.mappings().first()
    agent_name = agent_row["user_name"] if agent_row else "客服"
    
    # 保存客服回复到数据库
    message_id = f"msg_{uuid.uuid4().hex[:30]}"
    insert_message_sql = text("""
        INSERT INTO tbkf_chat_message (
            message_id, session_id, sender_type, sender_id, sender_name,
            content, message_type
        ) VALUES (
            :message_id, :session_id, 'agent', :sender_id, :sender_name,
            :content, 'text'
        )
    """)
    await session.execute(insert_message_sql, {
        "message_id": message_id,
        "session_id": session_id,
        "sender_id": current_user_id,
        "sender_name": agent_name,
        "content": content
    })
    await session.commit()
    
    # 通过WebSocket发送给公开用户
    public_user_id = chat_session["user_id"]
    if manager.is_connected(public_user_id):
        await manager.send_personal_message({
            "type": "message",
            "sender_type": "agent",
            "sender_id": current_user_id,
            "sender_name": agent_name,
            "content": content,
            "message_id": message_id,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }, public_user_id)
    
    return {
        "message": "回复成功",
        "message_id": message_id,
        "session_id": session_id
    }



