# 2026-06-14-02 FastAPI Layered Architecture

这个目录是在 SQLAlchemy 版本基础上继续拆分后端分层的版本。

项目重点是把数据库访问逻辑从 `TaskService` 中拆出来，新增 `TaskRepository`，形成更清晰的后端分层结构。

## 学习目标

- 理解后端分层架构
- 区分 `models`、`schemas`、`repositories`、`services`、`routers`
- 把数据库 CRUD 从 service 层移动到 repository 层
- 让 service 层专注业务规则
- 使用 FastAPI `Depends` 组装 db、repository、service
- 理解数据库迁移的基本概念

## 项目结构

```text
2026-06-14-02-fastapi-layered-architecture/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── task_repository.py
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
├── requirements.txt
└── README.md
```

## 分层关系

这一版的核心链路是：

```text
router -> service -> repository -> database
```

对应文件：

```text
app/routers/tasks.py
app/services/task_service.py
app/repositories/task_repository.py
app/models/task.py + app/database.py
```

## 核心文件

### `app/routers/tasks.py`

路由层，负责：

- 定义 API 路径
- 接收请求体和路径参数
- 通过 `Depends` 获取 `TaskService`
- 调用 service 返回结果

路由层不直接操作数据库。

### `app/services/task_service.py`

业务逻辑层，负责：

- 调用 repository
- 处理任务不存在的业务规则
- 抛出 `TaskNotFoundError`
- 把数据库模型转换成 API 响应模型

这一版中，`TaskService` 不再直接写：

```python
self.db.query(...)
self.db.commit()
```

而是调用：

```python
self.repository.create(...)
self.repository.list()
self.repository.get_by_id(...)
self.repository.update(...)
self.repository.delete(...)
```

### `app/repositories/task_repository.py`

数据库访问层，负责：

- 创建任务
- 查询任务列表
- 按 id 查询任务
- 更新任务
- 删除任务
- 执行 `add`、`commit`、`refresh`、`query`

Repository 层只关心数据库怎么读写，不关心 HTTP、Swagger 或响应格式。

### `app/models/task.py`

数据库表模型。

定义 `tasks` 表：

- `id`
- `title`
- `description`
- `status`

### `app/schemas/task.py`

API 数据模型。

定义：

- `TaskCreate`
- `TaskUpdate`
- `TaskResponse`

注意：

```text
models
面向数据库表

schemas
面向 API 请求和响应
```

### `app/dependencies.py`

依赖注入层。

当前依赖链：

```text
get_db
-> get_task_repository
-> get_task_service
-> router
```

代码结构：

```python
def get_task_repository(...):
    return TaskRepository(db)


def get_task_service(...):
    return TaskService(repository)
```

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

## 本地运行

在本目录执行：

```bash
../.venv/bin/python -m uvicorn app.main:app --port 8000
```

访问 Swagger：

```text
http://127.0.0.1:8000/docs
```

## 运行测试

```bash
../.venv/bin/python -m pytest
```

## 这版和上一版的区别

上一版 SQLAlchemy 项目是：

```text
router -> service -> database
```

这一版升级为：

```text
router -> service -> repository -> database
```

也就是：

```text
TaskService 负责业务规则
TaskRepository 负责数据库访问
```

## 数据库迁移概念

当前项目仍然使用：

```python
Base.metadata.create_all(bind=engine)
```

它适合学习阶段创建表，但不适合真实项目管理表结构变化。

真实项目后续应该使用：

```text
Alembic
```

来管理数据库迁移。

## 当前限制

- 暂未使用 Alembic
- 暂未加入用户认证
- 暂未实现任务归属和权限隔离
- `tasks.db` 是本地开发数据库文件，不应作为正式数据源

## 后续演进

后续版本会继续加入：

- 用户注册和登录
- 密码哈希
- JWT 鉴权
- 当前用户依赖
- 任务 owner_id 权限隔离

## 一句话总结

这个练习把 FastAPI + SQLAlchemy 项目继续拆成 `router -> service -> repository -> database`，让业务逻辑和数据库访问职责更清楚。
