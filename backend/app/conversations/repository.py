from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.database.models.conversation import Conversation


class ConversationRepository:
    @staticmethod
    def create(
        db: Session,
        user_id: int,
        title: str,
    ) -> Conversation:
        conversation = Conversation(
            user_id=user_id,
            title=title,
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def get_by_id(
        db: Session,
        conversation_id: int,
    ) -> Conversation | None:
        return (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id)
            .first()
        )

    @staticmethod
    def get_all_by_user(
        db: Session,
        user_id: int,
    ) -> list[Conversation]:
        return (
            db.query(Conversation)
            .filter(Conversation.user_id == user_id)
            .order_by(Conversation.updated_at.desc())
            .all()
        )

    @staticmethod
    def search(
        db: Session,
        user_id: int,
        query: str,
    ) -> list[Conversation]:
        return (
            db.query(Conversation)
            .filter(
                Conversation.user_id == user_id,
                Conversation.title.ilike(f"%{query}%"),
            )
            .order_by(Conversation.updated_at.desc())
            .all()
        )

    @staticmethod
    def update_title(
        db: Session,
        conversation: Conversation,
        title: str,
    ) -> Conversation:
        conversation.title = title

        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def delete(
        db: Session,
        conversation: Conversation,
    ) -> None:
        db.delete(conversation)
        db.commit()