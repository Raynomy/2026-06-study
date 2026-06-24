import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, StreamingResponse

from app.exceptions import LLMServiceError
from app.logging_config import setup_logging
from app.schemas import ChatRequest, ChatResponse
from app.services import chat_with_llm, chat_with_llm_stream

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(LLMServiceError)
def handle_llm_service_error(request: Request, exc: LLMServiceError):
    logger.error(
        "LLMServiceError path=%s code=%s message=%s",
        request.url.path,
        exc.code,
        exc.message,
    )

    return JSONResponse(
        status_code=503,
        content={
            "code": exc.code,
            "message": exc.message,
        },
    )


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    duration = time.perf_counter() - start_time

    logger.info(
        "%s %s %s %.4fs",
        request.method,
        request.url.path,
        response.status_code,
        duration,
    )

    return response


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