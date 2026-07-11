from sqlalchemy.orm import Session

from app.database.models.memory import Memory


class MemoryRepository:

    @staticmethod
    def create(
        db: Session,
        user_id: int,
        content: str,
    ) -> Memory:

        memory = Memory(
            user_id=user_id,
            content=content,
        )

        db.add(memory)
        db.commit()
        db.refresh(memory)

        return memory

    @staticmethod
    def update_vector_id(
        db: Session,
        memory: Memory,
        vector_id: str,
    ) -> Memory:

        memory.vector_id = vector_id
        memory.is_embedded = True

        db.commit()
        db.refresh(memory)

        return memory