'''
from fastapi import FastAPI

from app.schemas import TaskCreate, TaskResponse
#导入 FastAPI
#导入请求体模型和响应模型

app = FastAPI() #创建 FastAPI 应用


@app.get("/health") #注册 GET /health 路由
def health_check() -> dict[str, str]: #处理这个请求的函数
    return {"status": "ok"} #返回 JSON 响应

#这个 /health 接口的目的不是做业务功能，而是做健康检查。
#它的作用是回答一个问题：这个后端服务现在是不是正常跑着？
#FastAPI 应用能启动、uvicorn 服务器能运行、路由注册成功、浏览器/客户端能访问服务器、服务器能返回 JSON


@app.post("/tasks", response_model=TaskResponse)# FastAPI 的路由装饰器：把下面这个 Python 函数注册成一个 API 接口。
def create_task(task: TaskCreate) -> TaskResponse:
    return TaskResponse(
        id=1,
        title=task.title,
        description=task.description,
        status="todo",
    )
#当客户端发送 POST /tasks 请求时，FastAPI 就执行 create_task 这个函数。
#你写 main.py 定义 API；
#uvicorn 启动服务器；
#服务器监听 127.0.0.1:8000；
#@app.get("/health") 定义路径；
#所以浏览器可以访问 http://127.0.0.1:8000/health。

'''

from fastapi import FastAPI, HTTPException, status

from app.schemas import TaskCreate, TaskResponse, TaskUpdate


app = FastAPI()


tasks: dict[int, TaskResponse] = {}
next_task_id = 1


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


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