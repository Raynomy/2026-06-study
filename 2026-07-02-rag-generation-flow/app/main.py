from fastapi import FastAPI

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

app = FastAPI(title="RAG Document API")


@app.get("/health")
def health_check():
    return {"status": "ok"}


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

@app.post("/documents/answer", response_model=DocumentAnswerResponse)
def answer_document(request: DocumentAnswerRequest):
    return answer_with_context(
        question=request.question,
        top_k=request.top_k,
    )