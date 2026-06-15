from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.task_repository import TaskRepository
from app.services.task_service import TaskService


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