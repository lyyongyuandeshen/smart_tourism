"""
WebSocket 连接管理器
用于管理所有活跃的 WebSocket 连接
"""
from typing import Dict, Set
from fastapi import WebSocket
import json
import logging

logger = logging.getLogger(__name__)


class ConnectionManager:
    """WebSocket 连接管理器"""
    
    def __init__(self):
        # 存储用户ID到WebSocket连接的映射 {user_id: WebSocket}
        self.active_connections: Dict[str, WebSocket] = {}
        # 存储会话ID到用户ID的映射 {session_id: user_id}
        self.session_to_user: Dict[str, str] = {}
        # 存储用户ID到会话ID的映射 {user_id: session_id}
        self.user_to_session: Dict[str, str] = {}
    
    async def connect(self, websocket: WebSocket, user_id: str, session_id: str):
        """
        建立 WebSocket 连接
        
        Args:
            websocket: WebSocket 连接对象
            user_id: 用户ID
            session_id: 会话ID
        """
        await websocket.accept()
        self.active_connections[user_id] = websocket
        self.session_to_user[session_id] = user_id
        self.user_to_session[user_id] = session_id
        logger.info(f"用户 {user_id} 建立 WebSocket 连接，会话ID: {session_id}")
    
    def disconnect(self, user_id: str):
        """
        断开 WebSocket 连接
        
        Args:
            user_id: 用户ID
        """
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        if user_id in self.user_to_session:
            session_id = self.user_to_session[user_id]
            if session_id in self.session_to_user:
                del self.session_to_user[session_id]
            del self.user_to_session[user_id]
        
        logger.info(f"用户 {user_id} 断开 WebSocket 连接")
    
    async def send_personal_message(self, message: dict, user_id: str):
        """
        向指定用户发送消息
        
        Args:
            message: 消息内容（字典）
            user_id: 目标用户ID
        """
        if user_id in self.active_connections:
            try:
                websocket = self.active_connections[user_id]
                await websocket.send_json(message)
                logger.debug(f"向用户 {user_id} 发送消息: {message}")
            except Exception as e:
                logger.error(f"向用户 {user_id} 发送消息失败: {e}")
                # 连接可能已断开，清理连接
                self.disconnect(user_id)
        else:
            logger.warning(f"用户 {user_id} 不在线，无法发送消息")
    
    async def broadcast(self, message: dict, exclude_user_id: str = None):
        """
        广播消息给所有连接的客户端
        
        Args:
            message: 消息内容（字典）
            exclude_user_id: 排除的用户ID（不发送给该用户）
        """
        disconnected_users = []
        for user_id, websocket in self.active_connections.items():
            if exclude_user_id and user_id == exclude_user_id:
                continue
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"向用户 {user_id} 广播消息失败: {e}")
                disconnected_users.append(user_id)
        
        # 清理断开的连接
        for user_id in disconnected_users:
            self.disconnect(user_id)
    
    def is_connected(self, user_id: str) -> bool:
        """
        检查用户是否在线
        
        Args:
            user_id: 用户ID
            
        Returns:
            bool: 是否在线
        """
        return user_id in self.active_connections
    
    def get_session_id(self, user_id: str) -> str:
        """
        获取用户的会话ID
        
        Args:
            user_id: 用户ID
            
        Returns:
            str: 会话ID，如果不存在返回 None
        """
        return self.user_to_session.get(user_id)
    
    def get_user_id(self, session_id: str) -> str:
        """
        根据会话ID获取用户ID
        
        Args:
            session_id: 会话ID
            
        Returns:
            str: 用户ID，如果不存在返回 None
        """
        return self.session_to_user.get(session_id)


# 全局连接管理器实例
manager = ConnectionManager()

