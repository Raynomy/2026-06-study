import logging
import time

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.routers.tasks import router as tasks_router
from app.exceptions import TaskNotFoundError
from app.config import settings


from app.logging_config import setup_logging
from app.database import Base, engine
from app.models import task

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
)

Base.metadata.create_all(bind=engine)
#根据所有继承 Base 的模型
#在 engine 连接的数据库里创建表


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

#配置、日志、路由、异常、通用拦截 全部分层解耦
#接口按业务模块拆分（tasks 独立路由）
#通用逻辑（日志、异常）全局统一处理，接口只专注业务