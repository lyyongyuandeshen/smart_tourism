from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
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

# 全局异常处理器
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """处理请求验证错误，返回详细的参数格式校验信息"""
    errors = []
    for error in exc.errors():
        field_path = " -> ".join(str(loc) for loc in error["loc"])
        error_info = {
            "field": field_path,
            "message": error["msg"],
            "invalid_value": error.get("input"),
            "error_type": error["type"]
        }
        errors.append(error_info)
    
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "参数验证失败",
            "errors": errors,
            "detail": "请检查以下字段的格式和值"
        }
    )


@app.exception_handler(ValidationError)
async def pydantic_validation_exception_handler(request: Request, exc: ValidationError):
    """处理Pydantic验证错误"""
    errors = []
    for error in exc.errors():
        field_path = " -> ".join(str(loc) for loc in error["loc"])
        error_info = {
            "field": field_path,
            "message": error["msg"],
            "invalid_value": error.get("input"),
            "error_type": error["type"]
        }
        errors.append(error_info)
    
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "message": "数据验证失败",
            "errors": errors,
            "detail": "请检查以下字段的格式和值"
        }
    )


# 注册API路由
app.include_router(api_router, prefix="/api/v1")


async def init_function():
    config.inject()


app.add_event_handler("startup", init_function)

if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8888, proxy_headers=True)
