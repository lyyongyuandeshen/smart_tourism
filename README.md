# 智慧旅游系统 - 快速开始指南

## 项目概述

智慧旅游系统后端API，提供景点导览管理、票务管理、时段管理等功能。

## 功能模块

### 1. 票务管理
- 查询景点可用时段余票
- 购票（自动生成电子票和销售记录）

### 2. 景点导览管理
- 景点导览信息的增删查改
- 支持历史背景、文化价值、建筑特色等详细信息
- 支持开放状态管理

### 3. 时段管理
- 按景点管理票余量表
- 单个时段创建
- 批量时段创建（多日期 × 多时段）
- 时段查询（支持日期范围筛选）
- 时段配额更新
- 时段删除（单个/批量）

### 4. SSO单点登录集成
- 支持思明项目SSO集成
- 获取授权码
- 获取授权Token
- 获取用户信息
- 一键登录（使用code直接获取用户信息）

## SSO集成详细说明

### SSO集成流程

1. **前端获取授权URL**
   ```bash
   GET /api/v1/sso/auth-url?callback_url=http://127.0.0.1:8000/callback
   ```

2. **用户授权**
   - 前端重定向用户到授权URL
   - 用户在SSO页面完成登录授权
   - 授权成功后跳转回callback_url并携带授权码

3. **后端处理登录**
   ```bash
   POST /api/v1/sso/login
   {
     "code": "授权码",
     "client_id": "qoos2xwcpl0svmf7",
     "client_secret": "b5hjzmqc62u0wx861q89t8mcjvh9f5gu"
   }
   ```

### SSO接口列表

**Base URL**: `http://localhost:8090/api/v1/sso`

- `GET /auth-url` - 获取SSO授权URL
- `GET /redirect` - 直接重定向到SSO授权页面
- `POST /access-token` - 获取访问令牌
- `POST /user-info` - 获取用户信息
- `POST /login` - SSO一键登录（推荐）
- `GET /callback` - SSO授权回调处理
- `POST /validate-token` - 验证访问令牌
- `GET /config` - 获取SSO配置信息

### 测试SSO功能

```bash
# 运行SSO接口测试
python test_sso_api.py
```

### SSO配置信息

- **授权服务地址**: `https://test-api.smdata.com.cn/wisdomSimingApp/sso`
- **API服务地址**: `http://115.190.160.216/api/v1`
- **客户端ID**: `qoos2xwcpl0svmf7`
- **客户端密钥**: `b5hjzmqc62u0wx861q89t8mcjvh9f5gu`

### 用户信息字段说明

SSO登录成功后返回的用户信息包含：
- `user_id`: 用户唯一标识
- `username`: 用户名
- `real_name`: 真实姓名
- `mobile`: 手机号
- `email`: 邮箱地址
- `credit_id`: 身份证号
- `company`: 公司信息
- `departments`: 部门信息列表

## 环境要求

- Python 3.8+
- MySQL 5.7+
- pip

## 安装步骤

### 1. 克隆项目

```bash
cd /Users/arthurlee/PycharmProjects/smart_tourism
```

### 2. 安装依赖

```bash
pip install fastapi uvicorn pydantic mysql-connector-python python-dotenv
```

或使用requirements.txt：

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件或设置环境变量：

```bash
export MYSQL_HOST=127.0.0.1
export MYSQL_PORT=3306
export MYSQL_USER=root
export MYSQL_PASSWORD=your_password
export MYSQL_DATABASE=smart_tourism
export MYSQL_POOL_SIZE=5
export MYSQL_POOL_TIMEOUT=30
export MYSQL_CHARSET=utf8mb4
export MYSQL_AUTOCOMMIT=true
```

### 4. 初始化数据库

```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS smart_tourism DEFAULT CHARSET utf8mb4;"

# 创建表
mysql -u root -p smart_tourism < create_tables.sql

# 插入测试数据（可选）
mysql -u root -p smart_tourism < test_data.sql
mysql -u root -p smart_tourism < test_scenic_data.sql
```

### 5. 启动应用

```bash
python main.py
```

应用将在 `http://0.0.0.0:8090` 启动

## 访问API文档

启动后访问以下地址：

- **Swagger UI**: http://localhost:8090/docs
- **ReDoc**: http://localhost:8090/redoc

## 快速测试

### 方式1：使用测试脚本

```bash
# 测试票务接口
python test_ticket_api.py

# 测试景点接口
python test_scenic_api.py
```

### 方式2：使用curl

```bash
# 查询所有景点导览
curl http://localhost:8090/api/v1/scenic/guides

# 查询景点余票
curl http://localhost:8090/api/v1/tickets/time-slots/scenic-001

# 创建景点导览
curl -X POST http://localhost:8090/api/v1/scenic/guides \
  -H "Content-Type: application/json" \
  -d '{
    "scenic_id": "scenic-001",
    "guide_title": "黄山风景区导览",
    "open_status": 1
  }'

# 批量创建时段
curl -X POST http://localhost:8090/api/v1/scenic/time-slots/batch \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "ticket-001",
    "scenic_id": "scenic-001",
    "reservation_dates": ["2025-11-26", "2025-11-27"],
    "time_slots": [
      {"start_time": "09:00", "end_time": "11:00", "total_quota": 100},
      {"start_time": "14:00", "end_time": "16:00", "total_quota": 100}
    ]
  }'
```

### 方式3：使用Postman

导入以下接口到Postman：

**Base URL**: `http://localhost:8090/api/v1`

**景点接口**:
- POST `/scenic/guides` - 创建景点导览
- GET `/scenic/guides` - 查询所有导览
- GET `/scenic/guides/{guide_id}` - 查询单个导览
- PUT `/scenic/guides/{guide_id}` - 更新导览
- DELETE `/scenic/guides/{guide_id}` - 删除导览

**时段接口**:
- POST `/scenic/time-slots` - 创建时段
- POST `/scenic/time-slots/batch` - 批量创建时段
- GET `/scenic/time-slots/scenic/{scenic_id}` - 查询景点时段
- PUT `/scenic/time-slots/{slot_id}` - 更新时段
- DELETE `/scenic/time-slots/{slot_id}` - 删除时段

**票务接口**:
- GET `/tickets/time-slots/{scenic_id}` - 查询余票
- POST `/tickets/purchase` - 购票

## 项目结构

```
smart_tourism/
├── app/
│   ├── models/              # 数据模型
│   │   ├── ticket_models.py
│   │   └── scenic_models.py
│   ├── repository/          # 数据仓储层
│   │   ├── base_repo.py
│   │   ├── ticket_repo.py
│   │   └── scenic_repo.py
│   ├── services/            # 业务服务层
│   │   ├── ticket_service.py
│   │   └── scenic_service.py
│   ├── api/                 # API接口层
│   │   └── v1/
│   │       ├── endpoints/
│   │       │   ├── tickets.py
│   │       │   └── scenic_spots.py
│   │       └── router.py
│   └── config/              # 配置管理
│       ├── config.py
│       └── mysql_config.py
├── main.py                  # 应用入口
├── create_tables.sql        # 建表SQL
├── test_data.sql            # 票务测试数据
├── test_scenic_data.sql     # 景点测试数据
├── test_ticket_api.py       # 票务接口测试
├── test_scenic_api.py       # 景点接口测试
├── TICKET_API.md            # 票务接口文档
├── SCENIC_API.md            # 景点接口文档
├── IMPLEMENTATION_SUMMARY.md # 票务实现总结
├── SCENIC_IMPLEMENTATION.md  # 景点实现总结
└── README.md                # 本文件
```

## 核心功能演示

### 1. 新景点上线流程

```bash
# Step 1: 创建景点导览
curl -X POST http://localhost:8090/api/v1/scenic/guides \
  -H "Content-Type: application/json" \
  -d '{
    "scenic_id": "scenic-huangshan",
    "guide_title": "黄山风景区导览",
    "historical_background": "黄山，古称黟山...",
    "open_status": 1,
    "last_bus_time": "17:30"
  }'

# Step 2: 批量创建未来7天的时段
curl -X POST http://localhost:8090/api/v1/scenic/time-slots/batch \
  -H "Content-Type: application/json" \
  -d '{
    "ticket_id": "ticket-001",
    "scenic_id": "scenic-huangshan",
    "reservation_dates": ["2025-11-26", "2025-11-27", "2025-11-28", "2025-11-29", "2025-11-30", "2025-12-01", "2025-12-02"],
    "time_slots": [
      {"start_time": "09:00", "end_time": "11:00", "total_quota": 100},
      {"start_time": "11:00", "end_time": "13:00", "total_quota": 100},
      {"start_time": "14:00", "end_time": "16:00", "total_quota": 100},
      {"start_time": "16:00", "end_time": "18:00", "total_quota": 100}
    ]
  }'

# Step 3: 验证时段创建
curl "http://localhost:8090/api/v1/scenic/time-slots/scenic/scenic-huangshan"
```

### 2. 用户购票流程

```bash
# Step 1: 查询可用时段
curl http://localhost:8090/api/v1/tickets/time-slots/scenic-huangshan

# Step 2: 选择时段购票
curl -X POST http://localhost:8090/api/v1/tickets/purchase \
  -H "Content-Type: application/json" \
  -d '{
    "scenic_id": "scenic-huangshan",
    "scenic_name": "黄山风景区",
    "time_slot_id": "slot-xxx",
    "ticket_type": 1,
    "ticket_quantity": 2,
    "ticket_price": 190.00,
    "sales_channel": 1,
    "channel_name": "官网",
    "valid_start_date": "2025-11-26",
    "valid_end_date": "2025-11-26"
  }'
```

## 常见问题

### 1. 数据库连接失败

检查环境变量配置是否正确，确保MySQL服务已启动。

### 2. 端口被占用

修改 `main.py` 中的端口号：

```python
uvicorn.run("main:app", host="0.0.0.0", port=8091, proxy_headers=True)
```

### 3. 导入模块失败

确保在项目根目录下运行，或将项目路径添加到PYTHONPATH：

```bash
export PYTHONPATH=/Users/arthurlee/PycharmProjects/smart_tourism:$PYTHONPATH
```

## 开发建议

### 1. 代码规范

- 遵循PEP 8编码规范
- 使用类型注解
- 编写文档字符串

### 2. 测试

- 编写单元测试
- 编写集成测试
- 使用pytest框架

### 3. 日志

- 添加日志记录
- 使用logging模块
- 区分不同日志级别

### 4. 安全

- 添加认证授权
- 使用HTTPS
- 防止SQL注入
- 添加请求频率限制

## 文档链接

- [票务接口文档](TICKET_API.md)
- [景点接口文档](SCENIC_API.md)
- [票务实现总结](IMPLEMENTATION_SUMMARY.md)
- [景点实现总结](SCENIC_IMPLEMENTATION.md)

## 技术栈

- **框架**: FastAPI
- **数据库**: MySQL
- **ORM**: 原生SQL（使用mysql-connector-python）
- **数据验证**: Pydantic
- **API文档**: Swagger UI / ReDoc

## 联系方式

如有问题，请联系开发团队。

## 许可证

MIT License