from abc import ABC, abstractmethod
from typing import Callable, List

from modules.api.base import LLMProvider
from modules.command_controllers import InitializerConfig
from modules.typing import LogLine


class BaseCommand(ABC):
    provider: LLMProvider = None
    model: str = None
    wrappers: List[Callable] = []

    @classmethod
    @abstractmethod
    def get_handler(cls):
        ...

    @classmethod
    def as_command(cls) -> Callable[[LogLine, InitializerConfig], None]:
        func = cls.get_handler()

        for decorator in cls.wrappers:
            func = decorator(func)

        return func


class QuickQueryCommand(BaseCommand):

    @classmethod
    def get_handler(cls):
        def func(logline: LogLine, shared_dict: InitializerConfig) -> None:
            cls.provider.get_quick_query_completion(
                logline.username,
                logline.prompt,
                model=cls.model,
                is_team_chat=logline.is_team_message,
            )

        return func


class GlobalChatCommand(BaseCommand):

    @classmethod
    def get_handler(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> None:
            chat_history = cls.provider.get_chat_completion(
                logline.username,
                logline.prompt,
                shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL,
                is_team=logline.is_team_message,
                model=cls.model,
            )
            shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL = chat_history

        return func


class PrivateChatCommand(BaseCommand):

    @classmethod
    def get_handler(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> None:
            user_chat = shared_dict.CHAT_CONVERSATION_HISTORY.get_conversation_history(logline.player)

            chat_history = cls.provider.get_chat_completion(
                logline.username,
                logline.prompt,
                user_chat,
                is_team=logline.is_team_message,
                model=cls.model,
            )
            shared_dict.CHAT_CONVERSATION_HISTORY.set_conversation_history(logline.player, chat_history)

        return func
