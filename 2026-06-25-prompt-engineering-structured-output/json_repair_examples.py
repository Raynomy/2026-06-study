import json
import os
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
)

MODEL = os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash")


bad_json_result = """
{
  "category": "技术学习",
  "reason": "缺少结尾大括号"
"""


def repair_json_with_llm(bad_json: str) -> str:
    prompt = f"""
你是一个严格的 JSON 修复助手。

任务：
修复下面这段不合法 JSON，使它变成合法 JSON。

要求：
1. 只输出修复后的 JSON
2. 不要输出 Markdown
3. 不要输出解释
4. 不要添加原文没有的信息
5. 字段名保持不变

不合法 JSON：
{bad_json}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
    )

    return response.choices[0].message.content or ""


def parse_or_repair_json(json_text: str, max_retries: int = 2) -> dict[str, Any]:
    current_text = json_text

    for attempt in range(max_retries + 1):
        try:
            return json.loads(current_text)
        except json.JSONDecodeError as exc:
            print(f"第 {attempt + 1} 次 JSON 解析失败：")
            print(exc)

            if attempt == max_retries:
                raise

            current_text = repair_json_with_llm(current_text)

            print("模型修复后的 JSON：")
            print(current_text)

    raise ValueError("JSON 解析失败")


print("错误 JSON 原始输出：")
print(bad_json_result)

data = parse_or_repair_json(bad_json_result)

print("最终解析结果：")
print(data)