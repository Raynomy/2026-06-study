import logging
import time

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.routers.tasks import router as tasks_router
from app.exceptions import TaskNotFoundError
from app.config import settings


from app.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    cost = time.perf_counter() - start_time

    logger.info(
        "%s %s %s %.4fs",
        request.method,
        request.url.path,
        response.status_code,
        cost,
    )

    return response

@app.exception_handler(TaskNotFoundError)
def task_not_found_handler(
    request: Request,
    exc: TaskNotFoundError,
) -> JSONResponse:
    logger.error(
        "TaskNotFoundError path=%s message=%s",
        request.url.path,
        str(exc),
    )

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