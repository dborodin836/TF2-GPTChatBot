from abc import ABC, abstractmethod
from typing import Callable, List, Optional

from modules.api.base import LLMProvider
from modules.command_controllers import InitializerConfig
from modules.conversation_history import ConversationHistory
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine, Message
from modules.utils.text import remove_args


class BaseLLMCommand(ABC):
    provider: LLMProvider = None
    model: str = None
    wrappers: List[Callable] = []
    settings = {}

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


class QuickQueryLLMCommand(BaseLLMCommand):

    @classmethod
    def get_handler(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> Optional[str]:
            tmp_chat_history = ConversationHistory()

            user_message = remove_args(logline.prompt)
            tmp_chat_history.add_user_message_from_prompt(user_message)

            response = cls.provider.get_completion_text(tmp_chat_history.get_messages_array(), logline.username,
                                                        cls.model, cls.settings)
            if response:
                tmp_chat_history.add_assistant_message(Message(role="assistant", content=response))
                send_say_command_to_tf2(response, logline.username, logline.is_team_message)
                return " ".join(response.split())

        return func


class GlobalChatLLMCommand(BaseLLMCommand):

    @classmethod
    def get_handler(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> Optional[str]:
            chat_history = shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL

            user_message = remove_args(logline.prompt)
            chat_history.add_user_message_from_prompt(user_message)

            response = cls.provider.get_completion_text(chat_history.get_messages_array(), logline.username,
                                                        cls.model, cls.settings)
            if response:
                chat_history.add_assistant_message(Message(role="assistant", content=response))
                send_say_command_to_tf2(response, logline.username, logline.is_team_message)
                return " ".join(response.split())

        return func


class PrivateChatLLMCommand(BaseLLMCommand):

    @classmethod
    def get_handler(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> Optional[str]:
            chat_history = shared_dict.CHAT_CONVERSATION_HISTORY.get_conversation_history(logline.player)

            user_message = remove_args(logline.prompt)
            chat_history.add_user_message_from_prompt(user_message)

            response = cls.provider.get_completion_text(chat_history.get_messages_array(), logline.username,
                                                        cls.model, cls.settings)
            if response:
                chat_history.add_assistant_message(Message(role="assistant", content=response))
                send_say_command_to_tf2(response, logline.username, logline.is_team_message)
                return " ".join(response.split())

        return func
