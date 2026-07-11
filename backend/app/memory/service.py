from sqlalchemy.orm import Session

from app.embeddings.service import generate_embedding
from app.memory.repository import MemoryRepository
from app.memory.schemas import MemoryCreate
from app.vector.service import store_embedding


def save_memory(
    db: Session,
    user_id: int,
    memory: MemoryCreate,
):
    """
    Complete memory pipeline:

    1. Save memory to PostgreSQL
    2. Generate embedding
    3. Store embedding in Qdrant
    4. Update PostgreSQL with vector_id
    """

    # Step 1: Save to PostgreSQL
    saved_memory = MemoryRepository.create(
        db=db,
        user_id=user_id,
        content=memory.content,
    )

    # Step 2: Generate embedding
    embedding = generate_embedding(
        saved_memory.content
    )

    # Step 3: Store in Qdrant
    vector_id = store_embedding(
        embedding=embedding,
        payload={
            "memory_id": saved_memory.id,
            "user_id": saved_memory.user_id,
            "content": saved_memory.content,
        },
    )

    # Step 4: Update PostgreSQL
    MemoryRepository.update_vector_id(
        db=db,
        memory=saved_memory,
        vector_id=vector_id,
    )

    return {
        "message": "Memory stored successfully.",
        "content": saved_memory.content,
    }