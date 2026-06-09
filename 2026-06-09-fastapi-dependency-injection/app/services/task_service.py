from fastapi import HTTPException, status

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


class TaskService:
    def __init__(self):
        self.tasks: dict[int, TaskResponse] = {}
        self.next_task_id = 1

    def create_task(self, task: TaskCreate) -> TaskResponse:
        new_task = TaskResponse(
            id=self.next_task_id,
            title=task.title,
            description=task.description,
            status="todo",
        )

        self.tasks[self.next_task_id] = new_task
        self.next_task_id += 1

        return new_task

    def list_tasks(self) -> list[TaskResponse]:
        return list(self.tasks.values())

    def get_task(self, task_id: int) -> TaskResponse:
        if task_id not in self.tasks:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task {task_id} not found",
            )

        return self.tasks[task_id]

    def update_task(self, task_id: int, update_data: TaskUpdate) -> TaskResponse:
        task = self.get_task(task_id)

        updated_task = TaskResponse(
            id=task.id,
            title=update_data.title if update_data.title is not None else task.title,
            description=(
                update_data.description
                if update_data.description is not None
                else task.description
            ),
            status=update_data.status if update_data.status is not None else task.status,
        )

        self.tasks[task_id] = updated_task

        return updated_task

    def delete_task(self, task_id: int) -> None:
        self.get_task(task_id)
        del self.tasks[task_id]