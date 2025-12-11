"""
字典缓存服务
将字典数据加载到 Redis 中，提高查询性能
"""
import json
from typing import Dict, List, Optional, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session_factory
from app.services.redis import get_redis_client


async def load_dict_to_redis(session: AsyncSession) -> Dict[str, int]:
    """
    加载字典数据到 Redis
    
    Returns:
        Dict[str, int]: 加载结果，key 为 dict_type，value 为加载的数据条数
    """
    redis = await get_redis_client()
    
    # 查询所有启用的字典类型
    type_sql = text("""
        SELECT dict_type
        FROM sys_dict_type
        WHERE status = '0'
    """)
    type_result = await session.execute(type_sql)
    dict_types = [row[0] for row in type_result.all()]
    
    # 一次性查询所有启用的字典数据
    data_sql = text("""
        SELECT dict_code, dict_sort, dict_label, dict_value, dict_type,
               css_class, list_class, is_default, status, remark
        FROM sys_dict_data
        WHERE status = '0'
        ORDER BY dict_type ASC, dict_sort ASC, dict_code ASC
    """)
    data_result = await session.execute(data_sql)
    all_dict_data = [dict(row) for row in data_result.mappings().all()]
    
    # 按 dict_type 分组
    dict_data_by_type: Dict[str, List[Dict[str, Any]]] = {}
    for data in all_dict_data:
        dict_type = data["dict_type"]
        if dict_type not in dict_data_by_type:
            dict_data_by_type[dict_type] = []
        dict_data_by_type[dict_type].append(data)
    
    load_result = {}
    
    # 为每个字典类型存储数据到 Redis
    for dict_type in dict_types:
        dict_data_list = dict_data_by_type.get(dict_type, [])
        
        # 存储到 Redis，key 格式：dict:data:{dict_type}
        redis_key = f"dict:data:{dict_type}"
        if dict_data_list:
            # 转换为 JSON 字符串存储
            await redis.set(redis_key, json.dumps(dict_data_list, ensure_ascii=False, default=str))
            load_result[dict_type] = len(dict_data_list)
        else:
            # 如果没有数据，删除 Redis 中的 key（如果存在）
            await redis.delete(redis_key)
            load_result[dict_type] = 0
    
    return load_result


async def refresh_dict_cache() -> Dict[str, int]:
    """
    刷新字典缓存（从数据库重新加载到 Redis）
    
    Returns:
        Dict[str, int]: 刷新结果，key 为 dict_type，value 为加载的数据条数
    """
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            result = await load_dict_to_redis(session)
            return result
        except Exception as e:
            print(f"[字典缓存] 刷新字典缓存时出错: {str(e)}")
            raise


async def get_dict_data_from_cache(dict_type: str) -> List[Dict[str, Any]]:
    """
    从 Redis 缓存中获取字典数据
    
    Args:
        dict_type: 字典类型
        
    Returns:
        List[Dict[str, Any]]: 字典数据列表，如果不存在返回空列表
    """
    redis = await get_redis_client()
    redis_key = f"dict:data:{dict_type}"
    
    cached_data = await redis.get(redis_key)
    if cached_data:
        return json.loads(cached_data)
    return []


async def init_dict_cache() -> None:
    """
    初始化字典缓存（应用启动时调用）
    """
    try:
        session_factory = get_session_factory()
        async with session_factory() as session:
            result = await load_dict_to_redis(session)
            total_types = len(result)
            total_data = sum(result.values())
            print(f"[字典缓存] 字典缓存初始化完成，加载 {total_types} 个字典类型，共 {total_data} 条数据")
    except Exception as e:
        print(f"[字典缓存] 初始化字典缓存时出错: {str(e)}")
        # 不抛出异常，避免影响应用启动

