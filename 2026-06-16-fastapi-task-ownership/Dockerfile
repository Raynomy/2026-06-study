FROM python:3.10-slim
#使用 Python 3.10 的轻量镜像作为基础环境
WORKDIR /app
#进入容器里的 /app 目录，之后命令都在这里执行
COPY requirements.txt .
#先复制依赖文件
RUN pip install --no-cache-dir -r requirements.txt
#安装 Python 依赖
COPY app ./app
#复制项目代码
EXPOSE 8000
#声明容器使用 8000 端口
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#容器启动时运行 FastAPI