from app.exceptions import TaskNotFoundError
from app.models.task import Task
from app.models.user import User
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task: TaskCreate, current_user: User) -> TaskResponse:
        db_task = self.repository.create(task, owner_id=current_user.id)
        return self._to_response(db_task)

    def list_tasks(self, current_user: User) -> list[TaskResponse]:
        db_tasks = self.repository.list_by_owner(owner_id=current_user.id)
        return [self._to_response(task) for task in db_tasks]

    def get_task(self, task_id: int, current_user: User) -> TaskResponse:
        db_task = self.repository.get_by_id_and_owner(
            task_id=task_id,
            owner_id=current_user.id,
        )

        if db_task is None:
            raise TaskNotFoundError(task_id)

        return self._to_response(db_task)

    def update_task(
        self,
        task_id: int,
        update_data: TaskUpdate,
        current_user: User,
    ) -> TaskResponse:
        db_task = self.repository.get_by_id_and_owner(
            task_id=task_id,
            owner_id=current_user.id,
        )

        if db_task is None:
            raise TaskNotFoundError(task_id)

        updated_task = self.repository.update(db_task, update_data)

        return self._to_response(updated_task)

    def delete_task(self, task_id: int, current_user: User) -> None:
        db_task = self.repository.get_by_id_and_owner(
            task_id=task_id,
            owner_id=current_user.id,
        )

        if db_task is None:
            raise TaskNotFoundError(task_id)

        self.repository.delete(db_task)

    def _to_response(self, task: Task) -> TaskResponse:
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
        )