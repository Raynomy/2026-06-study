from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def get_auth_headers() -> dict[str, str]:
    username = f"auth_{uuid4().hex[:12]}"
    password = "123456"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}

def create_auth_headers_for(username_prefix: str) -> dict[str, str]:
    username = f"{username_prefix}_{uuid4().hex[:12]}"
    password = "123456"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )
    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task():
    headers = get_auth_headers()

    response = client.post(
        "/tasks",
        json={
            "title": "学习 pytest",
            "description": "使用 TestClient 测试 FastAPI",
        },
        headers=headers,
    )

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["id"] >= 1
    assert data["title"] == "学习 pytest"
    assert data["description"] == "使用 TestClient 测试 FastAPI"
    assert data["status"] == "todo"


def test_list_tasks():
    headers = get_auth_headers()

    client.post(
        "/tasks",
        json={
            "title": "学习查询任务",
            "description": "测试 GET /tasks",
        },
        headers=headers,
    )

    response = client.get("/tasks", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 1
    assert data[-1]["title"] == "学习查询任务"
    assert data[-1]["description"] == "测试 GET /tasks"
    assert data[-1]["status"] == "todo"


def test_get_task_by_id():
    headers = get_auth_headers()

    create_response = client.post(
        "/tasks",
        json={
            "title": "学习查询单个任务",
            "description": "测试 GET /tasks/{task_id}",
        },
        headers=headers,
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}", headers=headers)

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "学习查询单个任务"
    assert data["description"] == "测试 GET /tasks/{task_id}"
    assert data["status"] == "todo"


def test_update_task_status():
    headers = get_auth_headers()

    create_response = client.post(
        "/tasks",
        json={
            "title": "学习更新任务",
            "description": "测试 PATCH /tasks/{task_id}",
        },
        headers=headers,
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "status": "doing",
        },
        headers=headers,
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "学习更新任务"
    assert data["description"] == "测试 PATCH /tasks/{task_id}"
    assert data["status"] == "doing"


def test_delete_task():
    headers = get_auth_headers()

    create_response = client.post(
        "/tasks",
        json={
            "title": "学习删除任务",
            "description": "测试 DELETE /tasks/{task_id}",
        },
        headers=headers,
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}", headers=headers)

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/tasks/{task_id}", headers=headers)

    assert get_response.status_code == 404
    assert get_response.json() == {
        "code": "TASK_NOT_FOUND",
        "message": f"Task {task_id} not found",
    }


def test_get_missing_task_returns_404():
    headers = get_auth_headers()

    response = client.get("/tasks/999", headers=headers)

    assert response.status_code == 404
    assert response.json() == {
        "code": "TASK_NOT_FOUND",
        "message": "Task 999 not found",
    }


def test_get_task_with_invalid_id_returns_422():
    headers = get_auth_headers()

    response = client.get("/tasks/0", headers=headers)

    assert response.status_code == 422


def test_create_task_with_empty_title_returns_422():
    headers = get_auth_headers()

    response = client.post(
        "/tasks",
        json={
            "title": "",
            "description": "标题为空应该校验失败",
        },
        headers=headers,
    )

    assert response.status_code == 422


def test_update_task_with_invalid_status_returns_422():
    headers = get_auth_headers()

    create_response = client.post(
        "/tasks",
        json={
            "title": "学习非法状态校验",
            "description": "测试 Literal 状态限制",
        },
        headers=headers,
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "status": "invalid",
        },
        headers=headers,
    )

    assert response.status_code == 422


def test_register_user():
    username = f"reg_{uuid4().hex[:12]}"

    response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "123456",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["username"] == username
    assert data["is_active"] is True
    assert "password" not in data
    assert "hashed_password" not in data


def test_register_duplicate_user_returns_409():
    username = f"dup_{uuid4().hex[:12]}"
    payload = {
        "username": username,
        "password": "123456",
    }

    first_response = client.post("/auth/register", json=payload)
    assert first_response.status_code == 201

    second_response = client.post("/auth/register", json=payload)

    assert second_response.status_code == 409
    assert second_response.json() == {
        "code": "USER_ALREADY_EXISTS",
        "message": f"User {username} already exists",
    }


def test_login_user_success():
    username = f"login_{uuid4().hex[:12]}"
    password = "123456"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    data = login_response.json()
    assert isinstance(data["access_token"], str)
    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_user_with_wrong_password_returns_401():
    username = f"wrong_{uuid4().hex[:12]}"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "password": "123456",
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "wrong-password",
        },
    )

    assert login_response.status_code == 401
    assert login_response.json() == {
        "code": "INVALID_CREDENTIALS",
        "message": "Invalid username or password",
    }


def test_login_missing_user_returns_401():
    username = f"missing_{uuid4().hex[:12]}"

    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "123456",
        },
    )

    assert response.status_code == 401
    assert response.json() == {
        "code": "INVALID_CREDENTIALS",
        "message": "Invalid username or password",
    }

def test_user_cannot_see_other_users_tasks_in_list():
    alice_headers = create_auth_headers_for("alice")
    bob_headers = create_auth_headers_for("bob")

    create_response = client.post(
        "/tasks",
        json={
            "title": "Alice 的私有任务",
            "description": "Bob 不应该在列表中看到",
        },
        headers=alice_headers,
    )
    assert create_response.status_code == 201

    response = client.get("/tasks", headers=bob_headers)

    assert response.status_code == 200

    data = response.json()
    titles = [task["title"] for task in data]

    assert "Alice 的私有任务" not in titles

def test_user_cannot_get_other_users_task_by_id():
    alice_headers = create_auth_headers_for("alice")
    bob_headers = create_auth_headers_for("bob")

    create_response = client.post(
        "/tasks",
        json={
            "title": "Alice 的单个私有任务",
            "description": "Bob 用 id 查询也应该失败",
        },
        headers=alice_headers,
    )
    assert create_response.status_code == 201

    alice_task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{alice_task_id}", headers=bob_headers)

    assert response.status_code == 404
    assert response.json() == {
        "code": "TASK_NOT_FOUND",
        "message": f"Task {alice_task_id} not found",
    }

def test_user_cannot_update_other_users_task():
    alice_headers = create_auth_headers_for("alice")
    bob_headers = create_auth_headers_for("bob")

    create_response = client.post(
        "/tasks",
        json={
            "title": "Alice 的待更新任务",
            "description": "Bob 不应该能更新",
        },
        headers=alice_headers,
    )
    assert create_response.status_code == 201

    alice_task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{alice_task_id}",
        json={
            "status": "doing",
        },
        headers=bob_headers,
    )

    assert response.status_code == 404
    assert response.json() == {
        "code": "TASK_NOT_FOUND",
        "message": f"Task {alice_task_id} not found",
    }

    alice_get_response = client.get(f"/tasks/{alice_task_id}", headers=alice_headers)

    assert alice_get_response.status_code == 200
    assert alice_get_response.json()["status"] == "todo"

def test_user_cannot_delete_other_users_task():
    alice_headers = create_auth_headers_for("alice")
    bob_headers = create_auth_headers_for("bob")

    create_response = client.post(
        "/tasks",
        json={
            "title": "Alice 的待删除任务",
            "description": "Bob 不应该能删除",
        },
        headers=alice_headers,
    )
    assert create_response.status_code == 201

    alice_task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{alice_task_id}", headers=bob_headers)

    assert response.status_code == 404
    assert response.json() == {
        "code": "TASK_NOT_FOUND",
        "message": f"Task {alice_task_id} not found",
    }

    alice_get_response = client.get(f"/tasks/{alice_task_id}", headers=alice_headers)

    assert alice_get_response.status_code == 200
    assert alice_get_response.json()["id"] == alice_task_id