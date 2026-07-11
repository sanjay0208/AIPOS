from app.core.config import settings

from app.ai.providers.mock_provider import MockProvider
from app.ai.providers.gemini_provider import GeminiProvider


class AIManager:
    """
    Central AI Manager
    """

    def __init__(self):

        if settings.AI_PROVIDER.lower() == "gemini":
            self.provider = GeminiProvider()

        else:
            self.provider = MockProvider()

    def chat(self, message: str) -> str:
        return self.provider.chat(message)


ai_manager = AIManager()