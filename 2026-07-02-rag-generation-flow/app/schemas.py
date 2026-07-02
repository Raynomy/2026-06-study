from pydantic import BaseModel, Field


class DocumentUploadRequest(BaseModel):
    filename: str = Field(min_length=1, max_length=200)
    content: str = Field(min_length=1)


class DocumentUploadResponse(BaseModel):
    filename: str
    chunk_count: int


class DocumentSearchRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class SearchResult(BaseModel):
    chunk_id: str
    text: str
    source: str
    paragraph: int
    score: float


class DocumentSearchResponse(BaseModel):
    query: str
    results: list[SearchResult]

class DocumentAnswerRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)


class AnswerSource(BaseModel):
    chunk_id: str
    source: str
    paragraph: int
    score: float
    text: str


class DocumentAnswerResponse(BaseModel):
    question: str
    answer: str
    sources: list[AnswerSource]