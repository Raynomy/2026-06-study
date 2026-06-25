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
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
        max_tokens=500,
    )

    print(response.choices[0].message.content)


source_text = """
FastAPI 是一个现代 Python Web 框架，适合构建 API。
它支持自动生成文档、请求参数校验和异步处理。
"""


loose_prompt = f"""
帮我整理一下这段内容：

{source_text}
"""

markdown_prompt = f"""
你是一个严谨的技术文档整理助手。

任务：
将给定文本整理成 Markdown 笔记。

边界：
1. 只能使用原文中出现的信息
2. 不要补充原文没有的信息
3. 不要输出寒暄语
4. 不要输出额外说明

输出格式：
必须严格使用下面格式：

### 标题

#### 核心说明
- 要点1
- 要点2

#### 特性
- 特性1
- 特性2
- 特性3

原文：
{source_text}
"""

json_prompt = f"""
你是一个严格的数据抽取助手。

任务：
从给定文本中抽取信息，并输出 JSON。

边界：
1. 只能使用原文中出现的信息
2. 不要补充原文没有的信息
3. 不要输出解释
4. 不要输出 Markdown
5. 只输出 JSON 对象

输出格式：
{{
  "title": "主题标题",
  "summary": "一句话总结",
  "features": ["特性1", "特性2", "特性3"]
}}

原文：
{source_text}
"""


ask_llm("宽泛 Prompt", loose_prompt)
ask_llm("强约束 Markdown Prompt", markdown_prompt)
ask_llm("强约束 JSON Prompt", json_prompt)