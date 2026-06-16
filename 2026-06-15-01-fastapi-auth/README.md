# 2026-06-15-01 FastAPI Auth

这个目录是在分层架构项目基础上加入用户注册和登录的版本。

项目重点是实现认证系统的基础闭环：

```text
注册用户
哈希密码
保存用户
登录校验
返回登录结果
```

这一版还没有 JWT，登录成功后返回 `message + user`。

## 学习目标

- 理解用户注册流程
- 理解用户登录流程
- 创建 `users` 数据表
- 使用 `pwdlib[argon2]` 做密码哈希
- 保存 `hashed_password`，不保存明文密码
- 拆分 auth router、auth service、user repository
- 测试注册成功、重复注册、登录成功、登录失败

## 项目结构

```text
2026-06-15-01-fastapi-auth/
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
│   │   ├── task.py
│   │   └── user.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── task_repository.py
│   │   └── user_repository.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── tasks.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── task.py
│   ├── security.py
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py
│       └── task_service.py
├── tests/
│   └── test_tasks_api.py
├── requirements.txt
└── README.md
```

## 核心文件

### `app/models/user.py`

定义 `users` 表。

字段包括：

- `id`
- `username`
- `hashed_password`
- `is_active`

关键点：

```text
数据库不保存 password
数据库只保存 hashed_password
```

### `app/schemas/auth.py`

定义认证相关 API 模型。

包含：

- `UserRegister`
- `UserLogin`
- `UserResponse`
- `LoginResponse`

`UserResponse` 和 `LoginResponse` 都不会返回密码相关字段。

### `app/security.py`

负责密码哈希和密码验证。

核心函数：

```python
hash_password(password)
verify_password(plain_password, hashed_password)
```

注册时：

```text
明文 password -> hash_password -> hashed_password
```

登录时：

```text
输入的 password + 数据库 hashed_password -> verify_password
```

### `app/repositories/user_repository.py`

用户数据库访问层。

负责：

- 根据 username 查询用户
- 创建用户
- 执行数据库 `add`、`commit`、`refresh`

### `app/services/auth_service.py`

认证业务逻辑层。

注册流程：

```text
查询 username 是否存在
-> 已存在则抛 UserAlreadyExistsError
-> 不存在则哈希密码
-> 创建用户
-> 返回 UserResponse
```

登录流程：

```text
查询 username
-> 用户不存在则抛 InvalidCredentialsError
-> 校验密码
-> 密码错误则抛 InvalidCredentialsError
-> 登录成功返回 LoginResponse
```

### `app/routers/auth.py`

认证路由。

新增接口：

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/auth/register` | 用户注册 |
| POST | `/auth/login` | 用户登录 |

这一版 `/auth/login` 接收 JSON 请求体。

## API 示例

注册：

```http
POST /auth/register
```

请求体：

```json
{
  "username": "alice",
  "password": "123456"
}
```

成功响应：

```json
{
  "id": 1,
  "username": "alice",
  "is_active": true
}
```

登录：

```http
POST /auth/login
```

请求体：

```json
{
  "username": "alice",
  "password": "123456"
}
```

成功响应：

```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "alice",
    "is_active": true
  }
}
```

重复注册：

```json
{
  "code": "USER_ALREADY_EXISTS",
  "message": "User alice already exists"
}
```

登录失败：

```json
{
  "code": "INVALID_CREDENTIALS",
  "message": "Invalid username or password"
}
```

## 本地运行

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

测试覆盖：

- 注册成功
- 重复注册返回 `409`
- 登录成功
- 密码错误返回 `401`
- 用户不存在返回 `401`
- 响应中不返回 `password` 或 `hashed_password`

## 当前限制

- 登录成功后还不返回 token
- 暂未实现 JWT
- 暂未实现当前用户依赖
- 暂未保护任务接口
- 暂未实现用户只能访问自己的任务

## 后续演进

下一版会加入：

- JWT access token
- `Authorization: Bearer <token>`
- `get_current_user`
- 任务接口鉴权

## 一句话总结

这个练习实现了 FastAPI 用户注册和登录基础流程，重点是用户表、密码哈希、认证 service 和注册登录接口，为后续 JWT 鉴权打基础。
