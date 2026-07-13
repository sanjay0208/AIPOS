from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.conversations.schemas import (
    ConversationCreate,
    ConversationListResponse,
    ConversationResponse,
)
from app.conversations.service import ConversationService
from app.database.session import get_db

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post(
    "",
    response_model=ConversationResponse,
)
def create_conversation(
    data: ConversationCreate,
    db: Session = Depends(get_db),
):
    # TODO: Replace with authenticated user
    user_id = 1

    return ConversationService.create_conversation(
        db=db,
        user_id=user_id,
        data=data,
    )


@router.get(
    "",
    response_model=ConversationListResponse,
)
def list_conversations(
    db: Session = Depends(get_db),
):
    # TODO: Replace with authenticated user
    user_id = 1

    return ConversationService.list_conversations(
        db=db,
        user_id=user_id,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
):
    conversation = ConversationService.get_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Conversation not found.",
        )

    return conversation