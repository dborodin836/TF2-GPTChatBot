from abc import ABC, abstractmethod
from typing import Optional

from modules.typing import MessageHistory


class LLMProvider(ABC):

    @staticmethod
    @abstractmethod
    def _get_provider_response(conversation_history: MessageHistory, username: str, model: str) -> str:
        ...

    @staticmethod
    @abstractmethod
    def _try_get_response(conversation_history, username, model) -> Optional[str]:
        ...
