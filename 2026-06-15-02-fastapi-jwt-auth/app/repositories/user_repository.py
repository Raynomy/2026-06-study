from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_username(self, username: str) -> User | None:
        return self.db.query(User).filter(User.username == username).first()

    def create(self, username: str, hashed_password: str) -> User:
        db_user = User(
            username=username,
            hashed_password=hashed_password,
            is_active=True,
        )

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user
    
#UserRepository 只负责数据库操作：
#按 username 查询用户
#创建用户
#add / commit / refresh
