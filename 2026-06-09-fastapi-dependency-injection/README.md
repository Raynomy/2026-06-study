# 2026-06-09 FastAPI Dependency Injection

这个目录是在 FastAPI 基础 CRUD 项目上继续演进的版本。

项目重点是把第一天集中在 `main.py` 里的代码拆成更接近真实后端项目的结构，并学习 FastAPI 的依赖注入、统一异常处理、日志和自动化测试。

## 学习目标

- 使用 `APIRouter` 拆分路由
- 使用 `Depends` 注入业务服务
- 拆分 `routers`、`schemas`、`services`
- 增加 `config.py` 管理基础配置
- 增加 `dependencies.py` 管理依赖对象
- 实现统一异常处理
- 使用 `Path` 和 Pydantic 做参数校验
- 增加请求日志和错误日志
- 使用 `pytest` + `TestClient` 测试 API

## 项目结构

```text
2026-06-09-fastapi-dependency-injection/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py
│   └── services/
│       ├── __init__.py
│       └── task_service.py
├── tests/
│   └── test_tasks_api.py
└── README.md
```

## 核心文件

### `app/main.py`

应用入口，负责：

- 创建 FastAPI app
- 加载配置
- 注册请求日志 middleware
- 注册异常处理器
- 保留 `/health` 和 `/demo`
- 注册任务 router

### `app/routers/tasks.py`

任务 API 路由层。

负责定义：

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

路由层只负责接收请求和调用 service。

### `app/services/task_service.py`

任务业务逻辑层。

当前版本仍然使用内存字典保存任务数据：

```text
self.tasks
self.next_task_id
```

所以服务重启后任务数据会丢失。

### `app/dependencies.py`

依赖注入层。

这里创建一个全局 `TaskService` 实例，并通过依赖函数提供给路由：

```python
task_service = TaskService()


def get_task_service() -> TaskService:
    return task_service
```

路由中使用：

```python
service: TaskService = Depends(get_task_service)
```

### `app/schemas/task.py`

任务相关 Pydantic 模型。

包含：

- `TaskCreate`
- `TaskUpdate`
- `TaskResponse`
- `TaskStatus`

用于请求体校验、响应模型和 Swagger 文档生成。

### `app/exceptions.py`

定义业务异常：

```python
TaskNotFoundError
```

当任务不存在时，service 层抛出业务异常，`main.py` 统一转换成 HTTP 响应。

### `app/logging_config.py`

配置 Python 标准库 `logging`。

项目中记录：

- 请求方法
- 请求路径
- 响应状态码
- 请求耗时
- 业务错误信息

### `tests/test_tasks_api.py`

使用 `pytest` 和 `TestClient` 测试 API。

覆盖：

- 健康检查
- 创建任务
- 查询任务列表
- 查询单个任务
- 更新任务
- 删除任务
- 任务不存在返回 `404`
- 非法路径参数返回 `422`
- 请求体校验失败返回 `422`

## API 列表

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查 |
| GET | `/demo` | 依赖注入示例 |
| POST | `/tasks` | 创建任务 |
| GET | `/tasks` | 查询任务列表 |
| GET | `/tasks/{task_id}` | 查询单个任务 |
| PATCH | `/tasks/{task_id}` | 更新任务 |
| DELETE | `/tasks/{task_id}` | 删除任务 |

## 示例请求

创建任务：

```json
{
  "title": "学习 FastAPI",
  "description": "练习 routers / services / schemas 分层"
}
```

成功响应：

```json
{
  "id": 1,
  "title": "学习 FastAPI",
  "description": "练习 routers / services / schemas 分层",
  "status": "todo"
}
```

任务不存在时：

```json
{
  "code": "TASK_NOT_FOUND",
  "message": "Task 999 not found"
}
```

## 本地运行

在本目录执行：

```bash
../.venv/bin/python -m uvicorn app.main:app --port 8000
```

访问：

```text
http://127.0.0.1:8000/docs
```

## 运行测试

在本目录执行：

```bash
../.venv/bin/python -m pytest
```

## 当前特点

这个版本完成了从单文件 CRUD 到分层结构的第一次升级。

核心变化：

```text
main.py 不再负责所有事情
router 负责 API
service 负责业务
schema 负责数据模型
dependencies 负责注入服务对象
```

## 当前限制

- 任务数据仍保存在内存中
- 服务重启后任务会丢失
- 暂未接入数据库
- 暂未加入用户认证
- 暂未实现用户权限隔离

## 后续演进

后续项目会继续加入：

- SQLite + SQLAlchemy
- Repository 层
- 用户注册和登录
- JWT 鉴权
- 任务归属和权限隔离

## 一句话总结

这个练习把 FastAPI 任务 CRUD 项目从单文件写法升级为 `routers / schemas / services / dependencies` 分层结构，并加入异常处理、日志和自动化测试。
