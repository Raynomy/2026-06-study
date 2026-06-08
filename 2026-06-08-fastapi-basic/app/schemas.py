from typing import Literal
from pydantic import BaseModel, Field
# Pydantic 数据模型。
# 请求模型和响应模型

TaskStatus = Literal["todo", "doing", "done"]

class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    description: str | None = None


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    description: str | None = None
    status: TaskStatus | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    status: str