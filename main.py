from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_router
from app.config.config import config

app = FastAPI(
    title="智慧旅游系统API",
    description="智慧旅游系统后端接口",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# 注册API路由
app.include_router(api_router, prefix="/api/v1")


async def init_function():
    config.inject()


app.add_event_handler("startup", init_function)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8090, proxy_headers=True)
