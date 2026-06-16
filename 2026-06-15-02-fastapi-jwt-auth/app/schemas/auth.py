from pydantic import BaseModel, Field


class UserRegister(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)


class UserLogin(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str
    is_active: bool


class LoginResponse(BaseModel):
    message: str
    user: UserResponse



#UserRegister注册时客户端传 username / password
#UserLogin登录时客户端传 username / password
#UserResponse返回用户信息，不包含 hashed_password
#LoginResponse登录成功后的响应

class TokenResponse(BaseModel):
    access_token: str
    token_type: str