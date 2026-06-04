'''
class SimpleContext:
    def __enter__(self):
        print("进入上下文")
        return self
    
    def __exit__(self,exc_type,exc_value,exc_traceback):
        print("退出上下文")

with SimpleContext() as ctx:
    print("执行任务")
'''
class FileManager:
    def __init__(self,file_path:str,mode:str,encoding:str='utf-8'):
        self.file_path=file_path
        self.mode=mode
        self.encoding=encoding
        self.file=None
    
    def __enter__(self):
        print(f"打开文文件：{self.file_path}")
        self.file=open(self.file_path,self.mode,encoding=self.encoding)
        return self.file
    
    def __exit__(self,exc_type,exc_value,traceback):
        print(f"关闭文件：{self.file_path}")

        if self.file:
            self.file.close()

class DatabaseConnection:
    def __init__(self,db_name:str):
        self.db_name=db_name
        self.connected=False
    
    def __enter__(self):
        print(f"链接数据库：{self.db_name}")
        self.connected=True
        return self
    
    def __exit__(self, exc_type, exc_value,traceback):
        print(f"关闭数据库连接：{self.db_name}")
        self.connected=False

    def query(self,sql:str)->list[dict]:
        if not self.connected:
            raise RuntimeError("数据库未连接")
        
        print(f"执行SQL：{sql}")
        return [
            {"id":1,"title":"学习context manager"},
            {"id":2,"title":"学习FastAPI"},
        ]

        
        
'''
with FileManager('demo.txt','w') as file:
    file.write('hello context manager')

with FileManager('demo.txt','r') as file:
    content=file.read()
    print(content)
'''
with DatabaseConnection("task_db") as db:
    result =db.query("select * from tasks")
    print(result)