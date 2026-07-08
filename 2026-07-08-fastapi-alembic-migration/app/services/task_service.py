from sqlalchemy.orm import Session

from app.exceptions import TaskNotFoundError
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


class TaskService:
    def __init__(self, db: Session):
        self.db = db

    def create_task(self, task: TaskCreate) -> TaskResponse:
        db_task = Task(
            title=task.title,
            description=task.description,
            status="todo",
        )

        self.db.add(db_task)
        self.db.commit()
        self.db.refresh(db_task)

        return self._to_response(db_task)

    def list_tasks(self) -> list[TaskResponse]:
        db_tasks = self.db.query(Task).order_by(Task.id).all()
        return [self._to_response(task) for task in db_tasks]

    def get_task(self, task_id: int) -> TaskResponse:
        db_task = self.db.query(Task).filter(Task.id == task_id).first()

        if db_task is None:
            raise TaskNotFoundError(task_id)

        return self._to_response(db_task)

    def update_task(self, task_id: int, update_data: TaskUpdate) -> TaskResponse:
        db_task = self.db.query(Task).filter(Task.id == task_id).first()

        if db_task is None:
            raise TaskNotFoundError(task_id)

        if update_data.title is not None:
            db_task.title = update_data.title

        if update_data.description is not None:
            db_task.description = update_data.description

        if update_data.status is not None:
            db_task.status = update_data.status

        self.db.commit()
        self.db.refresh(db_task)

        return self._to_response(db_task)

    def delete_task(self, task_id: int) -> None:
        db_task = self.db.query(Task).filter(Task.id == task_id).first()

        if db_task is None:
            raise TaskNotFoundError(task_id)

        self.db.delete(db_task)
        self.db.commit()

    def _to_response(self, task: Task) -> TaskResponse:
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            status=task.status,
        )