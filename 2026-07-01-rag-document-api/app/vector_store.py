import os
from uuid import uuid4

from dotenv import load_dotenv
from openai import OpenAI
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, VectorParams

from app.schemas import SearchResult


load_dotenv()

COLLECTION_NAME = "documents"
VECTOR_SIZE = 1024
EMBEDDING_MODEL = os.getenv("AIHUBMIX_EMBEDDING_MODEL", "text-embedding-3-small")

openai_client = OpenAI(
    api_key=os.getenv("AIHUBMIX_API_KEY"),
    base_url=os.getenv("AIHUBMIX_BASE_URL"),
    timeout=60.0,
)

qdrant_client = QdrantClient(":memory:")


def get_embedding(text: str) -> list[float]:
    response = openai_client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding


def init_collection() -> None:
    existing_collections = qdrant_client.get_collections().collections
    existing_names = [collection.name for collection in existing_collections]

    if COLLECTION_NAME in existing_names:
        return

    qdrant_client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=VECTOR_SIZE,
            distance=Distance.COSINE,
        ),
    )


def add_chunks(filename: str, chunks: list[str]) -> int:
    init_collection()

    points = []

    for index, chunk in enumerate(chunks, start=1):
        chunk_id = f"{filename}-{index}-{uuid4().hex[:8]}"
        point_id = str(uuid4())
        vector = get_embedding(chunk)

        points.append(
            PointStruct(
                id=point_id,
                vector=vector,
                payload={
                    "chunk_id": chunk_id,
                    "text": chunk,
                    "source": filename,
                    "paragraph": index,
                },
            )
        )

    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=points,
    )

    return len(points)


def search_chunks(query: str, top_k: int) -> list[SearchResult]:
    init_collection()

    query_vector = get_embedding(query)

    search_results = qdrant_client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
    )

    results = []

    for result in search_results.points:
        payload = result.payload

        results.append(
            SearchResult(
                chunk_id=payload["chunk_id"],
                text=payload["text"],
                source=payload["source"],
                paragraph=payload["paragraph"],
                score=result.score,
            )
        )

    return results