from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """
    Base interface for all AI providers.
    """

    @abstractmethod
    def chat(self, message: str) -> str:
        pass