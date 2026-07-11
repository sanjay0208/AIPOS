from qdrant_client import QdrantClient
from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.core.config import settings

client = QdrantClient(
    host=settings.QDRANT_HOST,
    port=settings.QDRANT_PORT,
)


def search_embeddings(
    embedding: list[float],
    user_id: int,
    limit: int = 5,
):
    """
    Search the Qdrant vector database using semantic similarity.

    Only returns memories belonging to the specified user.
    """

    results = client.query_points(
        collection_name="memories",
        query=embedding,
        limit=limit,
        with_payload=True,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id),
                )
            ]
        ),
    )

    return results.points