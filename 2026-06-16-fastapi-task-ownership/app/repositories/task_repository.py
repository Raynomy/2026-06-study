from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, task: TaskCreate, owner_id: int) -> Task:
        db_task = Task(
            title=task.title,
            description=task.description,
            status="todo",
            owner_id=owner_id,
        )

        self.db.add(db_task) #把对象加入数据库会话，可以理解为加入购物车
        self.db.commit() #真正提交到数据库，可以理解为：付款下单
        self.db.refresh(db_task) #从数据库重新读取这条数据，更新 db_task 这个 Python 对象

        return db_task

    def list_by_owner(self, owner_id: int) -> list[Task]:
        return (
            self.db.query(Task)
            .filter(Task.owner_id == owner_id)
            .order_by(Task.id)
            .all()
        ) #这段是 SQLAlchemy 的链式查询写法：

    def get_by_id_and_owner(self, task_id: int, owner_id: int) -> Task | None:
        return (
            self.db.query(Task)
            .filter(Task.id == task_id, Task.owner_id == owner_id)
            .first() #task_id 是唯一的，最多只会有一个任务
        )

    def update(self, db_task: Task, update_data: TaskUpdate) -> Task:
        if update_data.title is not None:
            db_task.title = update_data.title

        if update_data.description is not None:
            db_task.description = update_data.description

        if update_data.status is not None:
            db_task.status = update_data.status

        self.db.commit()
        self.db.refresh(db_task)

        return db_task

    def delete(self, db_task: Task) -> None:
        self.db.delete(db_task)
        self.db.commit()