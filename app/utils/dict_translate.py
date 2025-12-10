"""
字典翻译工具
用于将数据库返回的字典数据进行字段翻译
"""
from typing import Any, Dict, List, Union, Type
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

# 翻译映射表
TRANSLATION_MAPS = {
    "work_order_priority": {
        "1": "低",
        "2": "中",
        "3": "高",
        "4": "紧急"
    },
    "work_order_status": {
        "10": "新建",
        "20": "处理中",
        "30": "待确认",
        "40": "已关闭"
    },
    "work_category": {
        "1": "售后维修",
        "2": "商品咨询",
        "3": "售后服务",
        "4": "退货",
        "99": "其他"
    },
    "work_order_node_type": {
        "创建": "创建",
        "分配": "分配",
        "提交": "提交",
        "转派": "转派",
        "关闭": "关闭"
    }
}


async def translate_response(
    data: Union[Dict, List[Dict]], 
    model: Type[BaseModel] = None
) -> Union[Dict, List[Dict]]:
    """
    翻译响应数据
    
    Args:
        data: 要翻译的数据（字典或字典列表）
        model: Pydantic模型类，用于获取字段的翻译配置
        
    Returns:
        翻译后的数据
    """
    if isinstance(data, list):
        return [await _translate_single(item, model) for item in data]
    else:
        return await _translate_single(data, model)


async def _translate_single(data: Dict, model: Type[BaseModel] = None) -> Dict:
    """翻译单个字典"""
    if not model:
        return data
    
    result = data.copy()
    
    # 遍历模型字段，查找需要翻译的字段
    for field_name, field_info in model.model_fields.items():
        if field_name in result:
            # 检查字段是否有翻译配置
            json_schema_extra = field_info.json_schema_extra or {}
            if isinstance(json_schema_extra, dict) and json_schema_extra.get("is_translate"):
                translation_map_name = json_schema_extra.get("translation_map")
                if translation_map_name and translation_map_name in TRANSLATION_MAPS:
                    # 获取原始值
                    original_value = str(result[field_name])
                    # 翻译
                    translation_map = TRANSLATION_MAPS[translation_map_name]
                    translated_value = translation_map.get(original_value, original_value)
                    # 添加翻译后的字段
                    text_field_name = f"{field_name}_text"
                    result[text_field_name] = translated_value
    
    return result
