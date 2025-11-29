from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from datetime import date

from app.models.schedule_models import (
    ScheduleCreate,
    ScheduleQueryRequest,
    ScheduleListResponse,
    ScheduleCreateResponse,
    BatchScheduleCreate,
    BatchScheduleCreateResponse,
    EmployeeListResponse,
    PositionListResponse,
    ShiftListResponse,
    ScheduleCalendarResponse,
    ScheduleDetail,
    ManualScheduleCreate,
    ManualScheduleCreateResponse,
    AutoScheduleConfig,
    AutoScheduleCreateResponse
)
from app.services.schedule_service import ScheduleService
from app.config.config import config

router = APIRouter()


def get_schedule_service() -> ScheduleService:
    """获取排班服务实例"""
    pool = config.get_mysql_pool()
    if not pool:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="数据库连接池未初始化"
        )
    return ScheduleService(pool)


# ==================== 基础数据接口 ====================

@router.get("/employees", response_model=EmployeeListResponse)
async def get_all_employees(
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    获取所有员工列表
    
    Returns:
        员工列表响应
    """
    try:
        return schedule_service.get_all_employees()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/positions", response_model=PositionListResponse)
async def get_all_positions(
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    获取所有岗位列表
    
    Returns:
        岗位列表响应
    """
    try:
        return schedule_service.get_all_positions()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/shifts", response_model=ShiftListResponse)
async def get_all_shifts(
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    获取所有班次列表
    
    Returns:
        班次列表响应
    """
    try:
        return schedule_service.get_all_shifts()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


# ==================== 排班查询接口 ====================

@router.get("/list", response_model=ScheduleListResponse)
async def query_schedules(
        start_date: Optional[date] = Query(None, description="开始日期"),
        end_date: Optional[date] = Query(None, description="结束日期"),
        position_id: Optional[int] = Query(None, description="岗位ID"),
        employee_id: Optional[int] = Query(None, description="员工ID"),
        keyword: Optional[str] = Query(None, description="搜索关键词（员工姓名、岗位名称）"),
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    查询排班列表
    
    支持以下查询方式：
    - 按日期范围查询：传入start_date和end_date
    - 按岗位查询：传入position_id
    - 按员工查询：传入employee_id
    - 关键词搜索：传入keyword（搜索员工姓名、岗位名称）
    - 组合查询：可以同时传入多个参数
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        position_id: 岗位ID
        employee_id: 员工ID
        keyword: 搜索关键词
        schedule_service: 排班服务实例
        
    Returns:
        排班列表响应
    """
    try:
        request = ScheduleQueryRequest(
            start_date=start_date,
            end_date=end_date,
            position_id=position_id,
            employee_id=employee_id,
            keyword=keyword
        )

        return schedule_service.query_schedules(request)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/calendar", response_model=ScheduleCalendarResponse)
async def get_calendar_schedules(
        start_date: date = Query(..., description="开始日期"),
        end_date: date = Query(..., description="结束日期"),
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    获取日历视图的排班数据
    
    用于在日历上展示排班信息，按日期分组返回。
    
    Args:
        start_date: 开始日期
        end_date: 结束日期
        schedule_service: 排班服务实例
        
    Returns:
        日历排班响应
    """
    try:
        return schedule_service.get_calendar_schedules(start_date, end_date)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


@router.get("/{schedule_id}", response_model=ScheduleDetail)
async def get_schedule_detail(
        schedule_id: int,
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    获取排班详情
    
    Args:
        schedule_id: 排班ID
        schedule_service: 排班服务实例
        
    Returns:
        排班详情
    """
    try:
        schedule = schedule_service.get_schedule_detail(schedule_id)

        if not schedule:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"排班记录不存在：{schedule_id}"
            )

        return schedule

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"查询失败：{str(e)}"
        )


# ==================== 排班创建接口 ====================

@router.post("/create", response_model=ScheduleCreateResponse)
async def create_schedule(
        schedule: ScheduleCreate,
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    创建单个排班
    
    Args:
        schedule: 排班信息
        schedule_service: 排班服务实例
        
    Returns:
        创建响应
    """
    try:
        response = schedule_service.create_schedule(schedule)

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


@router.post("/batch-create", response_model=BatchScheduleCreateResponse)
async def batch_create_schedules(
        batch_request: BatchScheduleCreate,
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    批量创建排班
    
    用于"新增排班"弹窗，一次性创建多个班次的排班。
    
    Args:
        batch_request: 批量排班请求
        schedule_service: 排班服务实例
        
    Returns:
        批量创建响应
    """
    try:
        response = schedule_service.batch_create_schedules(batch_request)

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
            detail=f"批量创建失败：{str(e)}"
        )


# ==================== 排班更新和删除接口 ====================

@router.put("/{schedule_id}", response_model=ScheduleCreateResponse)
async def update_schedule(
        schedule_id: int,
        schedule: ScheduleCreate,
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    更新排班
    
    Args:
        schedule_id: 排班ID
        schedule: 排班信息
        schedule_service: 排班服务实例
        
    Returns:
        更新响应
    """
    try:
        response = schedule_service.update_schedule(schedule_id, schedule)

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
            detail=f"更新失败：{str(e)}"
        )


@router.delete("/{schedule_id}", response_model=ScheduleCreateResponse)
async def delete_schedule(
        schedule_id: int,
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    删除排班
    
    Args:
        schedule_id: 排班ID
        schedule_service: 排班服务实例
        
    Returns:
        删除响应
    """
    try:
        response = schedule_service.delete_schedule(schedule_id)

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
            detail=f"删除失败：{str(e)}"
        )


# ==================== 手动排班接口 ====================

@router.post("/manual-create", response_model=ManualScheduleCreateResponse)

async def manual_create_schedules(
        manual_request: ManualScheduleCreate,
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    手动创建排班
    
    管理员可以手动选择员工、岗位、班次进行精确排班。
    
    功能特点：
    - 支持批量创建多个排班
    - 可以指定具体的员工和负责人
    - 支持覆盖已存在的排班
    - 提供详细的操作结果反馈
    
    业务规则：
    - 每个岗位每天只能有一个排班
    - 必须指定至少一个员工
    - 负责人必须在员工列表中
    - 可以选择是否覆盖已存在的排班
    
    Args:
        manual_request: 手动排班请求
        schedule_service: 排班服务实例
        
    Returns:
        手动排班创建响应
    """
    try:
        response = schedule_service.manual_create_schedules(manual_request)

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
            detail=f"手动排班失败：{str(e)}"
        )


# ==================== 自动排班接口 ====================

@router.post("/auto-preview", response_model=AutoScheduleCreateResponse)
async def auto_schedule_preview(
        auto_config: AutoScheduleConfig,
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    自动排班预览
    
    根据配置的规则生成排班预览，不实际创建排班记录。
    用于让管理员确认自动排班结果后再决定是否执行。
    
    功能特点：
    - 智能员工分配算法
    - 工作负荷均衡
    - 连续工作天数限制
    - 冲突检测和提示
    
    Args:
        auto_config: 自动排班配置
        schedule_service: 排班服务实例
        
    Returns:
        自动排班预览响应
    """
    try:
        response = schedule_service.auto_create_schedules(auto_config, preview_mode=True)

        return response

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"自动排班预览失败：{str(e)}"
        )


@router.post("/auto-create", response_model=AutoScheduleCreateResponse)
async def auto_create_schedules(
        auto_config: AutoScheduleConfig,
        schedule_service: ScheduleService = Depends(get_schedule_service)
):
    """
    自动创建排班
    
    根据配置的规则自动生成并创建排班记录。
    
    智能排班算法：
    1. 工作负荷均衡：优先分配给工作较少的员工
    2. 连续工作限制：避免员工连续工作过多天数
    3. 休息时间保证：确保员工有足够的休息时间
    4. 岗位需求匹配：根据岗位要求分配合适数量的员工
    5. 负责人自动选择：智能选择合适的员工担任负责人
    
    配置说明：
    - start_date/end_date: 排班时间范围
    - rules: 每个岗位的排班规则
    - max_consecutive_days: 最大连续工作天数
    - min_rest_hours: 最小休息时间
    - balance_workload: 是否启用工作负荷均衡
    - override_existing: 是否覆盖已存在的排班
    
    Args:
        auto_config: 自动排班配置
        schedule_service: 排班服务实例
        
    Returns:
        自动排班创建响应
    """
    try:
        response = schedule_service.auto_create_schedules(auto_config, preview_mode=False)

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
            detail=f"自动排班失败：{str(e)}"
        )
