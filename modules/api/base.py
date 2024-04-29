from abc import ABC, abstractmethod
from typing import Optional

from modules.conversation_history import ConversationHistory
from modules.typing import MessageHistory


class LLMProvider(ABC):

    @staticmethod
    @abstractmethod
    def get_quick_query_completion(
            username: str, user_prompt: str, model: str, is_team_chat: bool = False
    ) -> None:
        ...

    @staticmethod
    @abstractmethod
    def get_chat_completion(username: str,
                            user_prompt: str,
                            conversation_history: ConversationHistory,
                            model,
                            is_team: bool = False,
                            ) -> ConversationHistory:
        ...

    @staticmethod
    @abstractmethod
    def _get_provider_response(conversation_history: MessageHistory, username: str, model: str) -> str:
        ...

    @staticmethod
    @abstractmethod
    def _try_get_response(conversation_history, username, model) -> Optional[str] :
        ...