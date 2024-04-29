from abc import ABC, abstractmethod
from typing import Callable, List

from config import config
from modules.api.base import LLMProvider
from modules.command_controllers import InitializerConfig
from modules.logs import log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine, Message
from modules.utils.text import get_system_message, remove_args


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
            log_gui_model_message(cls.model, logline.username, logline.prompt)

            user_message = remove_args(logline.prompt)
            sys_message = get_system_message(logline.prompt)

            payload = [
                sys_message,
                Message(role="assistant", content=config.GREETING),
                Message(role="user", content=user_message),
            ]

            response = cls.provider._try_get_response(payload, logline.username, cls.model)

            if response:
                log_gui_model_message(cls.model, logline.username, " ".join(response.split()))
                send_say_command_to_tf2(response, logline.username, logline.is_team_message)

        return func


class GlobalChatCommand(BaseCommand):

    @classmethod
    def get_handler(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> None:
            log_gui_model_message(cls.model, logline.username, logline.prompt)
            chat_history = shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL

            user_message = remove_args(logline.prompt)
            chat_history.add_user_message_from_prompt(user_message)

            response = cls.provider._try_get_response(chat_history.get_messages_array(), logline.username,
                                                      cls.model)
            if response:
                chat_history.add_assistant_message(Message(role="assistant", content=response))
                log_gui_model_message(cls.model, logline.username, " ".join(response.split()))
                send_say_command_to_tf2(response, logline.username, logline.is_team_message)

        return func


class PrivateChatCommand(BaseCommand):

    @classmethod
    def get_handler(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> None:
            log_gui_model_message(cls.model, logline.username, logline.prompt)
            chat_history = shared_dict.CHAT_CONVERSATION_HISTORY.get_conversation_history(logline.player)

            user_message = remove_args(logline.prompt)
            chat_history.add_user_message_from_prompt(user_message)

            response = cls.provider._try_get_response(chat_history.get_messages_array(), logline.username,
                                                      cls.model)
            if response:
                chat_history.add_assistant_message(Message(role="assistant", content=response))
                log_gui_model_message(cls.model, logline.username, " ".join(response.split()))
                send_say_command_to_tf2(response, logline.username, logline.is_team_message)

        return func
