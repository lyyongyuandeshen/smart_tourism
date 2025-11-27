from typing import List, Optional
from datetime import date, datetime
from mysql.connector import pooling

from app.repository.schedule_repo import ScheduleRepository
from app.models.schedule_models import (
    EmployeeResponse,
    PositionResponse,
    ShiftResponse,
    ScheduleCreate,
    ScheduleDetail,
    ScheduleEmployeeDetail,
    ScheduleQueryRequest,
    ScheduleListResponse,
    ScheduleCreateResponse,
    BatchScheduleCreate,
    BatchScheduleCreateResponse,
    EmployeeListResponse,
    PositionListResponse,
    ShiftListResponse,
    CalendarScheduleItem,
    CalendarDaySchedule,
    ScheduleCalendarResponse
)


class ScheduleService:
    """排班业务服务类"""

    def __init__(self, pool: pooling.MySQLConnectionPool):
        self.schedule_repo = ScheduleRepository(pool)

    # ==================== 基础数据查询 ====================

    def get_all_employees(self) -> EmployeeListResponse:
        """获取所有员工列表"""
        try:
            employees = self.schedule_repo.get_all_employees()
            
            employee_list = [
                EmployeeResponse(
                    employee_id=e['employee_id'],
                    name=e['name'],
                    employee_code=e['employee_code'],
                    phone=e['phone'],
                    created_at=e['created_at']
                )
                for e in employees
            ]
            
            return EmployeeListResponse(
                success=True,
                message="查询成功",
                data=employee_list
            )
        except Exception as e:
            return EmployeeListResponse(
                success=False,
                message=f"查询失败：{str(e)}",
                data=[]
            )

    def get_all_positions(self) -> PositionListResponse:
        """获取所有岗位列表"""
        try:
            positions = self.schedule_repo.get_all_positions()
            
            position_list = [
                PositionResponse(
                    position_id=p['position_id'],
                    position_name=p['position_name'],
                    description=p['description'],
                    created_at=p['created_at']
                )
                for p in positions
            ]
            
            return PositionListResponse(
                success=True,
                message="查询成功",
                data=position_list
            )
        except Exception as e:
            return PositionListResponse(
                success=False,
                message=f"查询失败：{str(e)}",
                data=[]
            )

    def get_all_shifts(self) -> ShiftListResponse:
        """获取所有班次列表"""
        try:
            shifts = self.schedule_repo.get_all_shifts()
            
            shift_list = [
                ShiftResponse(
                    shift_id=s['shift_id'],
                    shift_name=s['shift_name'],
                    start_time=str(s['start_time']),
                    end_time=str(s['end_time']),
                    position_id=s['position_id'],
                    position_name=s['position_name'],
                    created_at=s['created_at']
                )
                for s in shifts
            ]
            
            return ShiftListResponse(
                success=True,
                message="查询成功",
                data=shift_list
            )
        except Exception as e:
            return ShiftListResponse(
                success=False,
                message=f"查询失败：{str(e)}",
                data=[]
            )

    # ==================== 排班查询 ====================

    def query_schedules(self, request: ScheduleQueryRequest) -> ScheduleListResponse:
        """
        查询排班列表
        
        Args:
            request: 查询请求参数
            
        Returns:
            排班列表响应
        """
        try:
            # 根据关键词搜索或按条件查询
            if request.keyword:
                schedules = self.schedule_repo.search_schedules_by_keyword(
                    keyword=request.keyword,
                    start_date=request.start_date,
                    end_date=request.end_date
                )
            else:
                schedules = self.schedule_repo.get_schedules_by_date_range(
                    start_date=request.start_date,
                    end_date=request.end_date,
                    position_id=request.position_id,
                    employee_id=request.employee_id
                )
            
            # 构建详细的排班信息
            schedule_list = []
            for schedule in schedules:
                # 获取该排班的员工列表
                employees = self.schedule_repo.get_schedule_employees(schedule['schedule_id'])
                
                employee_details = [
                    ScheduleEmployeeDetail(
                        employee_id=emp['employee_id'],
                        employee_name=emp['employee_name'],
                        employee_code=emp['employee_code'],
                        is_leader=bool(emp['is_leader'])
                    )
                    for emp in employees
                ]
                
                schedule_detail = ScheduleDetail(
                    schedule_id=schedule['schedule_id'],
                    schedule_date=schedule['schedule_date'],
                    shift_id=schedule['shift_id'],
                    shift_name=schedule['shift_name'],
                    start_time=str(schedule['start_time']),
                    end_time=str(schedule['end_time']),
                    position_id=schedule['position_id'],
                    position_name=schedule['position_name'],
                    employees=employee_details,
                    created_at=schedule['created_at']
                )
                
                schedule_list.append(schedule_detail)
            
            return ScheduleListResponse(
                success=True,
                message="查询成功",
                total=len(schedule_list),
                data=schedule_list
            )
            
        except Exception as e:
            return ScheduleListResponse(
                success=False,
                message=f"查询失败：{str(e)}",
                total=0,
                data=[]
            )

    def get_calendar_schedules(
        self,
        start_date: date,
        end_date: date
    ) -> ScheduleCalendarResponse:
        """
        获取日历视图的排班数据
        
        Args:
            start_date: 开始日期
            end_date: 结束日期
            
        Returns:
            日历排班响应
        """
        try:
            schedules = self.schedule_repo.get_schedules_by_date_range(
                start_date=start_date,
                end_date=end_date
            )
            
            # 按日期分组
            date_schedules_map = {}
            
            for schedule in schedules:
                schedule_date = schedule['schedule_date']
                
                # 获取该排班的员工列表
                employees = self.schedule_repo.get_schedule_employees(schedule['schedule_id'])
                employee_names = "、".join([emp['employee_name'] for emp in employees])
                
                calendar_item = CalendarScheduleItem(
                    schedule_id=schedule['schedule_id'],
                    position_name=schedule['position_name'],
                    shift_name=schedule['shift_name'],
                    start_time=str(schedule['start_time']),
                    end_time=str(schedule['end_time']),
                    employee_names=employee_names
                )
                
                if schedule_date not in date_schedules_map:
                    date_schedules_map[schedule_date] = []
                
                date_schedules_map[schedule_date].append(calendar_item)
            
            # 构建日历数据
            calendar_data = [
                CalendarDaySchedule(
                    schedule_date=schedule_date,
                    schedules=schedules
                )
                for schedule_date, schedules in sorted(date_schedules_map.items())
            ]
            
            return ScheduleCalendarResponse(
                success=True,
                message="查询成功",
                data=calendar_data
            )
            
        except Exception as e:
            return ScheduleCalendarResponse(
                success=False,
                message=f"查询失败：{str(e)}",
                data=[]
            )

    # ==================== 排班创建 ====================

    def create_schedule(self, schedule: ScheduleCreate) -> ScheduleCreateResponse:
        """
        创建单个排班
        
        Args:
            schedule: 排班信息
            
        Returns:
            创建响应
        """
        try:
            # 检查是否已存在排班
            if self.schedule_repo.check_schedule_exists(
                schedule.schedule_date,
                schedule.position_id
            ):
                return ScheduleCreateResponse(
                    success=False,
                    message=f"该岗位在 {schedule.schedule_date} 已有排班记录"
                )
            
            # 创建排班记录
            schedule_data = {
                'schedule_date': schedule.schedule_date,
                'shift_id': schedule.shift_id,
                'position_id': schedule.position_id
            }
            
            schedule_id = self.schedule_repo.create_schedule(schedule_data)
            
            if schedule_id <= 0:
                return ScheduleCreateResponse(
                    success=False,
                    message="排班记录创建失败"
                )
            
            # 添加员工关联
            for employee in schedule.employees:
                self.schedule_repo.add_schedule_employee(
                    schedule_id,
                    employee.employee_id,
                    employee.is_leader
                )
            
            return ScheduleCreateResponse(
                success=True,
                message="排班创建成功",
                schedule_id=schedule_id
            )
            
        except Exception as e:
            return ScheduleCreateResponse(
                success=False,
                message=f"创建失败：{str(e)}"
            )

    def batch_create_schedules(
        self,
        batch_request: BatchScheduleCreate
    ) -> BatchScheduleCreateResponse:
        """
        批量创建排班（用于新增排班弹窗）
        
        Args:
            batch_request: 批量排班请求
            
        Returns:
            批量创建响应
        """
        try:
            created_count = 0
            schedule_ids = []
            
            for schedule_item in batch_request.schedules:
                # 解析班次时间（如：08:00-17:00）
                time_parts = schedule_item.shift_time.split('-')
                if len(time_parts) != 2:
                    continue
                
                start_time = time_parts[0].strip()
                end_time = time_parts[1].strip()
                
                # 查找或创建班次
                # 这里简化处理，假设使用第一个匹配的班次
                shifts = self.schedule_repo.get_all_shifts()
                shift_id = shifts[0]['shift_id'] if shifts else 1
                
                # 创建排班记录
                schedule_data = {
                    'schedule_date': batch_request.schedule_date,
                    'shift_id': shift_id,
                    'position_id': batch_request.position_id
                }
                
                schedule_id = self.schedule_repo.create_schedule(schedule_data)
                
                if schedule_id > 0:
                    # 添加员工关联
                    for employee in schedule_item.employees:
                        self.schedule_repo.add_schedule_employee(
                            schedule_id,
                            employee.employee_id,
                            employee.is_leader
                        )
                    
                    created_count += 1
                    schedule_ids.append(schedule_id)
            
            return BatchScheduleCreateResponse(
                success=True,
                message=f"成功创建 {created_count} 个排班",
                created_count=created_count,
                schedule_ids=schedule_ids
            )
            
        except Exception as e:
            return BatchScheduleCreateResponse(
                success=False,
                message=f"批量创建失败：{str(e)}",
                created_count=0,
                schedule_ids=[]
            )

    # ==================== 排班更新和删除 ====================

    def update_schedule(
        self,
        schedule_id: int,
        schedule: ScheduleCreate
    ) -> ScheduleCreateResponse:
        """
        更新排班
        
        Args:
            schedule_id: 排班ID
            schedule: 排班信息
            
        Returns:
            更新响应
        """
        try:
            # 检查排班是否存在
            existing = self.schedule_repo.get_schedule_by_id(schedule_id)
            if not existing:
                return ScheduleCreateResponse(
                    success=False,
                    message=f"排班记录不存在：{schedule_id}"
                )
            
            # 检查是否与其他排班冲突
            if self.schedule_repo.check_schedule_exists(
                schedule.schedule_date,
                schedule.position_id,
                exclude_schedule_id=schedule_id
            ):
                return ScheduleCreateResponse(
                    success=False,
                    message=f"该岗位在 {schedule.schedule_date} 已有其他排班记录"
                )
            
            # 更新排班记录
            schedule_data = {
                'schedule_date': schedule.schedule_date,
                'shift_id': schedule.shift_id,
                'position_id': schedule.position_id
            }
            
            rows_affected = self.schedule_repo.update_schedule(schedule_id, schedule_data)
            
            if rows_affected <= 0:
                return ScheduleCreateResponse(
                    success=False,
                    message="排班记录更新失败"
                )
            
            # 删除旧的员工关联
            self.schedule_repo.delete_schedule_employees(schedule_id)
            
            # 添加新的员工关联
            for employee in schedule.employees:
                self.schedule_repo.add_schedule_employee(
                    schedule_id,
                    employee.employee_id,
                    employee.is_leader
                )
            
            return ScheduleCreateResponse(
                success=True,
                message="排班更新成功",
                schedule_id=schedule_id
            )
            
        except Exception as e:
            return ScheduleCreateResponse(
                success=False,
                message=f"更新失败：{str(e)}"
            )

    def delete_schedule(self, schedule_id: int) -> ScheduleCreateResponse:
        """
        删除排班
        
        Args:
            schedule_id: 排班ID
            
        Returns:
            删除响应
        """
        try:
            # 检查排班是否存在
            existing = self.schedule_repo.get_schedule_by_id(schedule_id)
            if not existing:
                return ScheduleCreateResponse(
                    success=False,
                    message=f"排班记录不存在：{schedule_id}"
                )
            
            # 删除排班记录（会级联删除员工关联）
            rows_affected = self.schedule_repo.delete_schedule(schedule_id)
            
            if rows_affected > 0:
                return ScheduleCreateResponse(
                    success=True,
                    message="排班删除成功"
                )
            else:
                return ScheduleCreateResponse(
                    success=False,
                    message="排班删除失败"
                )
                
        except Exception as e:
            return ScheduleCreateResponse(
                success=False,
                message=f"删除失败：{str(e)}"
            )

    def get_schedule_detail(self, schedule_id: int) -> Optional[ScheduleDetail]:
        """
        获取排班详情
        
        Args:
            schedule_id: 排班ID
            
        Returns:
            排班详情
        """
        try:
            schedule = self.schedule_repo.get_schedule_by_id(schedule_id)
            
            if not schedule:
                return None
            
            # 获取员工列表
            employees = self.schedule_repo.get_schedule_employees(schedule_id)
            
            employee_details = [
                ScheduleEmployeeDetail(
                    employee_id=emp['employee_id'],
                    employee_name=emp['employee_name'],
                    employee_code=emp['employee_code'],
                    is_leader=bool(emp['is_leader'])
                )
                for emp in employees
            ]
            
            return ScheduleDetail(
                schedule_id=schedule['schedule_id'],
                schedule_date=schedule['schedule_date'],
                shift_id=schedule['shift_id'],
                shift_name=schedule['shift_name'],
                start_time=str(schedule['start_time']),
                end_time=str(schedule['end_time']),
                position_id=schedule['position_id'],
                position_name=schedule['position_name'],
                employees=employee_details,
                created_at=schedule['created_at']
            )
            
        except Exception as e:
            return None
