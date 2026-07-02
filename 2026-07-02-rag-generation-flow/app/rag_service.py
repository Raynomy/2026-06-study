import os

from dotenv import load_dotenv
from openai import OpenAI

from app.schemas import AnswerSource, DocumentAnswerResponse
from app.vector_store import search_chunks

load_dotenv()

client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
    timeout=60.0,
)

MIN_RELEVANCE_SCORE = 0.6

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
你是一个严格基于资料回答问题的中文助手。

要求：
1. 只能根据【资料】回答问题
2. 如果资料中没有答案，回答“资料中没有提到”
3. 不要编造资料外的信息
4. 回答要简洁清楚

【资料】
{context}

【问题】
{question}
"""

    response = client.chat.completions.create(
        model=os.getenv("AIHUBMIX_MODEL", "deepseek-v4-flash"),
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0.2,
        max_tokens=500,
    )

    answer = response.choices[0].message.content

    return DocumentAnswerResponse(
        question=question,
        answer=answer,
        sources=sources,
    )