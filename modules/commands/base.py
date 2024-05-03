from abc import ABC, abstractmethod
from typing import Callable, List, Optional

from modules.api.base import LLMProvider
from modules.command_controllers import CommandChatTypes, InitializerConfig
from modules.conversation_history import ConversationHistory
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine, Message
from modules.utils.text import remove_args


class BaseCommand(ABC):
    wrappers: List[Callable] = []
    name: str = None

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


class LLMChatCommand(BaseCommand):
    provider: LLMProvider = None
    model: str = None
    model_settings = {}
    chat: ConversationHistory = None
    chat_settings = {}

    @classmethod
    @abstractmethod
    def get_chat(cls, logline: LogLine, shared_dict: InitializerConfig) -> ConversationHistory:
        ...

    @classmethod
    def get_handler(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> Optional[str]:
            chat = cls.get_chat(logline, shared_dict)

            user_message = remove_args(logline.prompt)
            chat.add_user_message_from_prompt(user_message)

            response = cls.provider.get_completion_text(chat.get_messages_array(), logline.username,
                                                        cls.model, cls.model_settings)
            if response:
                chat.add_assistant_message(Message(role="assistant", content=response))
                send_say_command_to_tf2(response, logline.username, logline.is_team_message)
                return " ".join(response.split())

        return func


class QuickQueryLLMCommand(LLMChatCommand):

    @classmethod
    def get_chat(cls, logline, shared_dict) -> ConversationHistory:
        return ConversationHistory(cls.chat_settings)


class GlobalChatLLMChatCommand(LLMChatCommand):

    @classmethod
    def get_chat(cls, logline, shared_dict) -> ConversationHistory:
        return shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL


class PrivateChatLLMChatCommand(LLMChatCommand):

    @classmethod
    def get_chat(cls, logline, shared_dict) -> ConversationHistory:
        return shared_dict.CHAT_CONVERSATION_HISTORY.get_user_chat_history(logline.player)


class CommandGlobalChatLLMChatCommand(LLMChatCommand):
    @classmethod
    def get_chat(cls, logline, shared_dict) -> ConversationHistory:
        return shared_dict.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(cls.name,
                                                                                        CommandChatTypes.GLOBAL,
                                                                                        cls.chat_settings)


class CommandPrivateChatLLMChatCommand(LLMChatCommand):
    @classmethod
    def get_chat(cls, logline, shared_dict) -> ConversationHistory:
        return shared_dict.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(cls.name,
                                                                                        CommandChatTypes.PRIVATE,
                                                                                        cls.chat_settings,
                                                                                        logline.player)
