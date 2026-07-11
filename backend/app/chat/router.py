from fastapi import APIRouter

from app.chat.schemas import (
    ChatRequest,
    ChatResponse,
)
from app.chat.service import process_chat

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(request: ChatRequest):
    response = process_chat(request)

    return ChatResponse(
        response=response,
    )