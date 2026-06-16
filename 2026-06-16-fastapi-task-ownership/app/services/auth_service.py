# 自定义业务异常：用户名已存在、账号密码错误
from app.exceptions import InvalidCredentialsError, UserAlreadyExistsError
# 用户数据库模型
from app.models.user import User
# 用户仓库层，负责纯数据库操作
from app.repositories.user_repository import UserRepository
# 数据模型：注册入参、登录返回token、用户信息出参
from app.schemas.auth import TokenResponse, UserRegister, UserResponse
# 安全工具：生成JWT、密码加密、密码校验
from app.security import create_access_token, hash_password, verify_password

class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository
        #依赖注入接收 UserRepository，遵循分层解耦；
        #Service 只写业务逻辑，不直接操作数据库，所有 DB 操作交给 repository。

    def register(self, data: UserRegister) -> UserResponse:
        existing_user = self.repository.get_by_username(data.username)

        if existing_user is not None:
            raise UserAlreadyExistsError(data.username)

        hashed_password = hash_password(data.password)
        user = self.repository.create(data.username, hashed_password)

        return self._to_response(user)
    #前端提交注册信息 → Service 查询用户名是否占用 → 加密密码 → 入库 → 返回脱敏后的用户信息（无密码）

    def login(self, username: str, password: str) -> TokenResponse:
        user = self.repository.get_by_username(username)

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        access_token = create_access_token(user.username)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
        )

    def _to_response(self, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            username=user.username,
            is_active=user.is_active,
        )