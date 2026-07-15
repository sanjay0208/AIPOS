from uuid import uuid4

from qdrant_client.models import (
    Distance,
    PointStruct,
    VectorParams,
)

from app.vector.client import client

VECTOR_SIZE = 3072


def create_collection(
    collection_name: str,
):
    """
    Create a collection if it does not exist.
    """

    collections = client.get_collections().collections

    existing = [
        collection.name
        for collection in collections
    ]

    if collection_name not in existing:

        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )


def store_embedding(
    collection_name: str,
    embedding: list[float],
    payload: dict,
) -> str:
    """
    Store embedding into any Qdrant collection.
    """

    point_id = str(uuid4())

    client.upsert(
        collection_name=collection_name,
        points=[
            PointStruct(
                id=point_id,
                vector=embedding,
                payload=payload,
            )
        ],
    )

    return point_id