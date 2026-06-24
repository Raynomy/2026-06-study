from fastapi import FastAPI
from fastapi.responses import StreamingResponse

from app.schemas import ChatRequest, ChatResponse
from app.services import chat_with_llm, chat_with_llm_stream

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

@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    return StreamingResponse(
        chat_with_llm_stream(
            session_id=request.session_id,
            question=request.question,
        ),
        media_type="text/plain",
    )
