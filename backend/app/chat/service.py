from app.ai.manager import ai_manager
from app.chat.schemas import ChatRequest


def process_chat(request: ChatRequest) -> str:
    """
    Process chat using the configured AI provider.
    """

    return ai_manager.chat(request.message)