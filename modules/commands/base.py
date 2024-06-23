from abc import ABC, abstractmethod
from typing import Callable, List, Optional

from modules.api.llm.base import LLMProvider
from modules.command_controllers import CommandChatTypes, InitializerConfig
from modules.conversation_history import ConversationHistory
from modules.logs import get_logger
from modules.rcon_client import RconClient
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine, Message

main_logger = get_logger("main")


class BaseCommand(ABC):
    name: str
    settings = {}
    wrappers: List[Callable] = []

    @classmethod
    @abstractmethod
    def get_handler(cls): ...

    @classmethod
    def as_command(cls) -> Callable[[LogLine, InitializerConfig], None]:
        func = cls.get_handler()

        for decorator in cls.wrappers:
            func = decorator(func)

        return func


class RconCommand(BaseCommand):
    command: str

    @classmethod
    def get_handler(cls):
        def func(logline: LogLine, shared_dict: InitializerConfig) -> Optional[str]:
            if logline.prompt.strip():
                cmd = (
                    f"wait {cls.settings.get('wait-ms', 0)};{cls.command} {logline.prompt.strip()};"
                )
            else:
                cmd = f"wait {cls.settings.get('wait-ms', 0)};{cls.command};"
            with RconClient() as client:
                get_logger("gui").warning(cmd)
                client.run(cmd)
                return cmd

        return func


class LLMChatCommand(BaseCommand):
    provider: LLMProvider
    model: str = Optional[str]
    model_settings = {}
    chat: ConversationHistory

    @classmethod
    @abstractmethod
    def get_chat(cls, logline: LogLine, shared_dict: InitializerConfig) -> ConversationHistory: ...

    @classmethod
    def get_handler(cls) -> Callable[[LogLine, InitializerConfig], None]:
        def func(logline: LogLine, shared_dict: InitializerConfig) -> Optional[str]:
            chat = cls.get_chat(logline, shared_dict)

            chat.add_user_message_from_prompt(logline.prompt)

            response = cls.provider.get_completion_text(
                chat.get_messages_array(), logline.username, cls.model, cls.model_settings
            )
            if response:
                chat.add_assistant_message(Message(role="assistant", content=response))
                # Strip the message if needed
                if cls.settings.get("enable-hard-limit") and len(response) > cls.settings.get(
                    "enable-hard-limit"
                ):
                    main_logger.warning(
                        f"Message is longer than Hard Limit [{len(response)}]. Limit is {cls.settings.get('hard-limit-length')}."
                    )
                    response = response[: cls.settings.get("hard-limit-length", 300)] + "..."
                send_say_command_to_tf2(response, logline.username, logline.is_team_message)
                return " ".join(response.split())

        return func


class QuickQueryLLMCommand(LLMChatCommand):

    @classmethod
    def get_chat(cls, logline, shared_dict) -> ConversationHistory:
        return ConversationHistory(cls.settings)


class CommandGlobalChatLLMChatCommand(LLMChatCommand):
    @classmethod
    def get_chat(cls, logline, shared_dict) -> ConversationHistory:
        return shared_dict.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(
            cls.name, CommandChatTypes.GLOBAL, cls.settings
        )


class CommandPrivateChatLLMChatCommand(LLMChatCommand):
    @classmethod
    def get_chat(cls, logline, shared_dict) -> ConversationHistory:
        return shared_dict.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(
            cls.name, CommandChatTypes.PRIVATE, cls.settings, logline.player
        )
