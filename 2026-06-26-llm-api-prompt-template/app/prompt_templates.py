def build_classification_prompt(input_text: str) -> str:
    return f"""
你是一个严格的文本分类助手。

任务：
请将下面文本分类到以下类别之一。

可选类别：
- 技术学习
- 生活记录
- 求职准备
- 其他

类别定义：
- 技术学习：学习编程、后端、AI、工具、框架等技术内容
- 生活记录：用户自己的生活经历、行为、感受或日常安排
- 求职准备：简历、面试、实习、求职、职业规划相关内容
- 其他：无法归入以上三类的内容

要求：
1. 只输出合法 JSON
2. 不要输出 Markdown
3. 不要输出解释文字
4. 字段必须包含 category 和 reason

输出格式：
{{
  "category": "技术学习 | 生活记录 | 求职准备 | 其他",
  "reason": "简要说明分类原因"
}}

文本：
{input_text}
"""


def build_extraction_prompt(input_text: str) -> str:
    return f"""
你是一个严格的信息抽取助手。

任务：
请从下面文本中抽取任务信息。

要求：
1. 只输出合法 JSON
2. 不要输出 Markdown
3. 不要输出解释文字
4. 不要编造原文没有的信息
5. 缺失字段填 null

输出格式：
{{
  "task_name": "任务名称或 null",
  "deadline": "截止时间或 null",
  "priority": "高 | 中 | 低 | null"
}}

文本：
{input_text}
"""


def build_summary_prompt(input_text: str) -> str:
    return f"""
你是一个简洁的中文总结助手。

任务：
请总结下面文本。

要求：
1. 只输出合法 JSON
2. 不要输出 Markdown
3. 不要输出解释文字
4. summary 控制在 50 字以内
5. key_points 输出 3 个要点

输出格式：
{{
  "summary": "一句话总结",
  "key_points": ["要点1", "要点2", "要点3"]
}}

文本：
{input_text}
"""