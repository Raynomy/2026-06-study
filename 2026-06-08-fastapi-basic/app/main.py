from fastapi import FastAPI

from app.schemas import TaskCreate, TaskResponse


app = FastAPI()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate) -> TaskResponse:
    return TaskResponse(
        id=1,
        title=task.title,
        description=task.description,
        status="todo",
    )