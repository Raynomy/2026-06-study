from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base

#写数据库表模型：以下是 SQLAlchemy 的数据库模型。
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="todo")


#schemas/task.py
#API 数据模型
#用于请求体和响应体
#职责：返回给客户端

#models/task.py
#数据库表模型
#用于数据库存储
#职责：保存到数据库表