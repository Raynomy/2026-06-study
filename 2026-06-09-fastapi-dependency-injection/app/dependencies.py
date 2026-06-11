from app.services.task_service import TaskService


task_service = TaskService()


def get_task_service() -> TaskService:
    return task_service