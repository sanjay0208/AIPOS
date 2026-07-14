from sqlalchemy.orm import Session

from app.conversations.repository import ConversationRepository
from app.conversations.schemas import (
    ConversationCreate,
    ConversationListResponse,
    ConversationResponse,
)


class ConversationService:
    @staticmethod
    def create_conversation(
        db: Session,
        user_id: int,
        data: ConversationCreate,
    ) -> ConversationResponse:
        conversation = ConversationRepository.create(
            db=db,
            user_id=user_id,
            title=data.title,
        )

        return ConversationResponse.model_validate(conversation)

    @staticmethod
    def get_conversation(
        db: Session,
        conversation_id: int,
    ) -> ConversationResponse | None:
        conversation = ConversationRepository.get_by_id(
            db=db,
            conversation_id=conversation_id,
        )

        if conversation is None:
            return None

        return ConversationResponse.model_validate(conversation)

    @staticmethod
    def list_conversations(
        db: Session,
        user_id: int,
    ) -> ConversationListResponse:
        conversations = ConversationRepository.get_all_by_user(
            db=db,
            user_id=user_id,
        )

        return ConversationListResponse(
            conversations=[
                ConversationResponse.model_validate(c)
                for c in conversations
            ]
        )

    @staticmethod
    def search_conversations(
        db: Session,
        user_id: int,
        query: str,
    ) -> ConversationListResponse:
        conversations = ConversationRepository.search(
            db=db,
            user_id=user_id,
            query=query,
        )

        return ConversationListResponse(
            conversations=[
                ConversationResponse.model_validate(c)
                for c in conversations
            ]
        )

    @staticmethod
    def rename_conversation(
        db: Session,
        conversation_id: int,
        title: str,
    ) -> ConversationResponse | None:

        conversation = ConversationRepository.get_by_id(
            db=db,
            conversation_id=conversation_id,
        )

        if conversation is None:
            return None

        updated = ConversationRepository.update_title(
            db=db,
            conversation=conversation,
            title=title,
        )

        return ConversationResponse.model_validate(updated)

    @staticmethod
    def delete_conversation(
        db: Session,
        conversation_id: int,
    ) -> bool:

        conversation = ConversationRepository.get_by_id(
            db=db,
            conversation_id=conversation_id,
        )

        if conversation is None:
            return False

        ConversationRepository.delete(
            db=db,
            conversation=conversation,
        )

        return True