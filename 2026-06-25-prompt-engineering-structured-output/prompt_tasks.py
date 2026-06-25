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
                "content": "你是一个严格遵守输出格式的中文助手。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_tokens=500,
    )

    print(response.choices[0].message.content)


qa_prompt = """
你是一个 Python 后端学习助手。

请回答用户问题。

要求：
1. 用中文回答
2. 控制在 3 句话以内
3. 不要扩展到无关内容

问题：
FastAPI 为什么适合写 API？
"""


classification_prompt = """
请判断下面文本属于哪一类。

可选类别：
- 技术学习
- 生活记录
- 求职准备
- 其他

要求：
1. 只输出一个类别
2. 不要解释

文本：
今天学习了 FastAPI 的依赖注入和 JWT 鉴权。
"""


extraction_prompt = """
请从下面文本中抽取任务信息。

要求：
1. 只抽取原文中明确出现的信息
2. 不要编造
3. 使用以下格式输出：
任务名称：
截止时间：
优先级：

文本：
请在本周五之前完成 FastAPI 项目的 README 整理，优先级高。
"""

bad_extraction_prompt = """
帮我看看下面这段话里有什么任务信息：

请在本周五之前完成 FastAPI 项目的 README 整理，优先级高。
"""


ask_llm("问答 Prompt", qa_prompt)
ask_llm("分类 Prompt", classification_prompt)
ask_llm("抽取 Prompt", extraction_prompt)
ask_llm("失败样例：约束不足的抽取 Prompt", bad_extraction_prompt)