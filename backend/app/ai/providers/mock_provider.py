from app.ai.providers.base import BaseAIProvider


class MockProvider(BaseAIProvider):
    """
    Temporary AI provider used during development.
    """

    def chat(self, message: str) -> str:
        return (
            f"🤖 Mock AI Response\n\n"
            f"You said:\n"
            f"{message}\n\n"
            f"This response is coming from the Mock Provider."
        )