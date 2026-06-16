from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService

from app.repositories.user_repository import UserRepository
from app.services.auth_service import AuthService


def get_task_repository(
    db: Annotated[Session, Depends(get_db)],
) -> TaskRepository:
    return TaskRepository(db)


def get_task_service(
    repository: Annotated[TaskRepository, Depends(get_task_repository)],
) -> TaskService:
    return TaskService(repository)

#依赖链是：
#get_db
#-> get_task_repository
#-> get_task_service
#-> router

def get_user_repository(
    db: Annotated[Session, Depends(get_db)],
) -> UserRepository:
    return UserRepository(db)


def get_auth_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> AuthService:
    return AuthService(repository)