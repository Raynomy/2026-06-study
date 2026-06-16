from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db
 # 1. 把前端数据转为数据库模型对象
    def create(self, task: TaskCreate) -> Task:
        db_task = Task(
            title=task.title,
            description=task.description,
            status="todo",
        )
        # 2. 加入会话，准备写入
        self.db.add(db_task)
        # 3. 提交事务，真正存入数据库
        self.db.commit()
        # 4. 从数据库刷新数据（拿到自增id等）
        self.db.refresh(db_task)

        return db_task    # 5. 返回数据库对象给 Service

    def list(self) -> list[Task]:
        return self.db.query(Task).order_by(Task.id).all()

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

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