# 2026-06-08 FastAPI Basic

这个目录是 FastAPI 基础 CRUD 练习。

项目重点是先用最直观的方式，把 FastAPI 的完整 API 流程跑通：

```text
创建 app
定义路由
接收请求体
返回响应模型
实现任务 CRUD
处理 404 错误
```

## 学习目标

- 理解 `app = FastAPI()`
- 使用 `@app.get()` / `@app.post()` / `@app.patch()` / `@app.delete()` 注册路由
- 使用 Pydantic 定义请求体和响应模型
- 理解 RESTful API 风格
- 实现任务 CRUD
- 使用内存字典临时保存数据
- 使用 `HTTPException` 返回错误响应

## 项目结构

```text
2026-06-08-fastapi-basic/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── schemas.py
└── README.md
```

## 核心文件

### `app/main.py`

这是 FastAPI 应用入口，也是第一版单文件 CRUD 示例。

主要内容：

- 创建 FastAPI 应用
- 定义 `/health` 健康检查接口
- 用内存字典保存任务
- 实现任务创建、查询、更新、删除
- 使用 `HTTPException` 处理任务不存在

临时数据存储：

```python
tasks: dict[int, TaskResponse] = {}
next_task_id = 1
```

这表示任务只保存在程序内存中，服务重启后数据会丢失。

### `app/schemas.py`

这个文件定义任务相关 Pydantic 模型。

包含：

- `TaskCreate`
- `TaskUpdate`
- `TaskResponse`
- `TaskStatus`

`TaskCreate` 用于创建任务请求体。

`TaskUpdate` 用于局部更新任务。

`TaskResponse` 用于接口响应模型。

## API 列表

| 方法 | 路径 | 说明 |
|---|---|---|
| GET | `/health` | 健康检查 |
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
  "description": "实现基础 CRUD"
}
```

成功响应：

```json
{
  "id": 1,
  "title": "学习 FastAPI",
  "description": "实现基础 CRUD",
  "status": "todo"
}
```

任务不存在时：

```json
{
  "detail": "Task 999 not found"
}
```

## 本地运行

在本目录执行：

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

## 当前特点

这个版本的特点是：

```text
所有逻辑集中在 main.py
```

包括：

- 路由
- 业务逻辑
- 数据存储
- 错误处理

这种写法适合入门阶段理解 FastAPI 的完整流程。

后续项目会继续拆分成：

```text
routers
schemas
services
repositories
models
```

## 一句话总结

这个练习用 FastAPI 实现了一个内存版任务 CRUD API，帮助理解路由、请求体、响应模型、RESTful API 和基础错误处理。
