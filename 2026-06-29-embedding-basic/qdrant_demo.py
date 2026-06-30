import os

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams


load_dotenv()

COLLECTION_NAME = "study_chunks"
EMBEDDING_MODEL = os.getenv("AIHUBMIX_EMBEDDING_MODEL", "text-embedding-3-small")

openai_client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
)

qdrant_client = QdrantClient(":memory:")


def get_embedding(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding


chunks = [
    {
        "chunk_id": "fastapi-auth-001",
        "text": "FastAPI 可以结合 JWT 实现用户登录和接口鉴权。",
        "source": "fastapi_notes.md",
        "metadata": {
            "topic": "FastAPI",
            "section": "鉴权",
        },
    },
    {
        "chunk_id": "fastapi-test-001",
        "text": "pytest 可以用来给 FastAPI 接口编写自动化测试。",
        "source": "fastapi_notes.md",
        "metadata": {
            "topic": "FastAPI",
            "section": "测试",
        },
    },
    {
        "chunk_id": "rag-basic-001",
        "text": "RAG 会先检索相关文档，再让大模型基于上下文生成答案。",
        "source": "rag_notes.md",
        "metadata": {
            "topic": "RAG",
            "section": "基础流程",
        },
    },
]

qdrant_client.create_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(
        size=1024,
        distance=Distance.COSINE,
    ),
)

points = []

for index, chunk in enumerate(chunks, start=1):
    vector = get_embedding(chunk["text"])

    points.append(
        PointStruct(
            id=index,
            vector=vector,
            payload={
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "source": chunk["source"],
                "metadata": chunk["metadata"],
            },
        )
    )

qdrant_client.upsert(
    collection_name=COLLECTION_NAME,
    points=points,
)

print("Inserted chunks:", len(points))


query = "FastAPI 怎么实现用户登录鉴权？"
query_vector = get_embedding(query)

search_results = qdrant_client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,
    limit=2,
)

print("=" * 60)
print("用户问题：")
print(query)
print("检索结果：")

for index, result in enumerate(search_results.points, start=1):
    payload = result.payload

    print(f"{index}. 相似度：{result.score:.4f}")
    print(f"   chunk_id：{payload['chunk_id']}")
    print(f"   source：{payload['source']}")
    print(f"   metadata：{payload['metadata']}")
    print(f"   text：{payload['text']}")