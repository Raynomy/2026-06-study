import os

from openai import OpenAI


client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
)

model = os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash")

question = "请用三句话介绍 FastAPI 的优点。"


def ask(temperature: float, top_p: float, max_tokens: int) -> str:
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
        temperature=temperature,
        top_p=top_p,
        max_tokens=max_tokens,
    )

    return response.choices[0].message.content


experiments = [
    {"temperature": 0.1, "top_p": 1.0, "max_tokens": 120},
    {"temperature": 0.7, "top_p": 1.0, "max_tokens": 120},
    {"temperature": 1.2, "top_p": 1.0, "max_tokens": 120},
    {"temperature": 0.7, "top_p": 0.5, "max_tokens": 120},
    {"temperature": 0.7, "top_p": 1.0, "max_tokens": 40},
]


for index, params in enumerate(experiments, start=1):
    print("=" * 60)
    print(f"实验 {index}: {params}")
    print(ask(**params))