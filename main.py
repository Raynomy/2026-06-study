from pydantic import ValidationError

from app.models import Document, Task, User


try:
    user = User(
        user_id="u1",
        name="小明",
        email="xiaoming@example.com",
        age=18,
    )

    task = Task(
        task_id="t1",
        title="学习 Pydantic",
        owner_id=user.user_id,
        status="doing",
    )

    document = Document(
        document_id="",
        title="",
        owner_id=user.user_id,
        content="",
        document_type="unkown",
    )

    print(user)
    print(task)
    print(document)

except ValidationError as e:
    print("数据校验失败")
    print(e)