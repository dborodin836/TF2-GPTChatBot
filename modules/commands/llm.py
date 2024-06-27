from abc import abstractmethod
from typing import Callable, Optional

from modules.api.llm.base import LLMProvider
from modules.command_controllers import CommandChatTypes, InitializerConfig
from modules.commands.base import BaseCommand, main_logger
from modules.conversation_history import ConversationHistory
from modules.logs import get_logger
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import ConfirmationStatus, GameChatMessage, Message

main_logger = get_logger("main")
gui_logger = get_logger("gui")


class LLMChatCommand(BaseCommand):
    provider: LLMProvider
    model: str = Optional[str]
    model_settings = {}
    chat: ConversationHistory

    @classmethod
    @abstractmethod
    def get_chat(cls, logline: GameChatMessage, shared_dict: InitializerConfig) -> ConversationHistory:
        ...

    @classmethod
    def get_handler(cls) -> Callable[[GameChatMessage, InitializerConfig], None]:
        def func(logline: GameChatMessage, shared_dict: InitializerConfig) -> Optional[str]:
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


class ConfirmableLLMChatCommand(LLMChatCommand):

    @classmethod
    @abstractmethod
    def get_chat(cls, logline: GameChatMessage, shared_dict: InitializerConfig) -> ConversationHistory:
        ...

    @classmethod
    def get_handler(cls) -> Callable[[GameChatMessage, InitializerConfig], None]:
        def func(logline: GameChatMessage, shared_dict: InitializerConfig) -> Optional[str]:
            confirmation = shared_dict.CONFIRMATIONS.get(cls.name, {})
            status = confirmation.get("status", None)

            # Send the message after confirmation
            if status == ConfirmationStatus.CONFIRMED:
                chat = cls.get_chat(logline, shared_dict)
                response = shared_dict.CONFIRMATIONS[cls.name]["output"]
                chat.add_assistant_message(Message(role="assistant", content=response))

                if cls.settings.get("enable-hard-limit") and len(response) > cls.settings.get(
                        "enable-hard-limit"
                ):
                    main_logger.warning(
                        f"Message is longer than Hard Limit [{len(response)}]. Limit is {cls.settings.get('hard-limit-length')}."
                    )
                    response = response[: cls.settings.get("hard-limit-length", 300)] + "..."
                send_say_command_to_tf2(response, logline.username, logline.is_team_message)

                # Remove the confirmation request
                shared_dict.CONFIRMATIONS[cls.name] = {}

                return " ".join(response.split())
            else:
                chat = cls.get_chat(logline, shared_dict)

                chat.add_user_message_from_prompt(logline.prompt)

                response = cls.provider.get_completion_text(
                    chat.get_messages_array(), logline.username, cls.model, cls.model_settings
                )
                if response:
                    # Put the confirmation request
                    shared_dict.CONFIRMATIONS[cls.name] = {
                        "status": ConfirmationStatus.WAITING,
                        "input": logline,
                        "output": response
                    }

                    return " ".join(response.split())

        return func


class ConfirmableQuickQueryLLMCommand(ConfirmableLLMChatCommand):
    @classmethod
    def get_chat(cls, logline, shared_dict) -> ConversationHistory:
        return ConversationHistory(cls.settings)


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
