# 2026-06-15-02 FastAPI JWT Auth

这个目录是在用户注册 / 登录项目基础上加入 JWT 鉴权的版本。

项目重点是让登录成功后返回 `access_token`，并用 `Authorization: Bearer <token>` 保护任务接口。

## 学习目标

- 学习 JWT 基础流程
- 使用 `PyJWT` 创建和解析 token
- 登录成功后返回 `access_token`
- 使用 `OAuth2PasswordRequestForm` 适配 Swagger 登录
- 使用 `OAuth2PasswordBearer` 从请求头读取 token
- 实现 `get_current_user`
- 给 `/tasks` 接口加鉴权
- 修改测试，让任务接口请求携带 token

## 项目结构

```text
2026-06-15-02-fastapi-jwt-auth/
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
├── requirements.txt
└── README.md
```

## 核心流程

JWT 鉴权流程：

```text
1. 用户注册
2. 用户登录
3. 后端验证用户名和密码
4. 后端创建 JWT access_token
5. 客户端后续请求携带 Authorization: Bearer <token>
6. 后端解析 token，获取当前用户
7. token 有效则允许访问受保护接口
```

## 核心文件

### `app/security.py`

负责密码哈希和 JWT。

密码相关：

```python
hash_password(...)
verify_password(...)
```

JWT 相关：

```python
create_access_token(username)
decode_access_token(token)
```

token 中保存：

```text
sub
当前用户名

exp
过期时间
```

当前学习版使用：

```python
SECRET_KEY = "dev-secret-key-change-me"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

真实项目中 `SECRET_KEY` 应该放到环境变量中。

### `app/schemas/auth.py`

新增 token 响应模型：

```python
class TokenResponse(BaseModel):
    access_token: str
    token_type: str
```

登录成功返回：

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

### `app/routers/auth.py`

认证路由。

注册接口仍然接收 JSON：

```text
POST /auth/register
```

登录接口改成 OAuth2 表单：

```python
form_data: OAuth2PasswordRequestForm = Depends()
```

这样 Swagger 右上角 `Authorize` 可以直接输入用户名和密码登录。

### `app/dependencies.py`

新增：

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
```

它负责从请求头中提取：

```http
Authorization: Bearer <token>
```

新增 `get_current_user`：

```text
读取 token
解析 token
取出 username
查询数据库用户
返回当前用户
```

如果 token 无效或过期，返回：

```text
401 Unauthorized
```

### `app/routers/tasks.py`

任务接口加入：

```python
current_user: User = Depends(get_current_user)
```

这表示 `/tasks` 相关接口都需要登录后才能访问。

当前受保护接口：

- `POST /tasks`
- `GET /tasks`
- `GET /tasks/{task_id}`
- `PATCH /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

## API 列表

| 方法 | 路径 | 说明 |
|---|---|---|
| POST | `/auth/register` | 用户注册 |
| POST | `/auth/login` | 登录并返回 token |
| POST | `/tasks` | 创建任务，需要 token |
| GET | `/tasks` | 查询任务列表，需要 token |
| GET | `/tasks/{task_id}` | 查询单个任务，需要 token |
| PATCH | `/tasks/{task_id}` | 更新任务，需要 token |
| DELETE | `/tasks/{task_id}` | 删除任务，需要 token |

## Swagger 测试方式

1. 先调用 `POST /auth/register` 注册用户。

2. 点击 Swagger 右上角 `Authorize`。

3. 输入：

```text
username
password
```

4. 不需要填写：

```text
client_id
client_secret
```

5. 登录成功后，Swagger 会自动把 token 加到后续请求中。

6. 再访问 `/tasks` 接口。

未授权访问任务接口会返回：

```text
401 Unauthorized
```

## 测试变化

因为 `/tasks` 接口需要 token，测试中新增 helper：

```python
def get_auth_headers() -> dict[str, str]:
    ...
    return {"Authorization": f"Bearer {token}"}
```

任务接口测试需要传：

```python
headers=headers
```

登录接口改成表单请求后，测试中登录使用：

```python
data={
    "username": username,
    "password": password,
}
```

而不是：

```python
json={...}
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

## 当前限制

- token 里只保存 username
- 暂未实现 refresh token
- 暂未把 `SECRET_KEY` 移到环境变量
- 任务接口只要求登录，但还没有按用户隔离任务

## 后续演进

下一版会继续实现：

```text
用户只能访问自己的任务
```

也就是给任务表加入：

```text
owner_id
```

并在查询、更新、删除时按当前用户过滤。

## 一句话总结

这个练习实现了 FastAPI JWT 鉴权：登录成功返回 token，客户端通过 `Authorization: Bearer <token>` 访问受保护任务接口。
