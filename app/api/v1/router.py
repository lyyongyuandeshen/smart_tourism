from fastapi import APIRouter
from app.api.v1.endpoints import tickets, scenic_spots, facilities, cultural_heritage, schedules, merchant_applications, \
    member_levels, sso, chat, work_orders

api_router = APIRouter()

# 注册票务相关路由
api_router.include_router(
    tickets.router,
    prefix="/tickets",
    tags=["tickets"]
)

# 注册景点相关路由
api_router.include_router(
    scenic_spots.router,
    prefix="/scenic",
    tags=["scenic"]
)

# 注册设备相关路由
api_router.include_router(
    facilities.router,
    prefix="/facilities",
    tags=["facilities"]
)

# 注册文化遗产相关路由
api_router.include_router(
    cultural_heritage.router,
    prefix="/cultural-heritage",
    tags=["cultural-heritage"]
)

# 注册排班管理相关路由
api_router.include_router(
    schedules.router,
    prefix="/schedules",
    tags=["schedules"]
)

# 注册商户申请管理相关路由
api_router.include_router(
    merchant_applications.router,
    prefix="/merchant-applications",
    tags=["merchant-applications"]
)

# 注册会员等级管理相关路由
api_router.include_router(
    member_levels.router,
    prefix="/member-levels",
    tags=["member-levels"]
)

# 注册SSO相关路由
api_router.include_router(
    sso.router,
    prefix="/sso",
    tags=["sso"]
)

# 注册聊天相关路由
api_router.include_router(
    chat.router,
    prefix="/chat",
    tags=["chat"]
)

# 注册工单管理相关路由
api_router.include_router(
    work_orders.router,
    prefix="/work-orders",
    tags=["work-orders"]
)
