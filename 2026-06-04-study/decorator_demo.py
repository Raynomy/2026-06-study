'''
日志装饰器
from functools import wraps

def log_call(func):
    @wraps(func)
    def wrapper(*args,**kwargs): #*args接收位置参数。**接收关键字参数。
        print(f'开始执行函数：{func.__name__}')
        print(f"位置参数：{args}")
        print(f"关键字参数：{kwargs}")

        result =func(*args,**kwargs)

        print(f"函数执行结束：{func.__name__}")
        print(f"返回值：{result}")

        return result

    return wrapper

@log_call
def create_task(title:str,status:str="todo")->dict:
    return {
        "title":title,
        "status":status,
    }

task=create_task("学习装饰器",status="doing")
print(task)


#@log_call
#def create_task(...):
#    ...
#这句等价于：
#def create_task(...):
#    ...
#create_task = log_call(create_task)
'''

'''
计时装饰器
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start_time=time.time() #返回当前时间戳，单位秒

        result=func(*args,**kwargs)

        end_time=time.time()
        cost=end_time-start_time

        print(f'函数{func.__name__}执行耗时：{cost:.4f}秒')

        return result
    
    return wrapper

@timer
def slow_creat_task(title:str,status:str='todo')->dict:
    time.sleep(1) #让程序暂停 1 秒。
    return {
        'title':title,
        'status':status,
    }

task2=slow_creat_task("学习计时装饰器",status='done')
print(task2)
#timer 先接收并包装了 slow_create_task，之后你调用 slow_create_task() 时，实际先执行的是 wrapper()，然后 wrapper() 里面再调用原来的 slow_create_task()。

'''
from functools import wraps
import time

def log_call(func):
    @wraps(func)
    def wrapper(*args,**kwargs): #*args接收位置参数。**接收关键字参数。
        print(f'开始执行函数：{func.__name__}')
        print(f"位置参数：{args}")
        print(f"关键字参数：{kwargs}")

        result =func(*args,**kwargs)

        print(f"函数执行结束：{func.__name__}")
        print(f"返回值：{result}")

        return result

    return wrapper

def timer(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        start_time=time.time() #返回当前时间戳，单位秒

        result=func(*args,**kwargs)

        end_time=time.time()
        cost=end_time-start_time

        print(f'函数{func.__name__}执行耗时：{cost:.4f}秒')

        return result
    
    return wrapper

tasks=[]

@log_call
@timer
def create_task(title:str,status:str='todo')->dict:
    time.sleep(0.5)

    task={
        "title":title,
        "status":status,
    }

    tasks.append(task)
    return task

@log_call
@timer
def list_tasks()->list[dict]:
    time.sleep(0.2)
    return tasks

@log_call
@timer
def update_task_status(index:int,status:str)->dict:
    time.sleep(0.3)
    task=tasks[index]
    task["status"]=status
    return task

create_task("学习装饰器",status='doing')
create_task("整理装饰器笔记")
update_task_status(1,"done")

all_tasks=list_tasks()
print(all_tasks)


