from typing import List, Optional
from mysql.connector import pooling

from app.repository.facility_repo import FacilityRepository
from app.models.facility_models import (
    FacilityResponse,
    FacilityCreate,
    FacilityQueryRequest,
    FacilityListResponse,
    FacilityUploadResponse,
    FacilityDeleteResponse
)


class FacilityService:
    """景区设备业务服务类"""

    def __init__(self, pool: pooling.MySQLConnectionPool):
        self.facility_repo = FacilityRepository(pool)

    def query_facilities(self, request: FacilityQueryRequest) -> FacilityListResponse:
        """
        查询设备列表
        
        Args:
            request: 查询请求参数
            
        Returns:
            设备列表响应
        """
        try:
            # 计算偏移量
            offset = (request.page - 1) * request.page_size
            
            # 查询设备列表
            facilities = self.facility_repo.get_facilities(
                facility_id=request.facility_id,
                facility_name=request.facility_name,
                category=request.category,
                status=request.status,
                offset=offset,
                limit=request.page_size
            )
            
            # 查询总数
            total = self.facility_repo.count_facilities(
                facility_id=request.facility_id,
                facility_name=request.facility_name,
                category=request.category,
                status=request.status
            )
            
            # 转换为响应模型
            facility_list = [
                FacilityResponse(
                    facility_id=f['facility_id'],
                    facility_name=f['facility_name'],
                    category=f['category'],
                    icon=f.get('icon'),
                    position_desc=f['position_desc'],
                    longitude=f.get('longitude'),
                    latitude=f.get('latitude'),
                    status=f['status'],
                    created_at=f['created_at'],
                    updated_at=f['updated_at']
                )
                for f in facilities
            ]
            
            return FacilityListResponse(
                success=True,
                message="查询成功",
                total=total,
                page=request.page,
                page_size=request.page_size,
                data=facility_list
            )
            
        except Exception as e:
            return FacilityListResponse(
                success=False,
                message=f"查询失败：{str(e)}",
                total=0,
                page=request.page,
                page_size=request.page_size,
                data=[]
            )

    def upload_facility(self, facility: FacilityCreate) -> FacilityUploadResponse:
        """
        上传（创建或更新）设备信息
        
        Args:
            facility: 设备信息
            
        Returns:
            上传响应
        """
        try:
            # 检查设备是否已存在
            existing_facility = self.facility_repo.get_facility_by_id(facility.facility_id)
            
            facility_data = {
                'facility_id': facility.facility_id,
                'facility_name': facility.facility_name,
                'category': facility.category,
                'icon': facility.icon,
                'position_desc': facility.position_desc,
                'longitude': facility.longitude,
                'latitude': facility.latitude,
                'status': facility.status
            }
            
            if existing_facility:
                # 更新现有设备
                rows_affected = self.facility_repo.update_facility(
                    facility.facility_id,
                    facility_data
                )
                
                if rows_affected > 0:
                    return FacilityUploadResponse(
                        success=True,
                        message="设备信息更新成功",
                        facility_id=facility.facility_id
                    )
                else:
                    return FacilityUploadResponse(
                        success=False,
                        message="设备信息更新失败"
                    )
            else:
                # 创建新设备
                rows_affected = self.facility_repo.create_facility(facility_data)
                
                if rows_affected > 0:
                    return FacilityUploadResponse(
                        success=True,
                        message="设备信息创建成功",
                        facility_id=facility.facility_id
                    )
                else:
                    return FacilityUploadResponse(
                        success=False,
                        message="设备信息创建失败"
                    )
                    
        except Exception as e:
            return FacilityUploadResponse(
                success=False,
                message=f"操作失败：{str(e)}"
            )

    def get_facility_by_id(self, facility_id: str) -> Optional[FacilityResponse]:
        """
        根据设备ID查询设备详情
        
        Args:
            facility_id: 设备ID
            
        Returns:
            设备详情
        """
        try:
            facility = self.facility_repo.get_facility_by_id(facility_id)
            
            if not facility:
                return None
            
            return FacilityResponse(
                facility_id=facility['facility_id'],
                facility_name=facility['facility_name'],
                category=facility['category'],
                icon=facility.get('icon'),
                position_desc=facility['position_desc'],
                longitude=facility.get('longitude'),
                latitude=facility.get('latitude'),
                status=facility['status'],
                created_at=facility['created_at'],
                updated_at=facility['updated_at']
            )
            
        except Exception as e:
            return None

    def delete_facility(self, facility_id: str) -> FacilityDeleteResponse:
        """
        删除设备信息
        
        Args:
            facility_id: 设备ID
            
        Returns:
            删除响应
        """
        try:
            # 检查设备是否存在
            existing_facility = self.facility_repo.get_facility_by_id(facility_id)
            
            if not existing_facility:
                return FacilityDeleteResponse(
                    success=False,
                    message=f"设备不存在：{facility_id}"
                )
            
            # 删除设备
            rows_affected = self.facility_repo.delete_facility(facility_id)
            
            if rows_affected > 0:
                return FacilityDeleteResponse(
                    success=True,
                    message="设备删除成功",
                    facility_id=facility_id
                )
            else:
                return FacilityDeleteResponse(
                    success=False,
                    message="设备删除失败"
                )
                
        except Exception as e:
            return FacilityDeleteResponse(
                success=False,
                message=f"删除失败：{str(e)}"
            )
