# 2026-06-16 FastAPI Task Ownership

这个目录是在 JWT 鉴权项目基础上加入任务权限隔离的版本。

项目重点是让任务和当前登录用户绑定，实现：

```text
用户只能访问自己的任务
```

## 项目亮点

- 使用 FastAPI 实现 RESTful CRUD API
- 使用 Pydantic 定义请求体和响应模型
- 使用 SQLAlchemy + SQLite 保存用户和任务数据
- 使用 Repository / Service / Router 分层组织代码
- 使用密码哈希保存用户密码，不保存明文密码
- 使用 JWT 实现登录后 token 鉴权
- 使用 `OAuth2PasswordBearer` 保护任务接口
- 使用 `owner_id` 实现用户任务权限隔离
- 使用统一异常格式返回业务错误
- 使用 pytest + TestClient 覆盖核心接口
- 使用 Dockerfile 打包 FastAPI 运行环境

## 学习目标

- 理解认证和授权的区别
- 给任务表增加 `owner_id`
- 创建任务时绑定当前用户
- 查询任务时按当前用户过滤
- 防止用户查看、修改、删除别人的任务
- 补充多用户权限隔离测试

## 核心概念

认证 Authentication：

```text
确认你是谁
```

授权 Authorization：

```text
确认你能访问什么
```

JWT 解决的是：

```text
通过 token 获取当前用户
```

任务权限隔离解决的是：

```text
只允许 current_user.id 操作 owner_id 等于自己的任务
```

数据库 Database：

```text
用 SQLite 保存用户和任务数据
用 SQLAlchemy 模型描述数据库表结构
```

Docker：

```text
把 FastAPI 项目和 Python 依赖打包成可运行的容器镜像
```

## 技术栈

```text
Python 3.10
FastAPI
Pydantic
SQLAlchemy
SQLite
PyJWT
pwdlib
pytest
Docker
```

## 项目结构

```text
2026-06-16-fastapi-task-ownership/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── dependencies.py
│   ├── exceptions.py
│   ├── logging_config.py
│   ├── models/
│   │   ├── task.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── task_repository.py
│   │   └── user_repository.py
│   ├── routers/
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── schemas/
│   │   ├── auth.py
│   │   └── task.py
│   ├── security.py
│   └── services/
│       ├── auth_service.py
│       └── task_service.py
├── tests/
│   └── test_tasks_api.py
├── .dockerignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## 主要改动

### 0. 分层结构

当前项目按后端常见分层组织：

```text
routers
接收 HTTP 请求，负责路径、状态码、依赖注入

schemas
定义请求和响应的数据结构

models
定义数据库表结构

repositories
封装数据库 CRUD 操作

services
编写业务逻辑

dependencies
提供数据库 session、service、current_user 等依赖
```

请求大致流向：

```text
HTTP 请求
-> router
-> service
-> repository
-> database
```

### 1. Task 表新增 owner_id

文件：

```text
app/models/task.py
```

新增：

```python
owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
```

含义：

```text
每个任务都属于某个用户
owner_id 对应 users.id
```

### 2. 数据库保存数据

用户表：

```text
users
```

保存：

```text
id
username
hashed_password
is_active
```

任务表：

```text
tasks
```

保存：

```text
id
title
description
status
owner_id
```

相比早期内存版项目，数据库版的变化是：

```text
数据不再只存在 Python 列表中
而是保存到 SQLite 数据库文件中
```

### 3. Repository 按 owner_id 过滤

文件：

```text
app/repositories/task_repository.py
```

主要方法变成：

```text
create(task, owner_id)
list_by_owner(owner_id)
get_by_id_and_owner(task_id, owner_id)
```

核心查询：

```python
.filter(Task.id == task_id, Task.owner_id == owner_id)
```

这样即使任务 id 存在，只要不属于当前用户，也查不到。

### 4. Service 接收 current_user

文件：

```text
app/services/task_service.py
```

任务 service 方法开始接收：

```python
current_user: User
```

创建任务时：

```python
owner_id=current_user.id
```

查询、更新、删除时：

```text
都使用 current_user.id 作为 owner_id 过滤条件
```

### 5. Router 传入 current_user

文件：

```text
app/routers/tasks.py
```

任务接口通过：

```python
current_user: User = Depends(get_current_user)
```

拿到当前登录用户，再传给 service：

```python
service.create_task(task, current_user)
service.list_tasks(current_user)
service.get_task(task_id, current_user)
service.update_task(task_id, update_data, current_user)
service.delete_task(task_id, current_user)
```

### 6. JWT 鉴权

登录成功后返回：

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

之后访问任务接口时，请求头携带：

```http
Authorization: Bearer <token>
```

后端通过 `get_current_user`：

```text
读取 token
解析 token
取出 username
查询用户
返回当前用户
```

## 权限规则

当前任务接口规则：

| 接口 | 权限行为 |
|---|---|
| `POST /tasks` | 创建当前用户自己的任务 |
| `GET /tasks` | 只返回当前用户自己的任务 |
| `GET /tasks/{task_id}` | 只能查询当前用户自己的任务 |
| `PATCH /tasks/{task_id}` | 只能更新当前用户自己的任务 |
| `DELETE /tasks/{task_id}` | 只能删除当前用户自己的任务 |

没有 token：

```text
401 Unauthorized
```

访问别人的任务：

```text
404 Not Found
```

这里使用 `404`，是为了不暴露：

```text
这个任务其实存在，只是不属于你
```

## 测试覆盖

测试文件：

```text
tests/test_tasks_api.py
```

新增多用户权限隔离测试：

- Alice 创建任务，Bob 的任务列表看不到
- Alice 创建任务，Bob 用 id 查询返回 `404`
- Alice 创建任务，Bob 修改返回 `404`
- Alice 创建任务，Bob 删除返回 `404`
- Bob 修改失败后，Alice 的任务状态不变
- Bob 删除失败后，Alice 仍然能查到任务

最终测试：

```text
19 passed
```

## 本地运行

```bash
../.venv/bin/python -m uvicorn app.main:app --port 8000
```

访问 Swagger：

```text
http://127.0.0.1:8000/docs
```

## Docker 入门

Docker 的作用是把项目代码、Python 环境和依赖打包到一个统一的运行环境里。

这次新增两个文件：

```text
Dockerfile
.dockerignore
```

`Dockerfile` 用来描述镜像如何构建：

```text
1. 使用 Python 3.10 基础镜像
2. 进入容器内的 /app 目录
3. 复制 requirements.txt
4. 安装项目依赖
5. 复制 app 代码
6. 暴露 8000 端口
7. 启动 uvicorn
```

`.dockerignore` 用来排除不需要进入镜像的本地文件：

```text
.venv
__pycache__
.pytest_cache
*.pyc
tasks.db
.git
.DS_Store
```

其中 `tasks.db` 不打进镜像，容器运行时会重新创建数据库文件。

构建镜像：

```bash
docker build -t fastapi-task-ownership .
```

运行容器：

```bash
docker run --name fastapi-task-ownership-container -p 8000:8000 fastapi-task-ownership
```

访问接口文档：

```text
http://127.0.0.1:8000/docs
```

测试健康检查：

```text
http://127.0.0.1:8000/health
```

本次 Docker 测试流程：

```text
1. 构建镜像成功
2. 容器启动 FastAPI 成功
3. /docs 可以打开
4. /health 返回正常
5. 在 Swagger 中完成注册、登录、创建任务、查询任务
```

## 运行测试

```bash
../.venv/bin/python -m pytest
```

## 数据库说明

因为 `Task` 表新增了 `owner_id` 字段，学习阶段删除旧的本地 SQLite 数据库文件后重新建表。

真实项目中不应该直接删库，而应该使用：

```text
Alembic 数据库迁移
```

## 当前项目能力

这个项目已经具备一个小型 FastAPI 后端的基本形态：

```text
接口层
数据模型
数据库表
数据库操作层
业务逻辑层
用户注册
密码哈希
JWT 登录
接口鉴权
权限隔离
自动化测试
Docker 运行
```

## 当前限制

- SQLite 适合学习和本地开发，正式项目通常会使用 PostgreSQL 或 MySQL
- 数据库迁移还没有接入 Alembic
- JWT secret 仍是学习阶段配置，真实项目应使用环境变量
- token 只有 access token，还没有 refresh token
- 任务功能还比较简单，没有分页、搜索、排序
- Docker 还没有加入 docker-compose

## 后续可以继续完善

- 接入 Alembic 做数据库迁移
- 使用环境变量管理 `SECRET_KEY` 和数据库地址
- 增加 refresh token
- 增加分页查询
- 增加 docker-compose
- 接入 PostgreSQL
- 增加更完整的 README API 示例
- 开始做 Agent 后端项目

## 和 Agent 项目的关系

后续 Agent 项目也需要类似权限隔离：

- 用户只能查看自己的 Agent 任务
- 用户只能查看自己的文档
- 用户只能查看自己的对话记录
- 用户只能查看自己的 trace

这些资源都可以通过类似的字段绑定用户：

```text
owner_id
user_id
```

## 一句话总结

这个练习通过给任务增加 `owner_id`，让所有任务操作都基于 `current_user.id` 过滤，实现了用户只能访问自己任务的权限隔离。
