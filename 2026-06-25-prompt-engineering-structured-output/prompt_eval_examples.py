import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
)

MODEL = os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash")

ALLOWED_CATEGORIES = ["技术学习", "生活记录", "求职准备", "其他"]

TEST_CASES = [
    {
        "text": "今天学习了 FastAPI 的依赖注入和 JWT 鉴权。",
        "expected_category": "技术学习",
    },
    {
        "text": "下午去健身房跑步 30 分钟，感觉状态不错。",
        "expected_category": "生活记录",
    },
    {
        "text": "我需要整理简历，并准备下周的后端实习面试。",
        "expected_category": "求职准备",
    },
    {
        "text": "周末可能会下雨，出门记得带伞。",
        "expected_category": "其他",
    },
]


def classify_with_basic_prompt(text: str) -> str:
    prompt = f"""
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
{text}
"""

    return ask_llm(prompt)


def classify_with_strict_prompt(text: str) -> str:
    prompt = f"""
你是一个严格的文本分类助手。

请判断下面文本属于哪一类。

类别定义：
- 技术学习：学习编程、后端、AI、工具、框架等技术内容
- 生活记录：用户自己的生活经历、行为、感受或日常安排
- 求职准备：简历、面试、实习、求职、职业规划相关内容
- 其他：无法归入以上三类的内容，包括天气提醒、普通提醒、客观信息、泛泛建议

要求：
1. 只输出一个类别
2. 不要解释
3. 必须从可选类别中选择
4. 不要因为文本是日常语言就自动归为生活记录

文本：
{text}
"""

    return ask_llm(prompt)


def ask_llm(prompt: str) -> str:
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

    return (response.choices[0].message.content or "").strip()


def evaluate(prompt_name: str, classify_func) -> None:
    correct_count = 0
    format_correct_count = 0

    print("=" * 60)
    print(prompt_name)
    print("=" * 60)

    for index, case in enumerate(TEST_CASES, start=1):
        actual_category = classify_func(case["text"])
        expected_category = case["expected_category"]

        is_format_correct = actual_category in ALLOWED_CATEGORIES
        is_correct = actual_category == expected_category

        if is_format_correct:
            format_correct_count += 1

        if is_correct:
            correct_count += 1

        if not is_format_correct:
            failure_reason = "格式错误：输出不在允许类别中"
        elif not is_correct:
            failure_reason = "分类错误：格式正确，但类别判断错误"
        else:
            failure_reason = "无"

        print(f"测试样例 {index}")
        print(f"输入：{case['text']}")
        print(f"预期分类：{expected_category}")
        print(f"模型输出：{actual_category}")
        print(f"格式正确：{is_format_correct}")
        print(f"分类正确：{is_correct}")
        print(f"失败原因：{failure_reason}")
        print("-" * 60)

    total_count = len(TEST_CASES)
    accuracy = correct_count / total_count
    format_accuracy = format_correct_count / total_count

    print("评测总结")
    print(f"总样例数：{total_count}")
    print(f"分类准确率：{accuracy:.2%}")
    print(f"格式正确率：{format_accuracy:.2%}")
    print()


evaluate("基础 Prompt", classify_with_basic_prompt)
evaluate("强约束 Prompt", classify_with_strict_prompt)