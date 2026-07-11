from uuid import uuid4

from qdrant_client.models import Distance, PointStruct, VectorParams

from app.vector.client import client

COLLECTION_NAME = "memories"
VECTOR_SIZE = 3072


def create_collection():
    """
    Create the memories collection if it doesn't exist.
    """

    collections = client.get_collections().collections
    existing = [c.name for c in collections]

    if COLLECTION_NAME not in existing:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def store_embedding(
    embedding: list[float],
    payload: dict,
) -> str:
    """
    Store an embedding in Qdrant.
    """

    point_id = str(uuid4())

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload,
            )
        ],
    )

    return point_id