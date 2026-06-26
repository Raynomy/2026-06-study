import json
import os
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
)

MODEL = os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash")


class ClassificationResult(BaseModel):
    category: Literal["技术学习", "生活记录", "求职准备", "其他"]
    reason: str


class TaskExtractionResult(BaseModel):
    task_name: str | None
    deadline: str | None
    priority: Literal["高", "中", "低"] | None


def ask_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是一个严格输出 JSON 的中文助手。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.1,
        max_tokens=500,
    )

    return response.choices[0].message.content or ""


classification_prompt = """
请判断下面文本属于哪一类，并输出 JSON。

可选类别：
- 技术学习
- 生活记录
- 求职准备
- 其他

要求：
1. 只输出 JSON
2. 不要输出 Markdown
3. 不要输出解释
4. category 必须是可选类别之一
5. reason 用一句话说明分类原因

JSON 格式：
{
  "category": "技术学习",
  "reason": "分类原因"
}

文本：
今天学习了 FastAPI 的依赖注入和 JWT 鉴权。
"""


classification_result = ask_llm(classification_prompt)

print("分类模型原始输出：")
print(classification_result)

classification_data = json.loads(classification_result)
classification = ClassificationResult.model_validate(classification_data)

print("Python 解析后的分类结果：")
print(classification_data)

print("Pydantic 校验后的分类结果：")
print(classification)

print("分类结果：")
print(classification.category)


extraction_prompt = """
请从下面文本中抽取任务信息，并输出 JSON。

要求：
1. 只输出 JSON
2. 不要输出 Markdown
3. 不要输出解释
4. 只能抽取原文明确出现的信息
5. 如果字段不存在，使用 null

JSON 格式：
{
  "task_name": "任务名称",
  "deadline": "截止时间",
  "priority": "优先级"
}

文本：
请在本周五之前完成 FastAPI 项目的 README 整理，优先级高。
"""


extraction_result = ask_llm(extraction_prompt)

print("信息抽取模型原始输出：")
print(extraction_result)

extraction_data = json.loads(extraction_result)
task = TaskExtractionResult.model_validate(extraction_data)

print("Python 解析后的信息抽取结果：")
print(extraction_data)

print("Pydantic 校验后的信息抽取结果：")
print(task)

print("任务名称：")
print(task.task_name)

print("截止时间：")
print(task.deadline)

print("优先级：")
print(task.priority)

bad_json_result = """
{
  "category": "技术学习",
  "reason": "缺少结尾大括号"
"""

print("错误 JSON 原始输出：")
print(bad_json_result)

try:
    bad_data = json.loads(bad_json_result)
except json.JSONDecodeError as exc:
    print("JSON 解析失败：")
    print(exc)