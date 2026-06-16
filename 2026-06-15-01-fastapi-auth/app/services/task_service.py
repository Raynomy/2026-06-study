from app.exceptions import TaskNotFoundError
from app.models.task import Task
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


#数据库版：数据写到 SQLite 数据库
#分层架构版：TaskService 不直接写数据库，而是调用 TaskRepository 写数据库

class TaskService:
    def __init__(self, repository: TaskRepository):
        self.repository = repository

    def create_task(self, task: TaskCreate) -> TaskResponse:
        db_task = self.repository.create(task)
        return self._to_response(db_task)

    def list_tasks(self) -> list[TaskResponse]:
        db_tasks = self.repository.list()
        return [self._to_response(task) for task in db_tasks]

    def get_task(self, task_id: int) -> TaskResponse:
        db_task = self.repository.get_by_id(task_id)

        if db_task is None:
            raise TaskNotFoundError(task_id)

        return self._to_response(db_task)

    def update_task(self, task_id: int, update_data: TaskUpdate) -> TaskResponse:
        db_task = self.repository.get_by_id(task_id)

        if db_task is None:
            raise TaskNotFoundError(task_id)

        updated_task = self.repository.update(db_task, update_data)

        return self._to_response(updated_task)

    def delete_task(self, task_id: int) -> None:
        db_task = self.repository.get_by_id(task_id)

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
    
#self.db.query(...)
#self.db.add(...)
#self.db.commit()
#self.db.delete(...)
#变成
#self.repository.create(...)
#self.repository.list()
#self.repository.get_by_id(...)
#self.repository.update(...)
#self.repository.delete(...)
#此时
#TaskService负责业务规则：
    #- 任务不存在时抛 TaskNotFoundError
    #- 把数据库模型转换成响应模型
#TaskRepository负责数据库操作：
    #- query
    #- add
    #- commit
    #- delete