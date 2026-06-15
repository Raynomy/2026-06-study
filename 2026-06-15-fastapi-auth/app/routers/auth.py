from fastapi import APIRouter, Depends, status

from app.dependencies import get_auth_service
from app.schemas.auth import LoginResponse, UserLogin, UserRegister, UserResponse
from app.services.auth_service import AuthService


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: UserRegister,
    service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    return service.register(data)


@router.post("/login", response_model=LoginResponse)
def login(
    data: UserLogin,
    service: AuthService = Depends(get_auth_service),
) -> LoginResponse:
    return service.login(data.username, data.password)