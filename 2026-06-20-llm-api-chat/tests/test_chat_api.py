from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_request_missing_session_id_returns_422():
    response = client.post(
        "/chat",
        json={
            "question": "请解释 FastAPI",
        },
    )

    assert response.status_code == 422


def test_chat_request_missing_question_returns_422():
    response = client.post(
        "/chat",
        json={
            "session_id": "test-session",
        },
    )

    assert response.status_code == 422


def test_chat_request_empty_question_returns_422():
    response = client.post(
        "/chat",
        json={
            "session_id": "test-session",
            "question": "",
        },
    )

    assert response.status_code == 422


def test_stream_request_missing_question_returns_422():
    response = client.post(
        "/chat/stream",
        json={
            "session_id": "test-session",
        },
    )

    assert response.status_code == 422