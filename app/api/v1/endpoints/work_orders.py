import uuid
from typing import Optional, List
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db_session, get_current_user_id
from app.utils.dict_translate import translate_response

router = APIRouter()


# 请求模型
class WorkOrderCreate(BaseModel):
    """创建工单请求"""
    title: str = Field(..., description="工单标题，长度1-200字符", min_length=1, max_length=200)
    detail: str = Field(..., description="工单详情描述")
    priority: int = Field(2, description="优先级：1=低 2=中 3=高 4=紧急，默认为2（中）", ge=1, le=4)
    category: int = Field(..., description="工单分类：1=售后维修 2=商品咨询 3=售后服务 4=退货 99=其他")
    assignee_id: Optional[str] = Field(None, description="指定处理人用户ID，如果指定则工单会自动分配给该用户", max_length=30)
    timeout_hours: Optional[int] = Field(None, description="超时小时数（从创建时间开始计算），如果不指定则默认为2小时", ge=1)


class WorkOrderUpdate(BaseModel):
    """更新工单请求"""
    title: Optional[str] = Field(None, description="工单标题，长度不超过200字符", max_length=200)
    detail: Optional[str] = Field(None, description="工单详情描述")
    priority: Optional[int] = Field(None, description="优先级：1=低 2=中 3=高 4=紧急", ge=1, le=4)
    category: Optional[int] = Field(None, description="工单分类：1=售后维修 2=商品咨询 3=售后服务 4=退货 99=其他")
    status: Optional[int] = Field(None, description="工单状态：10=新建 20=处理中 30=待确认 40=已关闭")
    timeout_hours: Optional[int] = Field(None, description="超时小时数（从当前时间重新计算）", ge=1)


class WorkOrderTransfer(BaseModel):
    """工单转移请求"""
    to_user_id: str = Field(..., description="转移目标用户ID，必须是有效的用户ID", max_length=30)
    node_content: Optional[str] = Field(None, description="转移说明/备注")


class WorkOrderNodeProcess(BaseModel):
    """工单节点处理请求"""
    node_type: str = Field(..., description="节点处理类型：提交/转派/关闭。提交：提交当前节点处理结果；转派：转派给其他处理人；关闭：关闭工单", max_length=50)
    node_content: Optional[str] = Field(None, description="处理意见/说明内容")
    next_node_name: Optional[str] = Field(None, description="下一节点名称（如果创建新节点时使用），如果不指定则使用默认名称", max_length=50)
    to_user_id: Optional[str] = Field(None, description="转派目标用户ID，当node_type为'转派'时必填，其他情况可为空", max_length=30)


class WorkOrderFeedback(BaseModel):
    """工单反馈请求"""
    score: int = Field(..., description="服务质量评分：1-5分，1分最低，5分最高", ge=1, le=5)
    suggestion: Optional[str] = Field(None, description="建议或意见内容")


# 响应模型
class WorkOrderNodeResponse(BaseModel):
    """工单节点响应"""
    node_id: str = Field(..., description="节点ID")
    order_id: Optional[str] = Field(None, description="工单ID")
    node_name: Optional[str] = Field(None, description="节点名称")
    handler_id: Optional[str] = Field(None, description="处理人ID")
    user_name: Optional[str] = Field(None, description="处理人姓名")
    node_type: Optional[str] = Field(
        None,
        description="节点类型：创建/分配/提交/转派/关闭",
        json_schema_extra={
            "is_translate": True,
            "translation_map": "work_order_node_type"
        }
    )
    node_type_text: Optional[str] = Field(None, description="节点类型文本（翻译后）")
    node_content: Optional[str] = Field(None, description="节点处理内容/说明")
    to_assignee_id: Optional[str] = Field(None, description="转派目标处理人ID")


class WorkOrderFeedbackResponse(BaseModel):
    """工单反馈响应"""
    feedback_id: str = Field(..., description="反馈ID")
    order_id: Optional[str] = Field(None, description="工单ID")
    score: Optional[int] = Field(None, description="评分：1-5分")
    suggestion: Optional[str] = Field(None, description="建议/意见")
    feedback_time: Optional[datetime] = Field(None, description="反馈时间")


class WorkOrderResponse(BaseModel):
    """工单响应"""
    order_id: Optional[str] = Field(None, description="工单ID")
    order_no: Optional[str] = Field(None, description="工单编号")
    title: Optional[str] = Field(None, description="工单标题")
    detail: Optional[str] = Field(None, description="工单详情")
    priority: Optional[str] = Field(
        None,
        description="工单优先级：1=低 2=中 3=高 4=紧急",
        json_schema_extra={
            "is_translate": True,
            "translation_map": "work_order_priority"
        }
    )
    priority_text: Optional[str] = Field(None, description="优先级文本（翻译后）")
    status: Optional[str] = Field(
        None,
        description="工单状态：10=新建 20=处理中 30=待确认 40=已关闭",
        json_schema_extra={
            "is_translate": True,
            "translation_map": "work_order_status"
        }
    )
    status_text: Optional[str] = Field(None, description="状态文本（翻译后）")
    category: Optional[str] = Field(
        None,
        description="工单分类：1=售后维修 2=商品咨询 3=售后服务 4=退货 99=其他",
        json_schema_extra={
            "is_translate": True,
            "translation_map": "work_category"
        }
    )
    category_text: Optional[str] = Field(None, description="分类文本（翻译后）")
    creator_user_id: Optional[str] = Field(None, description="创建人用户ID")
    user_name: Optional[str] = Field(None, description="创建人姓名")
    current_node_id: Optional[str] = Field(None, description="当前节点ID")
    timeount: Optional[datetime] = Field(None, description="超时时间")
    create_time: Optional[datetime] = Field(None, description="创建时间")
    update_time: Optional[datetime] = Field(None, description="更新时间")
    nodes: Optional[List[WorkOrderNodeResponse]] = Field(None, description="处理节点列表")
    feedbacks: Optional[List[WorkOrderFeedbackResponse]] = Field(None, description="反馈列表")


class WorkOrderListResponse(BaseModel):
    """工单列表响应"""
    total: int = Field(..., description="总记录数")
    items: List[WorkOrderResponse] = Field(..., description="工单列表")


class WorkOrderNodeListResponse(BaseModel):
    """工单节点列表响应"""
    total: int = Field(..., description="总记录数")
    items: List[WorkOrderNodeResponse] = Field(..., description="节点列表")


def _generate_order_no() -> str:
    """生成工单编号：yyyymmdd+6位流水"""
    today = datetime.now().strftime("%Y%m%d")
    # 这里简化处理，实际应该从数据库获取当日最大流水号
    import random
    serial = f"{random.randint(100000, 999999)}"
    return f"{today}{serial}"


@router.get(
    "",
    summary="分页查询工单",
    description="分页查询工单列表，支持按创建人、工单编号、状态、优先级、分类、时间范围等条件筛选。返回工单列表和总数。",
    response_description="返回工单列表及总数，包含工单基本信息（标题、详情、优先级、状态、分类等）和创建人信息。"
)
async def list_work_orders(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    creator_user_id: Optional[str] = Query(None, description="创建人ID"),
    order_no: Optional[str] = Query(None, description="工单编号（精确查询）"),
    status: Optional[int] = Query(None, description="状态：10=新建 20=处理中 30=待确认 40=已关闭"),
    priority: Optional[int] = Query(None, description="优先级：1=低 2=中 3=高 4=紧急"),
    category: Optional[int] = Query(None, description="工单分类：1=售后维修 2=商品咨询 3=售后服务 4=退货,99=其他"),
    start_time: Optional[datetime] = Query(None, description="开始时间"),
    end_time: Optional[datetime] = Query(None, description="结束时间"),
    session: AsyncSession = Depends(get_db_session),
    current_user_id: str = Depends(get_current_user_id),
) -> WorkOrderListResponse:
    """分页查询工单列表"""
    offset = (page - 1) * page_size
    
    # 构建查询条件
    conditions = []
    params = {}
    
    if creator_user_id:
        conditions.append("creator_user_id = :creator_user_id")
        params["creator_user_id"] = creator_user_id
    if order_no:
        conditions.append("order_no = :order_no")
        params["order_no"] = order_no
    if status is not None:
        conditions.append("status = :status")
        params["status"] = status
    if priority is not None:
        conditions.append("priority = :priority")
        params["priority"] = priority
    if start_time:
        conditions.append("create_time >= :start_time")
        params["start_time"] = start_time
    if end_time:
        conditions.append("create_time <= :end_time")
        params["end_time"] = end_time
    if category:
        conditions.append("category = :category")
        params["category"] = category
    
    where_clause = " AND ".join(conditions) if conditions else "1=1"
    
    # 查询总数
    count_sql = text(f"SELECT COUNT(*) as total FROM tbkf_work_order_info WHERE {where_clause}")
    count_result = await session.execute(count_sql, params)
    total = count_result.scalar()
    
    # 查询列表
    list_sql = text(f"""
        SELECT order_id, order_no, title, detail, priority, status,category,
        creator_user_id,
        (select user_name from sys_user where tbkf_work_order_info.creator_user_id=sys_user.user_id) user_name,
        current_node_id, timeount, create_time, update_time
        FROM tbkf_work_order_info
        WHERE {where_clause}
        ORDER BY create_time DESC
        LIMIT :limit OFFSET :offset
    """)
    params.update({"limit": page_size, "offset": offset})
    result = await session.execute(list_sql, params)
    orders = [dict(row) for row in result.mappings().all()]
    orders = await translate_response(orders, WorkOrderResponse)
    return WorkOrderListResponse(total=total, items=orders)


@router.get(
    "/{order_id}",
    summary="工单详情",
    description="根据工单ID获取工单的详细信息，包括工单基本信息、所有处理节点记录和反馈信息。",
    response_description="返回完整的工单信息，包含：工单基本信息、处理节点列表（按时间顺序）、反馈列表（按时间倒序）。"
)
async def get_work_order(
    order_id: str,
    session: AsyncSession = Depends(get_db_session),
    current_user_id: str = Depends(get_current_user_id),
) -> WorkOrderResponse:
    """获取工单详情"""
    sql = text("""
        SELECT order_id, order_no, title, detail, priority, status,category,
        creator_user_id, current_node_id, timeount, create_time, update_time
        FROM tbkf_work_order_info
        WHERE order_id = :order_id
    """)
    result = await session.execute(sql, {"order_id": order_id})
    order = result.mappings().first()
    
    if not order:
        raise HTTPException(status_code=404, detail="工单不存在")
    
    order_dict = dict(order)
    
    # 查询工单节点（注意：表结构中没有 create_time，这里假设有，如果没有需要添加该字段）
    node_sql = text("""
        SELECT node_id, order_id, node_name, handler_id,
        (select user_name from sys_user where tbkf_work_order_node_info.handler_id=sys_user.user_id) user_name,
        node_type, node_content, to_assignee_id
        FROM tbkf_work_order_node_info
        WHERE order_id = :order_id
        ORDER BY node_id ASC
    """)
    node_result = await session.execute(node_sql, {"order_id": order_id})
    order_dict["nodes"] = [dict(row) for row in node_result.mappings().all()]
    
    # 查询工单反馈
    feedback_sql = text("""
        SELECT feedback_id, order_id, score, suggestion, feedback_time
        FROM tbkf_work_order_feedback_info
        WHERE order_id = :order_id
        ORDER BY feedback_time DESC
    """)
    feedback_result = await session.execute(feedback_sql, {"order_id": order_id})
    order_dict["feedbacks"] = [dict(row) for row in feedback_result.mappings().all()]
    result = await translate_response(order_dict, WorkOrderResponse)
    return result


@router.get(
    "/{order_id}/nodes",
    summary="工单节点记录分页查询",
    description="分页查询指定工单的所有处理节点记录，包括节点名称、处理人、动作类型、处理内容等信息。",
    response_description="返回工单节点列表及总数，包含每个节点的详细信息（节点ID、名称、处理人、动作类型、处理内容等）。"
)
async def list_work_order_nodes(
    order_id: str,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=100, description="每页数量"),
    session: AsyncSession = Depends(get_db_session),
    current_user_id: str = Depends(get_current_user_id),
) -> WorkOrderNodeListResponse:
    """分页查询工单节点记录"""
    # 检查工单是否存在
    check_sql = text("SELECT order_id FROM tbkf_work_order_info WHERE order_id = :order_id")
    check_result = await session.execute(check_sql, {"order_id": order_id})
    if not check_result.first():
        raise HTTPException(status_code=404, detail="工单不存在")
    
    offset = (page - 1) * page_size
    
    # 查询总数
    count_sql = text("SELECT COUNT(*) as total FROM tbkf_work_order_node_info WHERE order_id = :order_id")
    count_result = await session.execute(count_sql, {"order_id": order_id})
    total = count_result.scalar()
    
    # 查询列表（注意：表结构中没有 create_time，这里假设有，如果没有需要添加该字段）
    list_sql = text("""
        SELECT node_id, order_id, node_name, handler_id,
        (select user_name from sys_user where tbkf_work_order_node_info.handler_id=sys_user.user_id) user_name,
        node_type, node_content, to_assignee_id
        FROM tbkf_work_order_node_info
        WHERE order_id = :order_id
        ORDER BY node_id DESC
        LIMIT :limit OFFSET :offset
    """)
    result = await session.execute(list_sql, {"order_id": order_id, "limit": page_size, "offset": offset})
    nodes = [dict(row) for row in result.mappings().all()]
    nodes = await translate_response(nodes, WorkOrderNodeResponse)
    return WorkOrderNodeListResponse(total=total, items=nodes)


@router.post(
    "",
    summary="创建工单",
    description="创建新的工单。必须提供标题、详情、优先级和分类。可选择指定处理人和超时小时数。创建成功后会生成工单编号和初始节点。如果指定了处理人，工单状态会自动变为'处理中'（20）。",
    response_description="返回创建的工单ID、工单编号和成功消息。"
)
async def create_work_order(
    order_data: WorkOrderCreate,
    session: AsyncSession = Depends(get_db_session),
    current_user_id: str = Depends(get_current_user_id),
) -> dict:
    """创建新工单"""
    # 生成工单ID和编号
    order_id = str(uuid.uuid4()).replace("-", "")[:30]
    order_no = _generate_order_no()
    
    # 计算超时时间
    timeout_time = None
    if order_data.timeout_hours:
        timeout_time = datetime.now() + timedelta(hours=order_data.timeout_hours)
    else:
        timeout_time = datetime.now() + timedelta(hours=2)
    
    # 创建初始节点
    node_id = str(uuid.uuid4()).replace("-", "")[:30]

    # 插入工单
    insert_sql = text("""
        INSERT INTO tbkf_work_order_info (
            order_id, order_no, title, detail, priority, status, category,
            creator_user_id, current_node_id, timeount
        ) VALUES (
            :order_id, :order_no, :title, :detail, :priority, 10, :category, 
            :creator_user_id, :current_node_id, :timeount
        )
    """)
    await session.execute(insert_sql, {
        "order_id": order_id,
        "order_no": order_no,
        "title": order_data.title,
        "detail": order_data.detail,
        "priority": order_data.priority,
        "category": order_data.category,
        "current_node_id": node_id,
        "creator_user_id": current_user_id,
        "timeount": timeout_time,
    })
    

    node_insert_sql = text("""
        INSERT INTO tbkf_work_order_node_info (
            node_id, order_id, node_name, handler_id,  node_type, node_content, to_assignee_id
        ) VALUES (
            :node_id, :order_id, '创建工单', :handler_id, '创建', :node_content, '0'
        )
    """)
    await session.execute(node_insert_sql, {
        "node_id": node_id,
        "order_id": order_id,
        "handler_id": current_user_id,
        "node_content": f"创建工单：{order_data.title}",
    })
    
    # 如果指定了处理人，创建处理节点
    if order_data.assignee_id:
        process_node_id = str(uuid.uuid4()).replace("-", "")[:30]
        process_node_sql = text("""
            INSERT INTO tbkf_work_order_node_info (
                node_id, order_id, node_name, handler_id,  node_type, node_content, to_assignee_id
            ) VALUES (
                :node_id, :order_id, '待处理', :handler_id, '分配', :node_content, '0'
            )
        """)
        await session.execute(process_node_sql, {
            "node_id": process_node_id,
            "order_id": order_id,
            "handler_id": order_data.assignee_id,
            "node_content": f"工单已分配给处理人",
        })
        
        # 更新工单当前节点和状态
        update_sql = text("""
            UPDATE tbkf_work_order_info
            SET current_node_id = :node_id, status = 20
            WHERE order_id = :order_id
        """)
        await session.execute(update_sql, {"node_id": process_node_id, "order_id": order_id})
    
    await session.commit()
    
    return {"order_id": order_id, "order_no": order_no, "message": "工单创建成功"}


@router.post(
    "/{order_id}",
    summary="更新工单",
    description="更新工单信息，可以更新标题、详情、优先级、状态、分类、超时时间等字段。已关闭的工单（状态为40）不能修改。所有字段都是可选的，只更新提供的字段。",
    response_description="返回更新结果消息。"
)
async def update_work_order(
    order_id: str,
    order_data: WorkOrderUpdate,
    session: AsyncSession = Depends(get_db_session),
    current_user_id: str = Depends(get_current_user_id),
) -> dict:
    """更新工单信息"""
    # 检查工单是否存在
    check_sql = text("SELECT order_id, status FROM tbkf_work_order_info WHERE order_id = :order_id")
    check_result = await session.execute(check_sql, {"order_id": order_id})
    order = check_result.mappings().first()
    if not order:
        raise HTTPException(status_code=404, detail="工单不存在")
    
    # 已关闭的工单不能修改
    if order["status"] == 40:
        raise HTTPException(status_code=400, detail="已关闭的工单不能修改")
    
    # 构建更新字段
    update_fields = []
    params = {"order_id": order_id}
    
    if order_data.title is not None:
        update_fields.append("title = :title")
        params["title"] = order_data.title
    if order_data.detail is not None:
        update_fields.append("detail = :detail")
        params["detail"] = order_data.detail
    if order_data.priority is not None:
        update_fields.append("priority = :priority")
        params["priority"] = order_data.priority
    if order_data.status is not None:
        update_fields.append("status = :status")
        params["status"] = order_data.status
    if order_data.timeout_hours is not None:
        timeout_time = datetime.now() + timedelta(hours=order_data.timeout_hours)
        update_fields.append("timeount = :timeount")
        params["timeount"] = timeout_time
    if order_data.category is not None:
        update_fields.append("category = :category")
        params["category"] = order_data.category
    
    if not update_fields:
        return {"message": "无更新内容"}
    
    update_sql = text(f"""
        UPDATE tbkf_work_order_info
        SET {', '.join(update_fields)}
        WHERE order_id = :order_id
    """)
    await session.execute(update_sql, params)
    await session.commit()
    
    return {"message": "工单更新成功"}


@router.delete(
    "/{order_id}",
    summary="删除工单",
    description="删除指定的工单。这是物理删除操作，会级联删除该工单的所有节点记录和反馈信息。请谨慎使用。",
    response_description="返回删除结果消息。"
)
async def delete_work_order(
    order_id: str,
    session: AsyncSession = Depends(get_db_session),
    current_user_id: str = Depends(get_current_user_id),
) -> dict:
    """删除工单（物理删除，会级联删除节点和反馈）"""
    # 检查工单是否存在
    check_sql = text("SELECT order_id FROM tbkf_work_order_info WHERE order_id = :order_id")
    check_result = await session.execute(check_sql, {"order_id": order_id})
    if not check_result.first():
        raise HTTPException(status_code=404, detail="工单不存在")
    
    # 删除工单（级联删除节点和反馈）
    delete_sql = text("DELETE FROM tbkf_work_order_info WHERE order_id = :order_id")
    await session.execute(delete_sql, {"order_id": order_id})
    await session.commit()
    
    return {"message": "工单删除成功"}

@router.post(
    "/{order_id}/process",
    summary="工单节点处理",
    description="处理工单节点，支持三种操作类型：1) 提交：提交当前节点处理结果，工单状态变为'待确认'（30）；2) 转派：将工单转派给其他处理人，必须提供to_user_id，工单状态变为'处理中'（20）；3) 关闭：关闭工单，工单状态变为'已关闭'（40）。已关闭的工单不能再次处理。",
    response_description="返回处理结果消息。"
)
async def process_work_order_node(
    order_id: str,
    process_data: WorkOrderNodeProcess,
    session: AsyncSession = Depends(get_db_session),
    current_user_id: str = Depends(get_current_user_id),
) -> dict:
    """处理工单节点（提交/转派/关闭）"""
    # 检查工单是否存在
    check_sql = text("""
        SELECT order_id, status, current_node_id
        FROM tbkf_work_order_info
        WHERE order_id = :order_id
    """)
    check_result = await session.execute(check_sql, {"order_id": order_id})
    order = check_result.mappings().first()
    if not order:
        raise HTTPException(status_code=404, detail="工单不存在")
    
    # 已关闭的工单不能处理
    if order["status"] == 40:
        raise HTTPException(status_code=400, detail="已关闭的工单不能处理")
    
    # 创建处理节点
    node_id = str(uuid.uuid4()).replace("-", "")[:30]
    to_assignee_id = "0"
    node_sql = text("""
            INSERT INTO tbkf_work_order_node_info (
                node_id, order_id, node_name, handler_id,  node_type, node_content, to_assignee_id
            ) VALUES (
                :node_id, :order_id, :node_name, :handler_id, :node_type, :node_content, '0'
            )
        """)
    node_type = process_data.node_type
    # 根据动作处理
    if process_data.node_type == "关闭":
        check_old_node_sql = text("""
        SELECT  node_id, order_id, node_name, handler_id,  node_type, node_content, to_assignee_id
        FROM tbkf_work_order_node_info
        WHERE node_id = :node_id
        """)
        old_node_result = ""
        if order["current_node_id"]:
            old_node_result = await session.execute(check_old_node_sql, {"node_id": order["current_node_id"]})
        # 旧有工单节点要关闭
        if old_node_result.mappings().first():
            # 当前用户
            # 检查工单是否存在
            curent_user_sql = text("""
            SELECT user_id, user_name, nick_name
            FROM sys_user
            WHERE user_id = :user_id
            """)
            current_user_first = (await session.execute(curent_user_sql, {"user_id": current_user_id})).first()
            if not current_user_first:
                raise HTTPException(status_code=400, detail="当前操作用户不存在")
            
            close_old_node_sql = text("""
            update tbkf_work_order_node_info 
            set node_type=:node_type,node_content= :node_content, to_assignee_id=:to_assignee_id 
            WHERE node_id = :node_id
            """)
            
            await session.execute(close_old_node_sql, {"node_id": order["current_node_id"],
                "node_type": node_type ,
                "node_content" :  current_user_first._mapping["user_name"]+"关闭工单"  ,
                "to_assignee_id" :to_assignee_id        
            })

        # 关闭工单
            node_name = "关闭工单"
            await session.execute(node_sql, {
                "node_id": node_id,
                "order_id": order_id,
                "node_name": node_name,
                "handler_id": current_user_id,
                "node_type": node_type,
                "node_content": process_data.node_content or "工单已关闭",
            })
        # 更新工单状态
        update_sql = text("""
            UPDATE tbkf_work_order_info
            SET current_node_id = :node_id, status = 40
            WHERE order_id = :order_id
        """)
        await session.execute(update_sql, {"node_id": node_id, "order_id": order_id})
        
    elif process_data.node_type == "转派":
        # 转派工单
        if not process_data.to_user_id:
            raise HTTPException(status_code=400, detail="转派时必须指定目标用户")
        
        # 检查目标用户是否存在
        user_check_sql = text("SELECT user_id FROM sys_user WHERE user_id = :user_id AND del_flag = '0'")
        user_result = await session.execute(user_check_sql, {"user_id": process_data.to_user_id})
        if not user_result.first():
            raise HTTPException(status_code=400, detail="目标用户不存在")
        node_name = process_data.next_node_name or "待处理"
        await session.execute(node_sql, {
            "node_id": node_id,
            "order_id": order_id,
            "handler_id": current_user_id,
            "node_content": process_data.node_content or f"工单转派给 {process_data.to_user_id}",
        })
        
        # 创建新的处理节点
        process_node_id = str(uuid.uuid4()).replace("-", "")[:30]
        process_node_sql = text("""
            INSERT INTO tbkf_work_order_node_info (
                node_id, order_id, node_name, handler_id, node_type, node_content, to_assignee_id
            ) VALUES (
                :node_id, :order_id, :node_name, :handler_id, '分配', :node_content, '0'
            )
        """)
        node_name = process_data.next_node_name or "待处理"
        await session.execute(process_node_sql, {
            "node_id": process_node_id,
            "order_id": order_id,
            "node_name": node_name,
            "handler_id": process_data.to_user_id,
            "node_content": "工单已转派，等待处理",
        })
        
        # 更新工单当前节点
        update_sql = text("""
            UPDATE tbkf_work_order_info
            SET current_node_id = :node_id, status = 20
            WHERE order_id = :order_id
        """)
        await session.execute(update_sql, {"node_id": process_node_id, "order_id": order_id})
        
    else:
        # 提交/处理
        node_name = process_data.next_node_name or "处理中"
        node_sql = text("""
            INSERT INTO tbkf_work_order_node_info (
                node_id, order_id, node_name, handler_id, node_type, node_content, to_assignee_id
            ) VALUES (
                :node_id, :order_id, :node_name, :handler_id, :node_type, :node_content, '0'
            )
        """)
        await session.execute(node_sql, {
            "node_id": node_id,
            "order_id": order_id,
            "node_name": node_name,
            "handler_id": current_user_id,
            "node_type": process_data.node_type,
            "node_content": process_data.node_content or f"执行{process_data.node_type}操作",
        })
        
        # 更新工单当前节点和状态
        new_status = 30 if process_data.node_type == "提交" else 20
        update_sql = text("""
            UPDATE tbkf_work_order_info
            SET current_node_id = :node_id, status = :status
            WHERE order_id = :order_id
        """)
        await session.execute(update_sql, {"node_id": node_id, "status": new_status, "order_id": order_id})
    
    await session.commit()
    
    return {"message": "工单处理成功"}


@router.post(
    "/{order_id}/feedback",
    summary="工单反馈",
    description="为工单创建反馈，用于处理结果反馈和服务质量评价。需要提供评分（1-5分）和可选的建议内容。",
    response_description="返回创建的反馈ID和成功消息。"
)
async def create_work_order_feedback(
    order_id: str,
    feedback_data: WorkOrderFeedback,
    session: AsyncSession = Depends(get_db_session),
    current_user_id: str = Depends(get_current_user_id),
) -> dict:
    """创建工单反馈（处理结果反馈、服务质量评价）"""
    # 检查工单是否存在
    check_sql = text("SELECT order_id FROM tbkf_work_order_info WHERE order_id = :order_id")
    check_result = await session.execute(check_sql, {"order_id": order_id})
    if not check_result.first():
        raise HTTPException(status_code=404, detail="工单不存在")
    
    # 生成反馈ID
    feedback_id = str(uuid.uuid4()).replace("-", "")[:30]
    
    # 插入反馈
    insert_sql = text("""
        INSERT INTO tbkf_work_order_feedback_info (
            feedback_id, order_id, score, suggestion, feedback_time
        ) VALUES (
            :feedback_id, :order_id, :score, :suggestion, NOW()
        )
    """)
    await session.execute(insert_sql, {
        "feedback_id": feedback_id,
        "order_id": order_id,
        "score": feedback_data.score,
        "suggestion": feedback_data.suggestion,
    })
    await session.commit()
    
    return {"feedback_id": feedback_id, "message": "反馈提交成功"}


@router.get(
    "/{order_id}/progress",
    summary="获取工单处理进度",
    description="获取工单的处理进度信息，包括当前状态、所有处理节点、是否超时等。用于展示工单的流转情况和处理进度。",
    response_description="返回工单处理进度信息，包含：工单ID、状态、当前节点ID、是否超时、超时提醒、超时时间、所有节点列表和节点总数。"
)
async def get_work_order_progress(
    order_id: str,
    session: AsyncSession = Depends(get_db_session),
    current_user_id: str = Depends(get_current_user_id),
) -> dict:
    """获取工单处理进度（多节点流转）"""
    # 检查工单是否存在
    check_sql = text("""
        SELECT order_id, status, current_node_id, timeount, create_time
        FROM tbkf_work_order_info
        WHERE order_id = :order_id
    """)
    check_result = await session.execute(check_sql, {"order_id": order_id})
    order = check_result.mappings().first()
    if not order:
        raise HTTPException(status_code=404, detail="工单不存在")
    
    # 查询所有节点（注意：表结构中没有 create_time，这里假设有，如果没有需要添加该字段）
    node_sql = text("""
        SELECT node_id, node_name, node_type, node_content, to_assignee_id
        FROM tbkf_work_order_node_info
        WHERE order_id = :order_id
        ORDER BY node_id ASC
    """)
    node_result = await session.execute(node_sql, {"order_id": order_id})


    nodes = [dict(row) for row in node_result.mappings().all()]
    
    # 检查是否超时
    is_timeout = False
    timeout_reminder = False
    if order["timeount"]:
        is_timeout = datetime.now() > order["timeount"]
        # 这里可以添加超时提醒逻辑
    
    return {
        "order_id": order_id,
        "status": order["status"],
        "current_node_id": order["current_node_id"],
        "is_timeout": is_timeout,
        "timeout_reminder": timeout_reminder,
        "timeout_time": order["timeount"],
        "nodes": nodes,
        "total_nodes": len(nodes),
    }

