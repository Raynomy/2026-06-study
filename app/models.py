from typing import Literal, Optional

from pydantic import BaseModel, Field


TaskStatus = Literal["todo", "doing", "done"]
DocumentType = Literal["note", "pdf", "markdown", "web"]


class User(BaseModel):
    user_id: str = Field(min_length=1)
    name: str = Field(min_length=1, max_length=20)
    email: Optional[str] = None
    age: Optional[int] = Field(default=None, ge=0, le=150)


class Task(BaseModel):
    task_id: str = Field(min_length=1)
    title: str = Field(min_length=1, max_length=100)
    owner_id: str = Field(min_length=1)
    description: Optional[str] = Field(default=None, max_length=500)
    status: TaskStatus = "todo"


class Document(BaseModel):
    document_id: str = Field(min_length=1)
    title: str = Field(min_length=1, max_length=100)
    owner_id: str = Field(min_length=1)
    content: str = Field(min_length=1)
    document_type: DocumentType = "note"
    source: Optional[str] = None