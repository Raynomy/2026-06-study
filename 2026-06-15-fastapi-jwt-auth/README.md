# FastAPI Dependency Injection Task API

这是一个用于学习 FastAPI 工程化结构的任务管理 API 项目。

项目从基础 CRUD API 出发，逐步加入了：

- RESTful API 设计
- Pydantic 请求体和响应模型
- FastAPI 依赖注入
- routers / schemas / services 分层结构
- 统一异常处理
- 请求参数校验
- 请求日志和错误日志
- pytest + TestClient 自动化测试

## 1. 技术栈

- Python 3.10
- FastAPI
- Pydantic
- Uvicorn
- pytest
- TestClient

## 2. 项目结构

```text
app/
├── __init__.py
├── main.py
├── config.py
├── exceptions.py
├── logging_config.py
├── routers/
│   ├── __init__.py
│   └── tasks.py
├── schemas/
│   ├── __init__.py
│   └── task.py
└── services/
    ├── __init__.py
    └── task_service.py
tests/
└── test_tasks_api.py
```

## 3. 功能列表

- 健康检查接口
- 创建任务
- 查询任务列表
- 查询单个任务
- 更新任务
- 删除任务
- 任务不存在时返回统一错误格式
- 路径参数校验
- 请求体校验
- 请求日志
- 错误日志
- API 自动化测试

## 4. API 列表

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查 |
| GET | `/demo` | 依赖注入示例 |
| POST | `/tasks` | 创建任务 |
| GET | `/tasks` | 查询任务列表 |
| GET | `/tasks/{task_id}` | 查询单个任务 |
| PATCH | `/tasks/{task_id}` | 更新任务 |
| DELETE | `/tasks/{task_id}` | 删除任务 |


## 5. 接口说明与示例

### 5.1 健康检查

请求：

```http
GET /health
```

响应：

```json
{
  "status": "ok"
}
```

用途：

```text
用于确认 FastAPI 服务是否正常运行。
```

### 5.2 创建任务

请求：

```http
POST /tasks
```

请求体：

```json
{
  "title": "学习 FastAPI",
  "description": "练习 routers / services / schemas 分层"
}
```

响应状态码：

```text
201 Created
```

响应体：

```json
{
  "id": 1,
  "title": "学习 FastAPI",
  "description": "练习 routers / services / schemas 分层",
  "status": "todo"
}
```

### 5.3 查询任务列表

请求：

```http
GET /tasks
```

响应：

```json
[
  {
    "id": 1,
    "title": "学习 FastAPI",
    "description": "练习 routers / services / schemas 分层",
    "status": "todo"
  }
]
```

### 5.4 查询单个任务

请求：

```http
GET /tasks/1
```

响应：

```json
{
  "id": 1,
  "title": "学习 FastAPI",
  "description": "练习 routers / services / schemas 分层",
  "status": "todo"
}
```

任务不存在时：

```http
GET /tasks/999
```

响应状态码：

```text
404 Not Found
```

响应体：

```json
{
  "code": "TASK_NOT_FOUND",
  "message": "Task 999 not found"
}
```

### 5.5 更新任务

请求：

```http
PATCH /tasks/1
```

请求体：

```json
{
  "status": "doing"
}
```

响应：

```json
{
  "id": 1,
  "title": "学习 FastAPI",
  "description": "练习 routers / services / schemas 分层",
  "status": "doing"
}
```

非法状态：

```json
{
  "status": "invalid"
}
```

响应状态码：

```text
422 Unprocessable Entity
```

### 5.6 删除任务

请求：

```http
DELETE /tasks/1
```

响应状态码：

```text
204 No Content
```

说明：

```text
删除成功后不返回响应体。
```

### 5.7 参数校验示例

非法路径参数：

```http
GET /tasks/0
```

响应状态码：

```text
422 Unprocessable Entity
```

原因：

```text
task_id 使用 Path(ge=1) 限制，必须大于等于 1。
```

空标题：

```json
{
  "title": "",
  "description": "标题不能为空"
}
```

响应状态码：

```text
422 Unprocessable Entity
```

原因：

```text
title 使用 Field(min_length=1, max_length=100) 限制，不能为空。
```

## 6. 本地运行

进入项目目录：

```bash
cd /Users/xiongzehao/Desktop/python进阶/2026-06-study/2026-06-09-fastapi-dependency-injection
```

启动服务：

```bash
../.venv/bin/python -m uvicorn app.main:app --port 8000
```

访问健康检查：

```text
http://127.0.0.1:8000/health
```

访问 Swagger 文档：

```text
http://127.0.0.1:8000/docs
```

## 7. 示例请求

创建任务：

```json
{
  "title": "学习 FastAPI",
  "description": "练习依赖注入和项目结构拆分"
}
```

成功响应：

```json
{
  "id": 1,
  "title": "学习 FastAPI",
  "description": "练习依赖注入和项目结构拆分",
  "status": "todo"
}
```

任务不存在时响应：

```json
{
  "code": "TASK_NOT_FOUND",
  "message": "Task 999 not found"
}
```

## 8. 运行测试

在项目目录执行：

```bash
../.venv/bin/python -m pytest
```

当前测试覆盖：

- `GET /health`
- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`
- 任务不存在返回 `404`
- 非法路径参数返回 `422`
- 空标题返回 `422`
- 非法任务状态返回 `422`

## 9. 学习重点

### FastAPI 路由

使用 `APIRouter` 拆分任务路由：

```python
router = APIRouter(prefix="/tasks", tags=["tasks"])
```

### 依赖注入

使用 `Depends` 注入 `TaskService`：

```python
service: TaskService = Depends(get_task_service)
```

### Service 层

任务业务逻辑集中在 `TaskService` 中：

```python
service.create_task(task)
service.list_tasks()
service.get_task(task_id)
```

### 统一异常处理

通过自定义异常和异常处理器返回统一错误格式：

```json
{
  "code": "TASK_NOT_FOUND",
  "message": "Task 999 not found"
}
```

### 日志设计

使用 Python 标准库 `logging` 记录请求日志和错误日志。

请求日志示例：

```text
INFO app.main GET /tasks 200 0.0032s
```

错误日志示例：

```text
ERROR app.main TaskNotFoundError path=/tasks/999 message=Task 999 not found
```

### 自动化测试

使用 `pytest` 和 `TestClient` 自动测试 API，减少手动 Swagger 测试。

## 10. 当前限制

- 当前任务数据保存在内存中，服务重启后会丢失
- 暂未接入数据库
- 暂未加入用户认证和权限控制
- 暂未接入真实 Agent 或 LLM

## 11. 后续计划

- 接入 SQLite / PostgreSQL
- 增加数据库 session 依赖
- 增加用户认证
- 增加 Agent Run API
- 增加任务执行 trace
- 接入 LLM 和工具调用