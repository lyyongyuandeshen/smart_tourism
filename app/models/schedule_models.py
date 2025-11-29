from __future__ import annotations
from datetime import datetime, date, time
from typing import Optional, List
from pydantic import BaseModel, Field


# ==================== 员工模型 ====================
class EmployeeBase(BaseModel):
    """员工基础模型"""
    name: str = Field(description="员工姓名")
    employee_code: str = Field(description="员工编号")
    phone: Optional[str] = Field(None, description="联系电话")


class EmployeeCreate(EmployeeBase):
    """创建员工请求模型"""
    pass


class EmployeeResponse(EmployeeBase):
    """员工响应模型"""
    employee_id: int = Field(description="员工ID")
    created_at: datetime = Field(description="创建时间")

    class Config:
        from_attributes = True


# ==================== 岗位模型 ====================
class PositionBase(BaseModel):
    """岗位基础模型"""
    position_name: str = Field(description="岗位名称")
    description: Optional[str] = Field(None, description="岗位描述")


class PositionCreate(PositionBase):
    """创建岗位请求模型"""
    pass


class PositionResponse(PositionBase):
    """岗位响应模型"""
    position_id: int = Field(description="岗位ID")
    created_at: datetime = Field(description="创建时间")

    class Config:
        from_attributes = True


# ==================== 班次模板模型 ====================
class ShiftBase(BaseModel):
    """班次基础模型"""
    shift_name: str = Field(description="班次名称")
    start_time: str = Field(description="开始时间 HH:MM:SS")
    end_time: str = Field(description="结束时间 HH:MM:SS")
    position_id: Optional[int] = Field(None, description="关联岗位ID")


class ShiftCreate(ShiftBase):
    """创建班次请求模型"""
    pass


class ShiftResponse(ShiftBase):
    """班次响应模型"""
    shift_id: int = Field(description="班次ID")
    created_at: datetime = Field(description="创建时间")
    position_name: Optional[str] = Field(None, description="岗位名称")

    class Config:
        from_attributes = True


# ==================== 排班员工关联模型 ====================
class ScheduleEmployeeBase(BaseModel):
    """排班员工基础模型"""
    employee_id: int = Field(description="员工ID")
    is_leader: bool = Field(False, description="是否为负责人")


class ScheduleEmployeeDetail(ScheduleEmployeeBase):
    """排班员工详情模型"""
    employee_name: str = Field(description="员工姓名")
    employee_code: str = Field(description="员工编号")


# ==================== 排班记录模型 ====================
class ScheduleBase(BaseModel):
    """排班基础模型"""
    schedule_date: date = Field(description="排班日期")
    shift_id: int = Field(description="班次ID")
    position_id: int = Field(description="岗位ID")


class ScheduleCreate(BaseModel):
    """创建排班请求模型（单个排班）"""
    schedule_date: date = Field(description="排班日期")
    shift_id: int = Field(description="班次ID")
    position_id: int = Field(description="岗位ID")
    employees: List[ScheduleEmployeeBase] = Field(description="员工列表")


class ScheduleDetail(BaseModel):
    """排班详情模型"""
    schedule_id: int = Field(description="排班ID")
    schedule_date: date = Field(description="排班日期")
    shift_id: int = Field(description="班次ID")
    shift_name: str = Field(description="班次名称")
    start_time: str = Field(description="开始时间")
    end_time: str = Field(description="结束时间")
    position_id: int = Field(description="岗位ID")
    position_name: str = Field(description="岗位名称")
    employees: List[ScheduleEmployeeDetail] = Field(description="员工列表")
    created_at: datetime = Field(description="创建时间")


# ==================== 批量排班模型 ====================
class BatchScheduleItem(BaseModel):
    """批量排班项"""
    shift_name: str = Field(description="班次名称（如：班次1、班次2）")
    work_content: str = Field(description="工作内容")
    shift_time: str = Field(description="班次时间（如：08:00-17:00）")
    employees: List[ScheduleEmployeeBase] = Field(description="员工列表")


class BatchScheduleCreate(BaseModel):
    """批量创建排班请求模型"""
    schedule_date: date = Field(description="排班日期")
    position_id: int = Field(description="岗位ID")
    schedules: List[BatchScheduleItem] = Field(description="排班列表")


# ==================== 查询模型 ====================
class ScheduleQueryRequest(BaseModel):
    """排班查询请求模型"""
    start_date: Optional[date] = Field(None, description="开始日期")
    end_date: Optional[date] = Field(None, description="结束日期")
    position_id: Optional[int] = Field(None, description="岗位ID")
    employee_id: Optional[int] = Field(None, description="员工ID")
    keyword: Optional[str] = Field(None, description="搜索关键词（员工姓名、岗位名称）")


class CalendarScheduleItem(BaseModel):
    """日历排班项"""
    schedule_id: int = Field(description="排班ID")
    position_name: str = Field(description="岗位名称")
    shift_name: str = Field(description="班次名称")
    start_time: str = Field(description="开始时间")
    end_time: str = Field(description="结束时间")
    employee_names: str = Field(description="员工姓名列表（逗号分隔）")


class CalendarDaySchedule(BaseModel):
    """日历某天的排班"""
    schedule_date: date = Field(description="日期")
    schedules: List[CalendarScheduleItem] = Field(description="当天排班列表")


class ScheduleCalendarResponse(BaseModel):
    """排班日历响应模型"""
    success: bool
    message: str
    data: List[CalendarDaySchedule] = Field(description="日历排班数据")


# ==================== 响应模型 ====================
class ScheduleListResponse(BaseModel):
    """排班列表响应模型"""
    success: bool
    message: str
    total: int = Field(description="总记录数")
    data: List[ScheduleDetail] = Field(description="排班列表")


class ScheduleCreateResponse(BaseModel):
    """排班创建响应模型"""
    success: bool
    message: str
    schedule_id: Optional[int] = None


class BatchScheduleCreateResponse(BaseModel):
    """批量排班创建响应模型"""
    success: bool
    message: str
    created_count: int = Field(0, description="成功创建的排班数量")
    schedule_ids: List[int] = Field(default_factory=list, description="创建的排班ID列表")


# ==================== 手动排班模型 ====================
class ManualScheduleItem(BaseModel):
    """手动排班项"""
    schedule_date: date = Field(description="排班日期")
    shift_id: int = Field(description="班次ID")
    position_id: int = Field(description="岗位ID")
    employee_ids: List[int] = Field(description="员工ID列表")
    leader_employee_id: Optional[int] = Field(None, description="负责人员工ID")
    notes: Optional[str] = Field(None, description="备注")


class ManualScheduleCreate(BaseModel):
    """手动排班创建请求模型"""
    schedules: List[ManualScheduleItem] = Field(description="排班列表")
    override_existing: bool = Field(False, description="是否覆盖已存在的排班")


class ManualScheduleCreateResponse(BaseModel):
    """手动排班创建响应模型"""
    success: bool
    message: str
    created_count: int = Field(0, description="成功创建的排班数量")
    updated_count: int = Field(0, description="更新的排班数量")
    skipped_count: int = Field(0, description="跳过的排班数量")
    schedule_ids: List[int] = Field(default_factory=list, description="创建/更新的排班ID列表")
    details: List[str] = Field(default_factory=list, description="详细信息")


# ==================== 自动排班模型 ====================
class AutoScheduleRule(BaseModel):
    """自动排班规则"""
    position_id: int = Field(description="岗位ID")
    required_employees: int = Field(description="所需员工数量")
    preferred_shift_ids: List[int] = Field(description="优先班次ID列表")
    exclude_employee_ids: List[int] = Field(default_factory=list, description="排除的员工ID列表")
    require_leader: bool = Field(True, description="是否需要负责人")


class AutoScheduleConfig(BaseModel):
    """自动排班配置"""
    start_date: date = Field(description="开始日期")
    end_date: date = Field(description="结束日期")
    rules: List[AutoScheduleRule] = Field(description="排班规则列表")
    max_consecutive_days: int = Field(5, description="最大连续工作天数")
    min_rest_hours: int = Field(12, description="最小休息时间（小时）")
    balance_workload: bool = Field(True, description="是否均衡工作负荷")
    override_existing: bool = Field(False, description="是否覆盖已存在的排班")


class AutoSchedulePreview(BaseModel):
    """自动排班预览"""
    schedule_date: date = Field(description="排班日期")
    position_name: str = Field(description="岗位名称")
    shift_name: str = Field(description="班次名称")
    employee_names: List[str] = Field(description="员工姓名列表")
    leader_name: Optional[str] = Field(None, description="负责人姓名")
    conflict_reason: Optional[str] = Field(None, description="冲突原因")


class AutoScheduleCreateResponse(BaseModel):
    """自动排班创建响应模型"""
    success: bool
    message: str
    preview_mode: bool = Field(False, description="是否为预览模式")
    created_count: int = Field(0, description="成功创建的排班数量")
    conflict_count: int = Field(0, description="冲突的排班数量")
    schedule_previews: List[AutoSchedulePreview] = Field(default_factory=list, description="排班预览列表")
    schedule_ids: List[int] = Field(default_factory=list, description="创建的排班ID列表")


# ==================== 员工列表响应 ====================
class EmployeeListResponse(BaseModel):
    """员工列表响应模型"""
    success: bool
    message: str
    data: List[EmployeeResponse] = Field(description="员工列表")


# ==================== 岗位列表响应 ====================
class PositionListResponse(BaseModel):
    """岗位列表响应模型"""
    success: bool
    message: str
    data: List[PositionResponse] = Field(description="岗位列表")


# ==================== 班次列表响应 ====================
class ShiftListResponse(BaseModel):
    """班次列表响应模型"""
    success: bool
    message: str
    data: List[ShiftResponse] = Field(description="班次列表")
