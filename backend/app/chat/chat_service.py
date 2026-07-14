from sqlalchemy.orm import Session

from app.chat.schemas import ChatRequest
from app.chat.service import process_chat
from app.conversations.message_service import MessageService
from app.conversations.schemas import MessageCreate


class ChatService:
    @staticmethod
    def chat(
        db: Session,
        request: ChatRequest,
        user_id: int,
    ) -> str:

        # Ensure a conversation exists
        if request.conversation_id is None:
            raise ValueError(
                "conversation_id is required."
            )

        # Save user message
        MessageService.create_message(
            db=db,
            conversation_id=request.conversation_id,
            data=MessageCreate(
                role="user",
                content=request.message,
            ),
        )

        # Existing AI pipeline
        response = process_chat(
            db=db,
            request=request,
            user_id=user_id,
        )

        # Save assistant response
        MessageService.create_message(
            db=db,
            conversation_id=request.conversation_id,
            data=MessageCreate(
                role="assistant",
                content=response,
            ),
        )

        return response