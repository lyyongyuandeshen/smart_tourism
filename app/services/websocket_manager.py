"""
WebSocket 连接管理器
"""
from typing import Dict
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """WebSocket 连接管理器"""
    
    def __init__(self):
        # 存储活跃连接：{user_id: {"websocket": WebSocket, "session_id": str}}
        self.active_connections: Dict[str, Dict] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str, session_id: str):
        """建立连接"""
        await websocket.accept()
        self.active_connections[user_id] = {
            "websocket": websocket,
            "session_id": session_id
        }
        logger.info(f"用户 {user_id} 已连接，会话ID: {session_id}")
    
    def disconnect(self, user_id: str):
        """断开连接"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            logger.info(f"用户 {user_id} 已断开连接")
    
    def is_connected(self, user_id: str) -> bool:
        """检查用户是否在线"""
        return user_id in self.active_connections
    
    async def send_personal_message(self, message: dict, user_id: str):
        """发送个人消息"""
        if user_id in self.active_connections:
            try:
                websocket = self.active_connections[user_id]["websocket"]
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"发送消息给用户 {user_id} 失败: {e}")
                self.disconnect(user_id)
    
    async def broadcast(self, message: dict):
        """广播消息给所有连接"""
        for user_id in list(self.active_connections.keys()):
            await self.send_personal_message(message, user_id)


# 全局管理器实例
manager = ConnectionManager()
