from fastapi import FastAPI

from app.schemas import ChatRequest, ChatResponse
from app.services import ChatService


app = FastAPI(title="LLM API Chat")

chat_service = ChatService()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(data: ChatRequest):
    answer = chat_service.chat(data.question)
    return ChatResponse(answer=answer)