from typing import Optional
import uuid
from mysql.connector import pooling

from app.repository.member_level_repo import MemberLevelRepository
from app.models.member_level_models import (
    MemberLevelResponse,
    MemberLevelCreate,
    MemberLevelUpdate,
    MemberLevelQueryRequest,
    MemberLevelListResponse,
    MemberLevelOperationResponse
)


class MemberLevelService:
    """会员等级业务服务类"""

    def __init__(self, pool: pooling.MySQLConnectionPool):
        self.member_level_repo = MemberLevelRepository(pool)

    def query_member_levels(self, request: MemberLevelQueryRequest) -> MemberLevelListResponse:
        """
        查询会员等级列表
        
        Args:
            request: 查询请求参数
            
        Returns:
            会员等级列表响应
        """
        try:
            # 计算偏移量
            offset = (request.page - 1) * request.page_size
            
            # 查询会员等级列表
            levels = self.member_level_repo.get_member_levels(
                level=request.level,
                keyword=request.keyword,
                offset=offset,
                limit=request.page_size
            )
            
            # 查询总数
            total = self.member_level_repo.count_member_levels(
                level=request.level,
                keyword=request.keyword
            )
            
            # 转换为响应模型
            level_list = [
                MemberLevelResponse(
                    id=lv['id'],
                    level=lv['level'],
                    level_name=lv['level_name'],
                    points_min=lv['points_min'],
                    points_max=lv['points_max'],
                    discount_rate=lv['discount_rate'],
                    priority_booking=bool(lv['priority_booking']),
                    is_deleted=lv['is_deleted'],
                    create_time=lv['create_time'],
                    update_time=lv['update_time']
                )
                for lv in levels
            ]
            
            return MemberLevelListResponse(
                success=True,
                message="查询成功",
                total=total,
                page=request.page,
                page_size=request.page_size,
                data=level_list
            )
            
        except Exception as e:
            return MemberLevelListResponse(
                success=False,
                message=f"查询失败：{str(e)}",
                total=0,
                page=request.page,
                page_size=request.page_size,
                data=[]
            )

    def create_member_level(self, level: MemberLevelCreate) -> MemberLevelOperationResponse:
        """
        创建会员等级
        
        Args:
            level: 会员等级信息
            
        Returns:
            操作响应
        """
        try:
            # 检查等级是否已存在
            existing_level = self.member_level_repo.get_member_level_by_level(level.level)
            
            if existing_level:
                return MemberLevelOperationResponse(
                    success=False,
                    message=f"等级 {level.level} 已存在"
                )
            
            # 验证积分范围
            if level.points_min >= level.points_max:
                return MemberLevelOperationResponse(
                    success=False,
                    message="积分下限必须小于积分上限"
                )

            level_data = {
                'level': level.level,
                'level_name': level.level_name,
                'points_min': level.points_min,
                'points_max': level.points_max,
                'discount_rate': level.discount_rate,
                'priority_booking': 1 if level.priority_booking else 0
            }
            
            # 创建会员等级
            rows_affected = self.member_level_repo.create_member_level(level_data)
            
            if rows_affected > 0:
                return MemberLevelOperationResponse(
                    success=True,
                    message="会员等级创建成功",
                )
            else:
                return MemberLevelOperationResponse(
                    success=False,
                    message="会员等级创建失败"
                )
                    
        except Exception as e:
            return MemberLevelOperationResponse(
                success=False,
                message=f"操作失败：{str(e)}"
            )

    def update_member_level(self, level_id: str, level: MemberLevelUpdate) -> MemberLevelOperationResponse:
        """
        更新会员等级信息
        
        Args:
            level_id: 会员等级ID
            level: 会员等级更新信息
            
        Returns:
            操作响应
        """
        try:
            # 检查会员等级是否存在
            existing_level = self.member_level_repo.get_member_level_by_id(level_id)
            
            if not existing_level:
                return MemberLevelOperationResponse(
                    success=False,
                    message=f"会员等级不存在：{level_id}"
                )
            
            # 构建更新数据
            level_data = {}
            
            if level.level_name is not None:
                level_data['level_name'] = level.level_name
            
            if level.points_min is not None:
                level_data['points_min'] = level.points_min
            
            if level.points_max is not None:
                level_data['points_max'] = level.points_max
            
            if level.discount_rate is not None:
                level_data['discount_rate'] = level.discount_rate
            
            if level.priority_booking is not None:
                level_data['priority_booking'] = 1 if level.priority_booking else 0
            
            # 验证积分范围
            points_min = level_data.get('points_min', existing_level['points_min'])
            points_max = level_data.get('points_max', existing_level['points_max'])
            
            if points_min >= points_max:
                return MemberLevelOperationResponse(
                    success=False,
                    message="积分下限必须小于积分上限"
                )
            
            if not level_data:
                return MemberLevelOperationResponse(
                    success=False,
                    message="没有需要更新的字段"
                )
            
            # 更新会员等级
            rows_affected = self.member_level_repo.update_member_level(level_id, level_data)
            
            if rows_affected > 0:
                return MemberLevelOperationResponse(
                    success=True,
                    message="会员等级更新成功",
                    level_id=level_id
                )
            else:
                return MemberLevelOperationResponse(
                    success=False,
                    message="会员等级更新失败"
                )
                
        except Exception as e:
            return MemberLevelOperationResponse(
                success=False,
                message=f"更新失败：{str(e)}"
            )

    def get_member_level_by_id(self, level_id: str) -> Optional[MemberLevelResponse]:
        """
        根据会员等级ID查询会员等级详情
        
        Args:
            level_id: 会员等级ID
            
        Returns:
            会员等级详情
        """
        try:
            level = self.member_level_repo.get_member_level_by_id(level_id)
            
            if not level:
                return None
            
            return MemberLevelResponse(
                id=level['id'],
                level=level['level'],
                level_name=level['level_name'],
                points_min=level['points_min'],
                points_max=level['points_max'],
                discount_rate=level['discount_rate'],
                priority_booking=bool(level['priority_booking']),
                is_deleted=level['is_deleted'],
                create_time=level['create_time'],
                update_time=level['update_time']
            )
            
        except Exception as e:
            return None

    def delete_member_level(self, level_id: str) -> MemberLevelOperationResponse:
        """
        删除会员等级信息（软删除）
        
        Args:
            level_id: 会员等级ID
            
        Returns:
            操作响应
        """
        try:
            # 检查会员等级是否存在
            existing_level = self.member_level_repo.get_member_level_by_id(level_id)
            
            if not existing_level:
                return MemberLevelOperationResponse(
                    success=False,
                    message=f"会员等级不存在：{level_id}"
                )
            
            # 软删除会员等级
            rows_affected = self.member_level_repo.soft_delete_member_level(level_id)
            
            if rows_affected > 0:
                return MemberLevelOperationResponse(
                    success=True,
                    message="会员等级删除成功",
                    level_id=level_id
                )
            else:
                return MemberLevelOperationResponse(
                    success=False,
                    message="会员等级删除失败"
                )
                
        except Exception as e:
            return MemberLevelOperationResponse(
                success=False,
                message=f"删除失败：{str(e)}"
            )
