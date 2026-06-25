import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
)

MODEL = os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash")


def ask_llm(title: str, prompt: str) -> None:
    print("=" * 60)
    print(title)
    print("-" * 60)

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个严谨、清晰的中文学习助手。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
        max_tokens=500,
    )

    print(response.choices[0].message.content)


task_text = """
FastAPI 是一个用于构建 API 的现代 Python Web 框架。
它基于 Starlette 和 Pydantic，支持异步、自动文档和数据校验。
"""


zero_shot_prompt = f"""
总结下面这段话：

{task_text}
"""


instruction_prompt = f"""
请总结下面这段话。

要求：
1. 只输出 3 个要点
2. 每个要点不超过 20 个字
3. 使用列表格式
4. 不要添加原文没有的信息

原文：
{task_text}
"""


few_shot_prompt = f"""
请把输入文本总结成 3 个简短要点。

要求：
1. 必须输出 3 条
2. 每条以 "- " 开头
3. 每条不超过 20 个字
4. 不要输出解释

示例：

输入：
Django 是一个 Python Web 框架，内置 ORM、后台管理和用户认证，适合快速开发完整网站。

输出：
- Python Web 框架
- 内置常用功能
- 适合完整网站

现在请处理下面文本：

输入：
{task_text}

输出：
"""


ask_llm("Zero-shot Prompt", zero_shot_prompt)
ask_llm("Instruction Prompt", instruction_prompt)
ask_llm("Few-shot Prompt", few_shot_prompt)