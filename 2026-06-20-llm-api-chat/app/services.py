import logging
import os
import time

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from app.exceptions import LLMServiceError
from app.memory import get_history, save_message

load_dotenv()

logger = logging.getLogger(__name__)

MAX_RETRY_COUNT = 2
RETRY_DELAY_SECONDS = 1

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

    answer = ""

    for attempt in range(MAX_RETRY_COUNT + 1):
        try:
            response = client.chat.completions.create(
                model=os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash"),
                messages=messages,
                temperature=0.7,
                max_tokens=500,
            )

            answer = response.choices[0].message.content or ""

            if response.usage:
                logger.info(
                    "LLM usage prompt_tokens=%s completion_tokens=%s total_tokens=%s",
                    response.usage.prompt_tokens,
                    response.usage.completion_tokens,
                    response.usage.total_tokens,
                )

            break

        except OpenAIError as exc:
            logger.error(
                "LLM API error attempt=%s error=%s",
                attempt + 1,
                exc,
            )

            if attempt == MAX_RETRY_COUNT:
                raise LLMServiceError() from exc

            time.sleep(RETRY_DELAY_SECONDS)

    save_message(session_id, "user", question)
    save_message(session_id, "assistant", answer)

    return answer


def chat_with_llm_stream(session_id: str, question: str):
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

    try:
        stream = client.chat.completions.create(
            model=os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash"),
            messages=messages,
            temperature=0.7,
            max_tokens=500,
            stream=True,
        )

        full_answer = ""

        for chunk in stream:
            content = chunk.choices[0].delta.content

            if content:
                full_answer += content
                yield content

    except OpenAIError as exc:
        logger.error("LLM stream API error error=%s", exc)
        raise LLMServiceError() from exc

    save_message(session_id, "user", question)
    save_message(session_id, "assistant", full_answer)