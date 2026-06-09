from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.routers.tasks import router as tasks_router
from app.services.task_service import TaskService
from app.exceptions import TaskNotFoundError
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

task_service = TaskService()

@app.exception_handler(TaskNotFoundError)
def task_not_found_handler(
    request: Request,
    exc: TaskNotFoundError,
) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "code": "TASK_NOT_FOUND",
            "message": str(exc),
        },
    )

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


def get_message() -> str:
    return "hello from dependency"


@app.get("/demo")
def demo(message: str = Depends(get_message)) -> dict[str, str]:
    return {"message": message}


app.include_router(tasks_router)