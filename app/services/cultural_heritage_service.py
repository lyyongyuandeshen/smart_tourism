from typing import List, Optional
from mysql.connector import pooling

from app.repository.cultural_heritage_repo import CulturalHeritageRepository
from app.models.cultural_heritage_models import (
    CulturalHeritageResponse,
    CulturalHeritageCreate,
    CulturalHeritageQueryRequest,
    CulturalHeritageListResponse,
    CulturalHeritageUploadResponse,
    CulturalHeritageDeleteResponse
)


class CulturalHeritageService:
    """文化遗产业务服务类"""

    def __init__(self, pool: pooling.MySQLConnectionPool):
        self.heritage_repo = CulturalHeritageRepository(pool)

    def query_cultural_heritages(self, request: CulturalHeritageQueryRequest) -> CulturalHeritageListResponse:
        """
        查询文化遗产列表
        
        Args:
            request: 查询请求参数
            
        Returns:
            文化遗产列表响应
        """
        try:
            # 计算偏移量
            offset = (request.page - 1) * request.page_size
            
            # 查询文化遗产列表
            heritages = self.heritage_repo.get_cultural_heritages(
                file_id=request.file_id,
                file_name=request.file_name,
                file_type=request.file_type,
                tag=request.tag,
                offset=offset,
                limit=request.page_size
            )
            
            # 查询总数
            total = self.heritage_repo.count_cultural_heritages(
                file_id=request.file_id,
                file_name=request.file_name,
                file_type=request.file_type,
                tag=request.tag
            )
            
            # 转换为响应模型
            heritage_list = [
                CulturalHeritageResponse(
                    file_id=h['file_id'],
                    file_name=h['file_name'],
                    file_type=h['file_type'],
                    tag=h['tag'],
                    url=h['url'],
                    created_at=h['created_at'],
                    updated_at=h['updated_at']
                )
                for h in heritages
            ]
            
            return CulturalHeritageListResponse(
                success=True,
                message="查询成功",
                total=total,
                page=request.page,
                page_size=request.page_size,
                data=heritage_list
            )
            
        except Exception as e:
            return CulturalHeritageListResponse(
                success=False,
                message=f"查询失败：{str(e)}",
                total=0,
                page=request.page,
                page_size=request.page_size,
                data=[]
            )

    def upload_cultural_heritage(self, heritage: CulturalHeritageCreate) -> CulturalHeritageUploadResponse:
        """
        上传（创建或更新）文化遗产信息
        
        Args:
            heritage: 文化遗产信息
            
        Returns:
            上传响应
        """
        try:
            # 检查文化遗产是否已存在
            existing_heritage = self.heritage_repo.get_cultural_heritage_by_id(heritage.file_id)
            
            heritage_data = {
                'file_id': heritage.file_id,
                'file_name': heritage.file_name,
                'file_type': heritage.file_type,
                'tag': heritage.tag,
                'url': heritage.url
            }
            
            if existing_heritage:
                # 更新现有文化遗产
                rows_affected = self.heritage_repo.update_cultural_heritage(
                    heritage.file_id,
                    heritage_data
                )
                
                if rows_affected > 0:
                    return CulturalHeritageUploadResponse(
                        success=True,
                        message="文化遗产信息更新成功",
                        file_id=heritage.file_id
                    )
                else:
                    return CulturalHeritageUploadResponse(
                        success=False,
                        message="文化遗产信息更新失败"
                    )
            else:
                # 创建新文化遗产
                rows_affected = self.heritage_repo.create_cultural_heritage(heritage_data)
                
                if rows_affected > 0:
                    return CulturalHeritageUploadResponse(
                        success=True,
                        message="文化遗产信息创建成功",
                        file_id=heritage.file_id
                    )
                else:
                    return CulturalHeritageUploadResponse(
                        success=False,
                        message="文化遗产信息创建失败"
                    )
                    
        except Exception as e:
            return CulturalHeritageUploadResponse(
                success=False,
                message=f"操作失败：{str(e)}"
            )

    def get_cultural_heritage_by_id(self, file_id: str) -> Optional[CulturalHeritageResponse]:
        """
        根据文件ID查询文化遗产详情
        
        Args:
            file_id: 文件ID
            
        Returns:
            文化遗产详情
        """
        try:
            heritage = self.heritage_repo.get_cultural_heritage_by_id(file_id)
            
            if not heritage:
                return None
            
            return CulturalHeritageResponse(
                file_id=heritage['file_id'],
                file_name=heritage['file_name'],
                file_type=heritage['file_type'],
                tag=heritage['tag'],
                url=heritage['url'],
                created_at=heritage['created_at'],
                updated_at=heritage['updated_at']
            )
            
        except Exception as e:
            return None

    def delete_cultural_heritage(self, file_id: str) -> CulturalHeritageDeleteResponse:
        """
        删除文化遗产信息
        
        Args:
            file_id: 文件ID
            
        Returns:
            删除响应
        """
        try:
            # 检查文化遗产是否存在
            existing_heritage = self.heritage_repo.get_cultural_heritage_by_id(file_id)
            
            if not existing_heritage:
                return CulturalHeritageDeleteResponse(
                    success=False,
                    message=f"文化遗产不存在：{file_id}"
                )
            
            # 删除文化遗产
            rows_affected = self.heritage_repo.delete_cultural_heritage(file_id)
            
            if rows_affected > 0:
                return CulturalHeritageDeleteResponse(
                    success=True,
                    message="文化遗产删除成功",
                    file_id=file_id
                )
            else:
                return CulturalHeritageDeleteResponse(
                    success=False,
                    message="文化遗产删除失败"
                )
                
        except Exception as e:
            return CulturalHeritageDeleteResponse(
                success=False,
                message=f"删除失败：{str(e)}"
            )
