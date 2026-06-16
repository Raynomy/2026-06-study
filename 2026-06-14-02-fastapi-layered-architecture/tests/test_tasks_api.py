from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_task():
    response = client.post( 
        "/tasks",
        json={
            "title": "学习 pytest",
            "description": "使用 TestClient 测试 FastAPI",
        },
    )

    assert response.status_code == 201

    data = response.json()
    assert isinstance(data["id"], int)
    assert data["id"] >= 1
    assert data["title"] == "学习 pytest"
    assert data["description"] == "使用 TestClient 测试 FastAPI"
    assert data["status"] == "todo"
#client.post(...) 是模拟请求接口
#json={...} 是请求体
#response.status_code 是状态码
#response.json() 是响应内容
#assert 是断言，判断结果是否符合预期

def test_list_tasks():
    client.post(
        "/tasks",
        json={
            "title": "学习查询任务",
            "description": "测试 GET /tasks",
        },
    )

    response = client.get("/tasks")

    assert response.status_code == 200

    data = response.json()
    assert len(data) >= 1
    assert data[-1]["title"] == "学习查询任务"
    assert data[-1]["description"] == "测试 GET /tasks"
    assert data[-1]["status"] == "todo"

def test_get_task_by_id():
    create_response = client.post(
        "/tasks",
        json={
            "title": "学习查询单个任务",
            "description": "测试 GET /tasks/{task_id}",
        },
    )

    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "学习查询单个任务"
    assert data["description"] == "测试 GET /tasks/{task_id}"
    assert data["status"] == "todo"

def test_update_task_status():
    create_response = client.post(
        "/tasks",
        json={
            "title": "学习更新任务",
            "description": "测试 PATCH /tasks/{task_id}",
        },
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "status": "doing",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "学习更新任务"
    assert data["description"] == "测试 PATCH /tasks/{task_id}"
    assert data["status"] == "doing"

def test_delete_task():
    create_response = client.post(
        "/tasks",
        json={
            "title": "学习删除任务",
            "description": "测试 DELETE /tasks/{task_id}",
        },
    )

    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/tasks/{task_id}")

    assert get_response.status_code == 404
    assert get_response.json() == {
        "code": "TASK_NOT_FOUND",
        "message": f"Task {task_id} not found",
    }

def test_get_missing_task_returns_404():
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "code": "TASK_NOT_FOUND",
        "message": "Task 999 not found",
    }

def test_get_task_with_invalid_id_returns_422():
    response = client.get("/tasks/0")

    assert response.status_code == 422

def test_create_task_with_empty_title_returns_422():
    response = client.post(
        "/tasks",
        json={
            "title": "",
            "description": "标题为空应该校验失败",
        },
    )

    assert response.status_code == 422

def test_update_task_with_invalid_status_returns_422():
    create_response = client.post(
        "/tasks",
        json={
            "title": "学习非法状态校验",
            "description": "测试 Literal 状态限制",
        },
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={
            "status": "invalid",
        },
    )

    assert response.status_code == 422

'''
GET /health
健康检查接口

POST /tasks
创建任务成功

GET /tasks
查询任务列表成功

GET /tasks/{task_id}
查询单个任务成功

PATCH /tasks/{task_id}
更新任务成功

DELETE /tasks/{task_id}
删除任务成功

GET /tasks/999
任务不存在，返回 404

GET /tasks/0
路径参数不合法，返回 422

POST /tasks title=""
请求体校验失败，返回 422

PATCH /tasks/{task_id} status="invalid"
状态字段校验失败，返回 422
'''