from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

#create_engine：属于 sqlalchemy 主模块，作用是创建数据库引擎。
#sessionmaker：属于 sqlalchemy.orm 子模块，作用是生成会话工厂。

DATABASE_URL = "sqlite:///./tasks.db"
#使用 SQLite
#数据库文件叫 tasks.db
#位置在你启动服务的当前目录


class Base(DeclarativeBase):
    pass
#Base 是所有数据库模型的基类。

engine = create_engine( #engine 是数据库连接入口。
    DATABASE_URL,
    connect_args={"check_same_thread": False}, #这是 SQLite + FastAPI 常见配置，允许 FastAPI 在不同请求处理中使用 SQLite 连接
)

SessionLocal = sessionmaker( #这是创建数据库会话的工厂。以后每次请求需要数据库时，就创建一个 session。
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db(): #这是 FastAPI 依赖注入函数。以后接口或 service 可以通过：db = Depends(get_db)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()