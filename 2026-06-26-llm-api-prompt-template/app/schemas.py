from typing import Literal

from pydantic import BaseModel, Field


TaskType = Literal["classification", "extraction", "summary"]


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1)
    question: str = Field(min_length=1)


class ChatResponse(BaseModel):
    session_id: str
    answer: str


class TemplateChatRequest(BaseModel):
    task_type: TaskType
    input_text: str = Field(min_length=1)


class ClassificationResult(BaseModel):
    category: Literal["技术学习", "生活记录", "求职准备", "其他"]
    reason: str


class ExtractionResult(BaseModel):
    task_name: str | None
    deadline: str | None
    priority: Literal["高", "中", "低"] | None


class SummaryResult(BaseModel):
    summary: str
    key_points: list[str]


class TemplateChatResponse(BaseModel):
    task_type: TaskType
    result: ClassificationResult | ExtractionResult | SummaryResult