from fastapi import APIRouter
from app.api.v1.endpoints import tickets, scenic_spots

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
