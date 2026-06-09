from fastapi import APIRouter, Depends, status

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])


def get_task_service() -> TaskService:
    from app.main import task_service

    return task_service


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    return service.create_task(task)


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    return service.list_tasks()


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    return service.get_task(task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    update_data: TaskUpdate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    return service.update_task(task_id, update_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    service: TaskService = Depends(get_task_service),
) -> None:
    service.delete_task(task_id)