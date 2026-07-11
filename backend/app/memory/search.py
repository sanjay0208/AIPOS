from app.embeddings.service import generate_embedding
from app.vector.search import search_embeddings


def search_memories(
    query: str,
    user_id: int,
    limit: int = 5,
):
    """
    Search semantic memories belonging to a specific user.

    Steps:
    1. Generate query embedding.
    2. Search Qdrant.
    3. Return matching memories.
    """

    embedding = generate_embedding(query)

    results = search_embeddings(
        embedding=embedding,
        user_id=user_id,
        limit=limit,
    )

    memories = []

    for result in results:
        if result.payload:
            memories.append(result.payload)

    return memories