from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.conversations.message_service import MessageService
from app.conversations.schemas import (
    ConversationCreate,
    ConversationListResponse,
    ConversationResponse,
    ConversationUpdate,
    MessageListResponse,
)
from app.conversations.service import ConversationService
from app.database.models.user import User
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
    current_user: User = Depends(get_current_user),
):
    return ConversationService.create_conversation(
        db=db,
        user_id=current_user.id,
        data=data,
    )


@router.get(
    "",
    response_model=ConversationListResponse,
)
def list_conversations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ConversationService.list_conversations(
        db=db,
        user_id=current_user.id,
    )


@router.get(
    "/search",
    response_model=ConversationListResponse,
)
def search_conversations(
    q: str = Query(..., description="Search conversation title"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return ConversationService.search_conversations(
        db=db,
        user_id=current_user.id,
        query=q,
    )


@router.get(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def get_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied.",
        )

    return conversation


@router.get(
    "/{conversation_id}/messages",
    response_model=MessageListResponse,
)
def get_messages(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied.",
        )

    return MessageService.list_messages(
        db=db,
        conversation_id=conversation_id,
    )


@router.patch(
    "/{conversation_id}",
    response_model=ConversationResponse,
)
def rename_conversation(
    conversation_id: int,
    data: ConversationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied.",
        )

    updated = ConversationService.rename_conversation(
        db=db,
        conversation_id=conversation_id,
        title=data.title,
    )

    return updated


@router.delete(
    "/{conversation_id}",
)
def delete_conversation(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Access denied.",
        )

    ConversationService.delete_conversation(
        db=db,
        conversation_id=conversation_id,
    )

    return {
        "message": "Conversation deleted successfully."
    }