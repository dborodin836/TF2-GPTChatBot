from abc import ABC, abstractmethod

from modules.typing import MessageHistory


class LLMProvider(ABC):

    @staticmethod
    @abstractmethod
    def get_completion_text(message_array: MessageHistory, username: str, model: str) -> str:
        ...
