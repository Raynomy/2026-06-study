# 2026-06-14-01 FastAPI SQLAlchemy

这个目录是在 FastAPI 分层项目基础上加入 SQLite + SQLAlchemy 的版本。

项目重点是把任务数据从内存字典改成数据库持久化存储。

## 学习目标

- 学习 SQLAlchemy 基础概念
- 使用 SQLite 保存任务数据
- 定义数据库表模型 `Task`
- 使用 `Session` 执行数据库 CRUD
- 理解 `schemas` 和 `models` 的区别
- 通过 FastAPI 依赖注入提供数据库 session

## 项目结构

```text
2026-06-14-01-fastapi-sqlalchemy/
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

### `app/database.py`

数据库基础配置。

定义：

- `DATABASE_URL`
- `Base`
- `engine`
- `SessionLocal`
- `get_db`

当前使用 SQLite：

```python
DATABASE_URL = "sqlite:///./tasks.db"
```

`get_db()` 是数据库 session 的依赖函数：

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

它负责在请求开始时创建 session，在请求结束后关闭 session。

### `app/models/task.py`

定义数据库表模型。

```python
class Task(Base):
    __tablename__ = "tasks"
```

字段包括：

- `id`
- `title`
- `description`
- `status`

这个文件对应数据库里的 `tasks` 表。

### `app/services/task_service.py`

任务业务逻辑层，同时直接使用 SQLAlchemy `Session` 操作数据库。

当前版本中，service 直接执行：

```python
self.db.add(...)
self.db.commit()
self.db.refresh(...)
self.db.query(...)
self.db.delete(...)
```

也就是说，这个版本的结构是：

```text
router -> service -> database
```

后续分层架构版本会继续拆出：

```text
repository
```

### `app/schemas/task.py`

定义 API 请求和响应模型。

注意区分：

```text
schemas/task.py
用于 API 请求体和响应体

models/task.py
用于数据库表结构
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

第一次启动时会根据 SQLAlchemy model 创建 SQLite 数据库文件：

```text
tasks.db
```

## 运行测试

```bash
../.venv/bin/python -m pytest
```

## 这版和上一版的区别

上一版使用内存字典：

```text
self.tasks: dict[int, TaskResponse]
```

这一版使用 SQLite：

```text
tasks.db
```

数据会持久化保存，服务重启后仍然存在。

## 当前限制

- 数据库表结构通过 `Base.metadata.create_all()` 创建
- 暂未使用 Alembic 迁移
- service 层仍然直接操作数据库
- 暂未拆出 repository 层
- 暂未加入用户认证和权限隔离

## 后续演进

下一步会继续拆分为：

```text
router -> service -> repository -> database
```

也就是把数据库访问逻辑从 `TaskService` 中移到 `TaskRepository`。

## 一句话总结

这个练习把任务数据从内存存储升级为 SQLite 数据库存储，学习了 SQLAlchemy 的 `engine`、`Session`、`Base`、数据库 model 和基础 CRUD。
