import os

from pydantic import BaseModel


class Settings(BaseModel):
    app_name: str = "Task API"
    app_version: str = "0.1.0"
    debug: bool = True
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./tasks.db")


settings = Settings()