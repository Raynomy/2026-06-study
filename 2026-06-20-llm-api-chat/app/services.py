import os

from openai import OpenAI

from app.memory import get_history, save_message

from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
)


def chat_with_llm(session_id: str, question: str) -> str:
    history = get_history(session_id)

    messages = [
        {
            "role": "system",
            "content": "你是一个耐心、清晰的中文学习助手。",
        },
        *history,
        {
            "role": "user",
            "content": question,
        },
    ]

    response = client.chat.completions.create(
        model=os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash"),
        messages=messages,
        temperature=0.7,
        max_tokens=500,
    )

    answer = response.choices[0].message.content

    save_message(session_id, "user", question)
    save_message(session_id, "assistant", answer)

    return answer