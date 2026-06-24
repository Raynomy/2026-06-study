from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(min_length=1, max_length=100)
    question: str = Field(min_length=1, max_length=1000)


class ChatResponse(BaseModel):
    session_id: str
    answer: str