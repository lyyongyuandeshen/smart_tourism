"""
字典翻译工具类
用于在返回给前端的接口中，对某些字段进行字典翻译
通过注解标记需要翻译的字段，自动从 Redis 获取字典数据并翻译
"""
import json
from typing import Any, Dict, List, Optional, Set, Union, Type
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo

from app.services.dict_cache import get_dict_data_from_cache


def get_translate_fields(model_class: Type[BaseModel]) -> Dict[str, str]:
    """
    从 Pydantic 模型中提取需要翻译的字段及其对应的字典类型
    
    Args:
        model_class: Pydantic 模型类
        
    Returns:
        Dict[str, str]: 字段名 -> 字典类型的映射
        例如: {"status": "sys_status", "sex": "sys_user_sex"}
    """
    translate_fields = {}
    
    # 遍历模型的所有字段
    for field_name, field_info in model_class.model_fields.items():
        # 检查字段是否有 json_schema_extra 属性
        # Pydantic v2 中，json_schema_extra 可能存储在 FieldInfo 的 json_schema_extra 属性中
        # 或者通过 field_info.json_schema_extra 访问
        extra = None
        
        # 尝试多种方式获取 json_schema_extra
        if hasattr(field_info, "json_schema_extra"):
            extra = field_info.json_schema_extra
        elif isinstance(field_info, FieldInfo):
            # 如果是 FieldInfo 对象，尝试从 json_schema_extra 获取
            if hasattr(field_info, "json_schema_extra"):
                extra = field_info.json_schema_extra
        
        # 如果 extra 是字典，检查是否有翻译标记
        if isinstance(extra, dict):
            # 检查是否有 is_translate 标记
            if extra.get("is_translate") is True:
                # 获取 translation_map（字典类型）
                translation_map = extra.get("translation_map")
                if translation_map:
                    translate_fields[field_name] = translation_map
    
    return translate_fields


# def add_text_fields_to_model(model_class: Type[BaseModel]) -> Type[BaseModel]:
#     """
#     为响应模型自动添加 _text 字段
    
#     扫描模型中的所有字段，如果字段标记了 is_translate=True，
#     则自动添加对应的 _text 字段（如果不存在）
    
#     注意：在 Pydantic v2 中，动态添加字段需要使用 __annotations__ 和 model_fields
    
#     Args:
#         model_class: Pydantic 模型类
        
#     Returns:
#         修改后的模型类（原地修改，也返回类本身）
        
#     示例:
#         class RoleResponse(BaseModel):
#             status: str = Field(..., json_schema_extra={"is_translate": True, "translation_map": "sys_status"})
        
#         # 调用后会自动添加 status_text 字段
#         RoleResponse = add_text_fields_to_model(RoleResponse)
#     """
#     translate_fields = get_translate_fields(model_class)
    
#     # 为每个需要翻译的字段添加对应的 _text 字段
#     for field_name, dict_type in translate_fields.items():
#         text_field_name = f"{field_name}_text"
        
#         # 如果 _text 字段已存在，跳过
#         if text_field_name in model_class.model_fields:
#             continue
        
#         # 更新 __annotations__（Pydantic v2 需要）
#         if not hasattr(model_class, '__annotations__'):
#             model_class.__annotations__ = {}
#         model_class.__annotations__[text_field_name] = Optional[str]
        
#         # 添加字段到 model_fields
#         model_class.model_fields[text_field_name] = FieldInfo(
#             default=None,
#             annotation=Optional[str],
#             description=f"{field_name} 字段的字典翻译值"
#         )
    
#     # 重新构建模型（使新字段生效）
#     model_class.model_rebuild()
    
#     return model_class


async def get_dict_mapping(dict_types: Set[str]) -> Dict[str, Dict[str, str]]:
    """
    批量从 Redis 获取字典数据，构建字典值到标签的映射
    
    Args:
        dict_types: 字典类型集合
        
    Returns:
        Dict[str, Dict[str, str]]: 字典类型 -> {字典值: 字典标签} 的映射
        例如: {
            "sys_status": {"0": "正常", "1": "停用"},
            "sys_user_sex": {"0": "男", "1": "女", "2": "未知"}
        }
    """
    dict_mapping = {}
    
    # 并发获取所有字典数据
    for dict_type in dict_types:
        dict_data_list = await get_dict_data_from_cache(dict_type)
        # 构建字典值到标签的映射
        value_to_label = {}
        for item in dict_data_list:
            dict_value = str(item.get("dict_value", ""))
            dict_label = item.get("dict_label", "")
            if dict_value:
                value_to_label[dict_value] = dict_label
        dict_mapping[dict_type] = value_to_label
    
    return dict_mapping


def translate_object(
    obj: Union[Dict[str, Any], BaseModel],
    translate_fields: Dict[str, str],
    dict_mapping: Dict[str, Dict[str, str]]
) -> Dict[str, Any]:
    """
    翻译单个对象的字段
    
    Args:
        obj: 要翻译的对象（字典或 Pydantic 模型实例）
        translate_fields: 字段名 -> 字典类型的映射
        dict_mapping: 字典类型 -> {字典值: 字典标签} 的映射
        
    Returns:
        Dict[str, Any]: 翻译后的对象（字典格式），新增了翻译字段（原字段名 + "_text"）
    """
    # 如果是 Pydantic 模型，转换为字典
    if isinstance(obj, BaseModel):
        obj_dict = obj.model_dump()
    else:
        obj_dict = obj.copy() if isinstance(obj, dict) else {}
    
    # 遍历需要翻译的字段
    for field_name, dict_type in translate_fields.items():
        # 获取原字段值
        field_value = obj_dict.get(field_name)
        
        # 如果字段值存在，进行翻译
        if field_value is not None:
            # 获取对应的字典映射
            value_to_label = dict_mapping.get(dict_type, {})
            # 将字段值转换为字符串进行匹配
            field_value_str = str(field_value)
            # 获取翻译后的标签
            translated_label = value_to_label.get(field_value_str, field_value_str)
            # 添加翻译字段（原字段名 + "_text"）
            obj_dict[f"{field_name}_text"] = translated_label
        else:
            # 如果字段值为 None，翻译字段也为 None
            obj_dict[f"{field_name}_text"] = None
    
    return obj_dict


async def translate_response(
    data: Union[BaseModel, Dict[str, Any], List[BaseModel], List[Dict[str, Any]]],
    model_class: Optional[Type[BaseModel]] = None
) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
    """
    翻译响应数据中的字典字段
    
    这是主要的公共方法，会自动识别需要翻译的字段，批量获取字典数据，然后进行翻译
    
    Args:
        data: 要翻译的数据，可以是单个对象或对象列表
        model_class: Pydantic 模型类，如果不提供，会尝试从 data 中推断
        
    Returns:
        翻译后的数据，格式与输入相同，但每个对象都新增了翻译字段（原字段名 + "_text"）
        
    示例:
        # 单个对象
        role = RoleResponse(...)
        translated = await translate_response(role, RoleResponse)
        # 结果: {"role_id": "...", "status": "0", "status_text": "正常", ...}
        
        # 对象列表
        roles = [RoleResponse(...), RoleResponse(...)]
        translated = await translate_response(roles, RoleResponse)
        # 结果: [{"role_id": "...", "status": "0", "status_text": "正常", ...}, ...]
    """
    # 确定模型类
    if model_class is None:
        if isinstance(data, BaseModel):
            model_class = type(data)
        elif isinstance(data, list) and len(data) > 0:
            first_item = data[0]
            if isinstance(first_item, BaseModel):
                model_class = type(first_item)
            else:
                # 如果是字典列表，无法自动推断，需要手动指定
                raise ValueError("无法自动推断模型类，请手动指定 model_class 参数")
        else:
            raise ValueError("无法自动推断模型类，请手动指定 model_class 参数")
    
    # 获取需要翻译的字段
    translate_fields = get_translate_fields(model_class)
    
    # 如果没有需要翻译的字段，直接返回
    if not translate_fields:
        if isinstance(data, BaseModel):
            return data.model_dump()
        elif isinstance(data, list):
            return [item.model_dump() if isinstance(item, BaseModel) else item for item in data]
        else:
            return data
    
    # 收集所有需要的字典类型
    dict_types = set(translate_fields.values())
    
    # 批量从 Redis 获取字典数据
    dict_mapping = await get_dict_mapping(dict_types)
    
    # 翻译数据
    if isinstance(data, list):
        # 列表：翻译每个对象
        return [translate_object(item, translate_fields, dict_mapping) for item in data]
    else:
        # 单个对象
        return translate_object(data, translate_fields, dict_mapping)

