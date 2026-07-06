import os

from dotenv import load_dotenv
from openai import OpenAI

from app.exceptions import RAGServiceError
from app.schemas import AnswerSource, DocumentAnswerResponse
from app.vector_store import search_chunks

load_dotenv()

CHAT_MODEL = os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash")

openai_client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
    timeout=60.0,
)

MIN_RELEVANCE_SCORE = 0.75

def build_context(sources: list[AnswerSource]) -> str:
    context_parts = []

    for index, source in enumerate(sources, start=1):
        context_parts.append(
            f"[资料{index}]\n"
            f"来源：{source.source}\n"
            f"段落：{source.paragraph}\n"
            f"内容：{source.text}"
        )

    return "\n\n".join(context_parts)


def answer_with_context(question: str, top_k: int = 3) -> DocumentAnswerResponse:
    search_results = [
        result
        for result in search_chunks(query=question, top_k=top_k)
        if result.score >= MIN_RELEVANCE_SCORE
    ]

    sources = [
        AnswerSource(
            chunk_id=result.chunk_id,
            source=result.source,
            paragraph=result.paragraph,
            score=result.score,
            text=result.text,
        )
        for result in search_results
    ]

    if not sources:
        return DocumentAnswerResponse(
            question=question,
            answer="我没有在已上传的资料中找到相关内容。",
            sources=[],
        )

    context = build_context(sources)

    prompt = f"""
你是一个严格遵守 grounding 规则的中文 RAG 助手。

你的任务：
只根据【资料】回答【问题】。

Grounding 规则：
1. 只能使用【资料】中明确出现的信息
2. 不能使用你自己的背景知识补充答案
3. 不能推测、扩展或编造资料外的信息
4. 如果【资料】不足以回答问题，必须回答“资料中没有提到”
5. 如果只能回答一部分，就只回答资料能支持的部分
6. 回答要简洁清楚

【资料】
{context}

【问题】
{question}
"""

    try:
        response = openai_client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": "你是一个严格遵守资料来源的中文 RAG 助手。",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.2,
            max_tokens=500,
        )
    except Exception as exc:
        raise RAGServiceError(
            code="LLM_GENERATION_ERROR",
            message="Failed to generate answer",
        ) from exc

    answer = response.choices[0].message.content

    if answer is None:
        raise RAGServiceError(
            code="LLM_EMPTY_ANSWER",
            message="LLM returned empty answer",
        )

    return DocumentAnswerResponse(
        question=question,
        answer=answer,
        sources=sources,
    )
