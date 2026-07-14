from sqlalchemy.orm import Session

from app.conversations.message_repository import MessageRepository
from app.conversations.schemas import (
    MessageCreate,
    MessageListResponse,
    MessageResponse,
)


class MessageService:
    @staticmethod
    def create_message(
        db: Session,
        conversation_id: int,
        data: MessageCreate,
    ) -> MessageResponse:
        message = MessageRepository.create(
            db=db,
            conversation_id=conversation_id,
            role=data.role,
            content=data.content,
        )

        return MessageResponse.model_validate(message)

    @staticmethod
    def list_messages(
        db: Session,
        conversation_id: int,
    ) -> MessageListResponse:

        messages = MessageRepository.list_by_conversation(
            db=db,
            conversation_id=conversation_id,
        )

        return MessageListResponse(
            messages=[
                MessageResponse.model_validate(message)
                for message in messages
            ]
        )