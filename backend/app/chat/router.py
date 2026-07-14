from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.chat.schemas import ChatRequest, ChatResponse
from app.chat.service import process_chat
from app.database.models.user import User
from app.database.session import get_db

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    response, conversation_id = process_chat(
        db=db,
        request=request,
        user_id=current_user.id,
    )

    return ChatResponse(
        response=response,
        conversation_id=conversation_id,
    )