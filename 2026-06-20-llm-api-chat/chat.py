import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
)

model = os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash")


def chat_once(question: str) -> str:
    response = client.chat.completions.create(
        model=model,
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


if __name__ == "__main__":
    answer = chat_once("请用一句话解释什么是 FastAPI。")
    print(answer)