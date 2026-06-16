from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.task_service import TaskService


def get_task_service(
    db: Annotated[Session, Depends(get_db)],
) -> TaskService:
    return TaskService(db)