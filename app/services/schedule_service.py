from typing import List, Optional
from datetime import date, datetime, timedelta
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
    ScheduleCalendarResponse,
    ManualScheduleCreate,
    ManualScheduleCreateResponse,
    AutoScheduleConfig,
    AutoScheduleCreateResponse,
    AutoSchedulePreview
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

    # ==================== 手动排班功能 ====================

    def manual_create_schedules(
        self,
        manual_request: ManualScheduleCreate
    ) -> ManualScheduleCreateResponse:
        """
        手动创建排班
        
        Args:
            manual_request: 手动排班请求
            
        Returns:
            手动排班创建响应
        """
        try:
            created_count = 0
            updated_count = 0
            skipped_count = 0
            schedule_ids = []
            details = []
            
            for schedule_item in manual_request.schedules:
                try:
                    # 检查是否已存在排班
                    existing_schedule = None
                    if self.schedule_repo.check_schedule_exists(
                        schedule_item.schedule_date,
                        schedule_item.position_id
                    ):
                        if manual_request.override_existing:
                            # 获取现有排班ID进行更新
                            schedules = self.schedule_repo.get_schedules_by_date_range(
                                start_date=schedule_item.schedule_date,
                                end_date=schedule_item.schedule_date,
                                position_id=schedule_item.position_id
                            )
                            if schedules:
                                existing_schedule = schedules[0]
                        else:
                            skipped_count += 1
                            details.append(
                                f"跳过 {schedule_item.schedule_date} {self._get_position_name(schedule_item.position_id)}：已存在排班"
                            )
                            continue
                    
                    if existing_schedule:
                        # 更新现有排班
                        schedule_id = existing_schedule['schedule_id']
                        
                        # 更新排班基本信息
                        schedule_data = {
                            'schedule_date': schedule_item.schedule_date,
                            'shift_id': schedule_item.shift_id,
                            'position_id': schedule_item.position_id
                        }
                        
                        self.schedule_repo.update_schedule(schedule_id, schedule_data)
                        
                        # 删除旧的员工关联
                        self.schedule_repo.delete_schedule_employees(schedule_id)
                        
                        updated_count += 1
                        details.append(
                            f"更新 {schedule_item.schedule_date} {self._get_position_name(schedule_item.position_id)}"
                        )
                    else:
                        # 创建新排班
                        schedule_data = {
                            'schedule_date': schedule_item.schedule_date,
                            'shift_id': schedule_item.shift_id,
                            'position_id': schedule_item.position_id
                        }
                        
                        schedule_id = self.schedule_repo.create_schedule(schedule_data)
                        
                        if schedule_id <= 0:
                            details.append(
                                f"创建失败 {schedule_item.schedule_date} {self._get_position_name(schedule_item.position_id)}"
                            )
                            continue
                        
                        created_count += 1
                        details.append(
                            f"创建 {schedule_item.schedule_date} {self._get_position_name(schedule_item.position_id)}"
                        )
                    
                    # 添加员工关联
                    for employee_id in schedule_item.employee_ids:
                        is_leader = (employee_id == schedule_item.leader_employee_id)
                        self.schedule_repo.add_schedule_employee(
                            schedule_id,
                            employee_id,
                            is_leader
                        )
                    
                    schedule_ids.append(schedule_id)
                    
                except Exception as item_error:
                    details.append(
                        f"处理失败 {schedule_item.schedule_date} {self._get_position_name(schedule_item.position_id)}：{str(item_error)}"
                    )
                    continue
            
            total_processed = created_count + updated_count
            
            return ManualScheduleCreateResponse(
                success=total_processed > 0,
                message=f"手动排班完成：创建 {created_count} 个，更新 {updated_count} 个，跳过 {skipped_count} 个",
                created_count=created_count,
                updated_count=updated_count,
                skipped_count=skipped_count,
                schedule_ids=schedule_ids,
                details=details
            )
            
        except Exception as e:
            return ManualScheduleCreateResponse(
                success=False,
                message=f"手动排班失败：{str(e)}",
                details=[f"系统错误：{str(e)}"]
            )

    # ==================== 自动排班功能 ====================

    def auto_create_schedules(
        self,
        auto_config: AutoScheduleConfig,
        preview_mode: bool = False
    ) -> AutoScheduleCreateResponse:
        """
        自动创建排班
        
        Args:
            auto_config: 自动排班配置
            preview_mode: 是否为预览模式
            
        Returns:
            自动排班创建响应
        """
        try:
            # 获取所有员工
            all_employees = self.schedule_repo.get_all_employees()
            employee_map = {emp['employee_id']: emp for emp in all_employees}
            
            # 获取所有岗位和班次信息
            all_positions = self.schedule_repo.get_all_positions()
            position_map = {pos['position_id']: pos for pos in all_positions}
            
            all_shifts = self.schedule_repo.get_all_shifts()
            shift_map = {shift['shift_id']: shift for shift in all_shifts}
            
            schedule_previews = []
            created_count = 0
            conflict_count = 0
            schedule_ids = []
            
            # 按日期循环生成排班
            current_date = auto_config.start_date
            employee_workload = {emp_id: 0 for emp_id in employee_map.keys()}  # 工作负荷统计
            employee_last_work_date = {}  # 员工最后工作日期
            
            while current_date <= auto_config.end_date:
                # 为每个规则生成排班
                for rule in auto_config.rules:
                    try:
                        # 检查是否已存在排班
                        if self.schedule_repo.check_schedule_exists(current_date, rule.position_id):
                            if not auto_config.override_existing:
                                conflict_count += 1
                                schedule_previews.append(AutoSchedulePreview(
                                    schedule_date=current_date,
                                    position_name=position_map.get(rule.position_id, {}).get('position_name', '未知岗位'),
                                    shift_name='已存在排班',
                                    employee_names=[],
                                    conflict_reason='该岗位已有排班记录'
                                ))
                                continue
                        
                        # 选择班次（优先使用配置的班次）
                        selected_shift_id = rule.preferred_shift_ids[0] if rule.preferred_shift_ids else 1
                        shift_info = shift_map.get(selected_shift_id, {})
                        
                        # 智能选择员工
                        selected_employees = self._select_employees_for_auto_schedule(
                            rule=rule,
                            current_date=current_date,
                            employee_map=employee_map,
                            employee_workload=employee_workload,
                            employee_last_work_date=employee_last_work_date,
                            auto_config=auto_config
                        )
                        
                        if len(selected_employees) < rule.required_employees:
                            conflict_count += 1
                            schedule_previews.append(AutoSchedulePreview(
                                schedule_date=current_date,
                                position_name=position_map.get(rule.position_id, {}).get('position_name', '未知岗位'),
                                shift_name=shift_info.get('shift_name', '未知班次'),
                                employee_names=[employee_map[emp_id]['name'] for emp_id in selected_employees],
                                conflict_reason=f'可用员工不足，需要 {rule.required_employees} 人，只找到 {len(selected_employees)} 人'
                            ))
                            continue
                        
                        # 选择负责人
                        leader_employee_id = None
                        if rule.require_leader and selected_employees:
                            # 选择工作负荷最低的员工作为负责人
                            leader_employee_id = min(selected_employees, key=lambda emp_id: employee_workload[emp_id])
                        
                        # 创建排班预览
                        employee_names = [employee_map[emp_id]['name'] for emp_id in selected_employees]
                        leader_name = employee_map[leader_employee_id]['name'] if leader_employee_id else None
                        
                        schedule_preview = AutoSchedulePreview(
                            schedule_date=current_date,
                            position_name=position_map.get(rule.position_id, {}).get('position_name', '未知岗位'),
                            shift_name=shift_info.get('shift_name', '未知班次'),
                            employee_names=employee_names,
                            leader_name=leader_name
                        )
                        schedule_previews.append(schedule_preview)
                        
                        # 如果不是预览模式，实际创建排班
                        if not preview_mode:
                            # 创建排班记录
                            schedule_data = {
                                'schedule_date': current_date,
                                'shift_id': selected_shift_id,
                                'position_id': rule.position_id
                            }
                            
                            schedule_id = self.schedule_repo.create_schedule(schedule_data)
                            
                            if schedule_id > 0:
                                # 添加员工关联
                                for employee_id in selected_employees:
                                    is_leader = (employee_id == leader_employee_id)
                                    self.schedule_repo.add_schedule_employee(
                                        schedule_id,
                                        employee_id,
                                        is_leader
                                    )
                                
                                schedule_ids.append(schedule_id)
                                created_count += 1
                                
                                # 更新员工工作负荷和最后工作日期
                                for employee_id in selected_employees:
                                    employee_workload[employee_id] += 1
                                    employee_last_work_date[employee_id] = current_date
                        
                    except Exception as rule_error:
                        conflict_count += 1
                        schedule_previews.append(AutoSchedulePreview(
                            schedule_date=current_date,
                            position_name=position_map.get(rule.position_id, {}).get('position_name', '未知岗位'),
                            shift_name='处理失败',
                            employee_names=[],
                            conflict_reason=f'处理错误：{str(rule_error)}'
                        ))
                        continue
                
                # 移动到下一天
                current_date = current_date + timedelta(days=1)
            
            success_message = f"自动排班{'预览' if preview_mode else '完成'}：生成 {len(schedule_previews)} 个排班方案"
            if conflict_count > 0:
                success_message += f"，其中 {conflict_count} 个存在冲突"
            
            return AutoScheduleCreateResponse(
                success=True,
                message=success_message,
                preview_mode=preview_mode,
                created_count=created_count,
                conflict_count=conflict_count,
                schedule_previews=schedule_previews,
                schedule_ids=schedule_ids
            )
            
        except Exception as e:
            return AutoScheduleCreateResponse(
                success=False,
                message=f"自动排班失败：{str(e)}",
                preview_mode=preview_mode,
                schedule_previews=[]
            )

    def _select_employees_for_auto_schedule(
        self,
        rule,
        current_date: date,
        employee_map: dict,
        employee_workload: dict,
        employee_last_work_date: dict,
        auto_config: AutoScheduleConfig
    ) -> List[int]:
        """
        为自动排班智能选择员工
        
        Args:
            rule: 排班规则
            current_date: 当前日期
            employee_map: 员工映射
            employee_workload: 员工工作负荷
            employee_last_work_date: 员工最后工作日期
            auto_config: 自动排班配置
            
        Returns:
            选中的员工ID列表
        """
        available_employees = []
        
        for employee_id, employee_info in employee_map.items():
            # 排除指定的员工
            if employee_id in rule.exclude_employee_ids:
                continue
            
            # 检查连续工作天数限制
            if employee_id in employee_last_work_date:
                last_work_date = employee_last_work_date[employee_id]
                days_diff = (current_date - last_work_date).days
                
                # 如果连续工作天数超过限制，需要休息
                if days_diff == 1 and employee_workload[employee_id] >= auto_config.max_consecutive_days:
                    continue
            
            # 检查是否有其他冲突（这里可以扩展更多业务规则）
            
            available_employees.append(employee_id)
        
        # 如果启用工作负荷均衡，按工作负荷排序
        if auto_config.balance_workload:
            available_employees.sort(key=lambda emp_id: employee_workload[emp_id])
        
        # 返回所需数量的员工
        return available_employees[:rule.required_employees]

    def _get_position_name(self, position_id: int) -> str:
        """获取岗位名称"""
        try:
            positions = self.schedule_repo.get_all_positions()
            for position in positions:
                if position['position_id'] == position_id:
                    return position['position_name']
            return f"岗位{position_id}"
        except:
            return f"岗位{position_id}"

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
