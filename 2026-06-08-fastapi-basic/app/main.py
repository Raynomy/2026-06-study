from fastapi import FastAPI, HTTPException, status
#FastAPI：用来创建 app 应用对象
#HTTPException：用来主动返回 HTTP 错误，比如任务不存在时返回 404。
#status：用来写状态码常量，比如 201、404、204
from app.schemas import TaskCreate, TaskResponse, TaskUpdate


app = FastAPI()
#这句创建一个 FastAPI 应用对象。
#运行：../.venv/bin/python -m uvicorn app.main:app --port 8000 里面最后的 app，指的就是这里


tasks: dict[int, TaskResponse] = {}
next_task_id = 1
#临时数据存储


#健康检查接口，它不是业务接口，主要用来确认：服务能启动、路由能访问、服务器能返回 JSON
@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
#FastAPI 应用对象app自带的方法.get()
#FastAPI 类 -> 创建 app 对象 -> app 对象有 get/post/put/delete 等方法 -> 用这些方法注册接口


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task: TaskCreate) -> TaskResponse:
    global next_task_id

    new_task = TaskResponse(
        id=next_task_id,
        title=task.title,
        description=task.description,
        status="todo",
    )

    tasks[next_task_id] = new_task
    next_task_id += 1

    return new_task


@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks() -> list[TaskResponse]:
    return list(tasks.values())


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int) -> TaskResponse:
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    return tasks[task_id]


@app.patch("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, update_data: TaskUpdate) -> TaskResponse:
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    task = tasks[task_id]

    updated_task = TaskResponse(
        id=task.id,
        title=update_data.title if update_data.title is not None else task.title,
        description=(
            update_data.description
            if update_data.description is not None
            else task.description
        ),
        status=update_data.status if update_data.status is not None else task.status,
    )

    tasks[task_id] = updated_task

    return updated_task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> None:
    if task_id not in tasks:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )

    del tasks[task_id]