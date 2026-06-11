from fastapi import APIRouter, Depends, Path, status

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService
from app.dependencies import get_task_service


router = APIRouter(prefix="/tasks", tags=["tasks"]) #RESTful API 设计



@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED) #RESTful API 设计
def create_task(
    task: TaskCreate,
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    return service.create_task(task)


@router.get("", response_model=list[TaskResponse]) #RESTful API 设计
def list_tasks(
    service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    return service.list_tasks()


@router.get("/{task_id}", response_model=TaskResponse) #RESTful API 设计
def get_task(
    task_id: int = Path(ge=1),
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    return service.get_task(task_id)


@router.patch("/{task_id}", response_model=TaskResponse) #RESTful API 设计
def update_task(
    update_data: TaskUpdate,
    task_id: int = Path(ge=1),
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    return service.update_task(task_id, update_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT) #RESTful API 设计
def delete_task(
    task_id: int = Path(ge=1),
    service: TaskService = Depends(get_task_service),
) -> None:
    service.delete_task(task_id)