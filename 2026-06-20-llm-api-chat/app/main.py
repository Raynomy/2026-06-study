from fastapi import FastAPI

from app.schemas import ChatRequest, ChatResponse
from app.services import chat_with_llm


app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    answer = chat_with_llm(
        session_id=request.session_id,
        question=request.question,
    )

    return ChatResponse(
        session_id=request.session_id,
        answer=answer,
    )