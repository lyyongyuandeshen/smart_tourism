from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional

from app.models.member_level_models import (
    MemberLevelCreate,
    MemberLevelUpdate,
    MemberLevelResponse,
    MemberLevelQueryRequest,
    MemberLevelListResponse,
    MemberLevelOperationResponse
)
from app.services.member_level_service import MemberLevelService
from app.config.config import config

router = APIRouter()


def get_member_level_service() -> MemberLevelService:
    """获取会员等级服务实例"""
    pool = config.get_mysql_pool()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库连接池未初始化"
        )
    return MemberLevelService(pool)


@router.get("/list", response_model=MemberLevelListResponse)
async def query_member_levels(
    level: Optional[int] = Query(None, ge=1, le=10, description="会员等级（1-10）"),
    keyword: Optional[str] = Query(None, description="关键词（等级名称模糊匹配）"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    member_level_service: MemberLevelService = Depends(get_member_level_service)
):
    """
    查询会员等级列表（支持分页查询）
    
    支持以下查询方式：
    - 全量查询：不传任何参数，返回所有会员等级（分页）
    - 根据等级查询：传入level参数
    - 根据关键词查询：传入keyword参数（支持等级名称模糊匹配）
    - 组合查询：可以同时传入多个参数
    
    Args:
        level: 会员等级（1-10）
        keyword: 关键词（等级名称模糊匹配）
        page: 页码
        page_size: 每页数量
        member_level_service: 会员等级服务实例
        
    Returns:
        会员等级列表响应
    """
    try:
        request = MemberLevelQueryRequest(
            level=level,
            keyword=keyword,
            page=page,
            page_size=page_size
        )
        
        response = member_level_service.query_member_levels(request)
        return response
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/{level_id}", response_model=MemberLevelResponse)
async def get_member_level_detail(
    level_id: str,
    member_level_service: MemberLevelService = Depends(get_member_level_service)
):
    """
    根据会员等级ID查询会员等级详情
    
    Args:
        level_id: 会员等级ID
        member_level_service: 会员等级服务实例
        
    Returns:
        会员等级详情
    """
    try:
        level = member_level_service.get_member_level_by_id(level_id)
        
        if not level:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"会员等级不存在：{level_id}"
            )
        
        return level
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.post("/create", response_model=MemberLevelOperationResponse)
async def create_member_level(
    level: MemberLevelCreate,
    member_level_service: MemberLevelService = Depends(get_member_level_service)
):
    """
    新增会员等级
    
    Args:
        level: 会员等级信息
        member_level_service: 会员等级服务实例
        
    Returns:
        操作响应
    """
    try:
        response = member_level_service.create_member_level(level)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建失败：{str(e)}"
        )


@router.put("/{level_id}", response_model=MemberLevelOperationResponse)
async def update_member_level(
    level_id: str,
    level: MemberLevelUpdate,
    member_level_service: MemberLevelService = Depends(get_member_level_service)
):
    """
    编辑某会员等级字段属性
    
    Args:
        level_id: 会员等级ID
        level: 会员等级更新信息
        member_level_service: 会员等级服务实例
        
    Returns:
        操作响应
    """
    try:
        response = member_level_service.update_member_level(level_id, level)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND if "不存在" in response.message else status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新失败：{str(e)}"
        )


@router.delete("/{level_id}", response_model=MemberLevelOperationResponse)
async def delete_member_level(
    level_id: str,
    member_level_service: MemberLevelService = Depends(get_member_level_service)
):
    """
    删除某积分等级（软删除）
    
    Args:
        level_id: 会员等级ID
        member_level_service: 会员等级服务实例
        
    Returns:
        操作响应
    """
    try:
        response = member_level_service.delete_member_level(level_id)
        
        if not response.success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND if "不存在" in response.message else status.HTTP_400_BAD_REQUEST,
                detail=response.message
            )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除失败：{str(e)}"
        )
