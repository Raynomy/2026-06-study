import logging
import time

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions import RAGServiceError
from app.logging_config import setup_logging
from app.rag_service import answer_with_context
from app.schemas import (
    DocumentAnswerRequest,
    DocumentAnswerResponse,
    DocumentSearchRequest,
    DocumentSearchResponse,
    DocumentUploadRequest,
    DocumentUploadResponse,
)
from app.text_splitter import split_text
from app.vector_store import add_chunks, init_collection, search_chunks

setup_logging()

logger = logging.getLogger(__name__)

app = FastAPI(title="RAG Document API")
# 当前项目保留三个核心 RAG 接口：
# 1. /documents/upload：上传文档，切分 chunk，写入向量库
# 2. /documents/search：只做向量检索，返回相关 chunks
# 3. /documents/answer：检索相关 chunks，并基于资料生成回答


@app.exception_handler(RAGServiceError)
def handle_rag_service_error(request: Request, exc: RAGServiceError):
    logger.error(
        "RAGServiceError path=%s code=%s message=%s",
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

# 上传文档：原始文本 -> chunks -> embeddings -> Qdrant
@app.post("/documents/upload", response_model=DocumentUploadResponse)
def upload_document(request: DocumentUploadRequest):
    chunks = split_text(request.content)
    chunk_count = add_chunks(
        filename=request.filename,
        chunks=chunks,
    )

    return DocumentUploadResponse(
        filename=request.filename,
        chunk_count=chunk_count,
    )

# 检索文档：query -> embedding -> top-k chunks
@app.post("/documents/search", response_model=DocumentSearchResponse)
def search_documents(request: DocumentSearchRequest):
    results = search_chunks(
        query=request.query,
        top_k=request.top_k,
    )

    return DocumentSearchResponse(
        query=request.query,
        results=results,
    )
# 生成回答：query -> retrieve context -> LLM answer + sources
@app.post("/documents/answer", response_model=DocumentAnswerResponse)
def answer_document(request: DocumentAnswerRequest):
    return answer_with_context(
        question=request.question,
        top_k=request.top_k,
    )