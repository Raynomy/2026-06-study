from app.services.task_service import TaskService


task_service = TaskService()


def get_task_service() -> TaskService: #  依赖函数
    return task_service

#不这么写：每个接口 service = TaskService()，重复创建对象，冗余难维护；
#实例只创建一次，靠依赖函数统一分发，符合分层、复用的开发规范。