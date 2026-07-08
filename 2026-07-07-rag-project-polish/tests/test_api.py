from fastapi.testclient import TestClient

from app.exceptions import RAGServiceError
from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_document_with_empty_filename_returns_422():
    response = client.post(
        "/documents/upload",
        json={
            "filename": "",
            "content": "FastAPI 可以结合 JWT 实现用户登录鉴权。",
        },
    )

    assert response.status_code == 422


def test_search_with_empty_query_returns_422():
    response = client.post(
        "/documents/search",
        json={
            "query": "",
            "top_k": 3,
        },
    )

    assert response.status_code == 422


def test_answer_with_empty_question_returns_422():
    response = client.post(
        "/documents/answer",
        json={
            "question": "",
            "top_k": 3,
        },
    )

    assert response.status_code == 422


def test_rag_service_error_returns_503():
    @app.get("/test-error")
    def test_error():
        raise RAGServiceError(
            code="TEST_RAG_ERROR",
            message="Test RAG error",
        )

    response = client.get("/test-error")

    assert response.status_code == 503
    assert response.json() == {
        "code": "TEST_RAG_ERROR",
        "message": "Test RAG error",
    }