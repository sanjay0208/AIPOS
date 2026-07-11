from app.memory.search import search_memories


def is_duplicate_memory(
    memory: str,
    user_id: int,
) -> bool:
    """
    Check whether a similar memory already exists.

    Returns:
        True if a duplicate exists.
        False otherwise.
    """

    results = search_memories(
        query=memory,
        user_id=user_id,
        limit=1,
    )

    if not results:
        return False

    existing = results[0]["content"].strip().lower()
    incoming = memory.strip().lower()

    return existing == incoming