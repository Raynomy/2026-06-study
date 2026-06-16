from app.exceptions import InvalidCredentialsError, UserAlreadyExistsError
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginResponse, UserRegister, UserResponse
from app.security import hash_password, verify_password


class AuthService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def register(self, data: UserRegister) -> UserResponse:
        existing_user = self.repository.get_by_username(data.username)

        if existing_user is not None:
            raise UserAlreadyExistsError(data.username)

        hashed_password = hash_password(data.password)
        user = self.repository.create(data.username, hashed_password)

        return self._to_response(user)

    def login(self, username: str, password: str) -> LoginResponse:
        user = self.repository.get_by_username(username)

        if user is None:
            raise InvalidCredentialsError()

        if not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError()

        return LoginResponse(
            message="Login successful",
            user=self._to_response(user),
        )

    def _to_response(self, user: User) -> UserResponse:
        return UserResponse(
            id=user.id,
            username=user.username,
            is_active=user.is_active,
        )