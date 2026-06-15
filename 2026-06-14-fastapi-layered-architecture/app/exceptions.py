#定义自定义异常类，继承 Python 内置异常基类 Exception
class TaskNotFoundError(Exception):
    def __init__(self, task_id: int):
        self.task_id = task_id
        super().__init__(f"Task {task_id} not found")#调用父类 Exception 的构造方法，设置异常描述文本
        #在 TaskService 查询任务时，判断数据不存在就手动 raise：raise TaskNotFoundError(task_id)

        