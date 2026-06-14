from fastapi import APIRouter, Depends, Path, status

from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.task_service import TaskService
from app.dependencies import get_task_service

#把接口按业务模块拆分
router = APIRouter(prefix="/tasks", tags=["tasks"]) #RESTful API 设计

#prefix="/tasks"：路由前缀
#该路由下所有接口，路径都会自动拼接 /tasks。
#下文 @router.post("") 空路径，完整接口地址就是：POST /tasks。
#tags=["tasks"]：接口分组标签，作用于自动接口文档，方便分类查看。

#优势（为什么这么设计）
#拆分模块：用户、任务、订单等不同功能，各自创建独立 APIRouter，代码分开文件存放，项目结构清晰；
#统一管理：要改公共前缀（比如从 /tasks 改成 /api/tasks），只改 prefix 一处即可，不用逐个修改接口；
#符合 RESTful 资源分组思路：同一类资源（任务）集中在同一个路由下。

# 1. 路由装饰器
@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED) #RESTful API 设计 # 2. 接口函数定义
def create_task(
    task: TaskCreate, # ← 这里 = 接收请求体
    service: TaskService = Depends(get_task_service),
) -> TaskResponse: #3. 业务逻辑
    return service.create_task(task)


@router.get("", response_model=list[TaskResponse]) #RESTful API 设计
def list_tasks(
    service: TaskService = Depends(get_task_service),
) -> list[TaskResponse]:
    return service.list_tasks()



@router.get("/{task_id}", response_model=TaskResponse) #RESTful API 设计
def get_task(
    task_id: int = Path(ge=1),
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    return service.get_task(task_id)


@router.patch("/{task_id}", response_model=TaskResponse) #RESTful API 设计
def update_task(
    update_data: TaskUpdate,
    task_id: int = Path(ge=1),
    service: TaskService = Depends(get_task_service),
) -> TaskResponse:
    return service.update_task(task_id, update_data)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT) #RESTful API 设计
def delete_task(
    task_id: int = Path(ge=1),
    service: TaskService = Depends(get_task_service),
) -> None:
    service.delete_task(task_id)