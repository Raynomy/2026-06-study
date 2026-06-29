import math
import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
)

embedding_model = os.getenv("AIHUBMIX_EMBEDDING_MODEL")


def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model=embedding_model,
        input=text,
    )

    return response.data[0].embedding


def cosine_similarity(vector_a: list[float], vector_b: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vector_a, vector_b))
    norm_a = math.sqrt(sum(a * a for a in vector_a))
    norm_b = math.sqrt(sum(b * b for b in vector_b))

    return dot_product / (norm_a * norm_b)


def search(query: str, documents: list[str], top_k: int = 3) -> list[dict]:
    query_embedding = get_embedding(query)

    results = []

    for document in documents:
        document_embedding = get_embedding(document)
        similarity = cosine_similarity(query_embedding, document_embedding)

        results.append(
            {
                "document": document,
                "similarity": similarity,
            }
        )

    results.sort(key=lambda item: item["similarity"], reverse=True)

    return results[:top_k]


documents = [
    "FastAPI 可以结合 JWT 实现用户登录和接口鉴权。",
    "SQLAlchemy 是 Python 常用的 ORM，可以用来操作数据库。",
    "Docker 可以把应用和运行环境打包成容器。",
    "pytest 可以用来给 FastAPI 接口编写自动化测试。",
    "Embedding 可以把文本转换成向量，用于语义检索。",
    "RAG 会先检索相关文档，再让大模型基于上下文生成答案。",
    "今天晚上我想吃火锅。",
]

queries = [
    "FastAPI 怎么实现用户登录鉴权？",
    "怎么给接口写自动化测试？",
    "RAG 为什么需要先检索文档？",
]

for query in queries:
    print("=" * 60)
    print("用户问题：")
    print(query)

    results = search(query=query, documents=documents, top_k=1)

    print(f"Top {len(results)} 检索结果：")
    for index, result in enumerate(results, start=1):
        print(f"{index}. 相似度：{result['similarity']:.4f}")
        print(f"   文档：{result['document']}")