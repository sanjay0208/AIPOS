from google import genai

from app.ai.providers.base import BaseAIProvider
from app.core.config import settings


class GeminiProvider(BaseAIProvider):
    """
    Google Gemini AI Provider
    """

    def __init__(self):
        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    def chat(self, message: str) -> str:
        response = self.client.models.generate_content(
            model="gemini-flash-latest",
            contents=message,
        )

        return response.text