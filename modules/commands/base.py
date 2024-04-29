from typing import Callable

from config import config
from modules.api.base import LLMProvider
from modules.command_controllers import InitializerConfig
from modules.typing import LogLine


class QuickQueryCommand:
    provider: LLMProvider = None
    model: str = None

    @classmethod
    def as_command(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> None:
            cls.provider.get_quick_query_completion(
                logline.username,
                logline.prompt,
                model=cls.model,
                is_team_chat=logline.is_team_message,
            )

        return func


class GlobalChatCommand:
    provider: LLMProvider = None
    model: str = None

    @classmethod
    def as_command(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> None:
            chat_history = cls.provider.get_chat_completion(
                logline.username,
                logline.prompt.removeprefix(config.GROQ_CHAT_COMMAND).strip(),
                shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL,
                is_team=logline.is_team_message,
                model=cls.model,
            )
            shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL = chat_history

        return func


class PrivateChatCommand:
    provider: LLMProvider = None
    model: str = None

    @classmethod
    def as_command(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> None:
            user_chat = shared_dict.CHAT_CONVERSATION_HISTORY.get_conversation_history(logline.player)

            chat_history = cls.provider.get_chat_completion(
                logline.username,
                logline.prompt.removeprefix(config.GROQ_PRIVATE_CHAT).strip(),
                user_chat,
                is_team=logline.is_team_message,
                model=cls.model,
            )
            shared_dict.CHAT_CONVERSATION_HISTORY.set_conversation_history(logline.player, chat_history)

        return func
