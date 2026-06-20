import os

from openai import OpenAI


class ChatService:
    def __init__(self):
        self.client = OpenAI(
            api_key=os.getenv("AIHUBMIX_API_KEY"),
            base_url=os.getenv("AIHUBMIX_BASE_URL"),
        )
        self.model = os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash")

    def chat(self, question: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个简洁清晰的 Python 后端学习助手。",
                },
                {
                    "role": "user",
                    "content": question,
                },
            ],
        )

        return response.choices[0].message.content