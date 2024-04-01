from typing import Any, Callable, Dict, Optional

import pydantic
from ordered_set import OrderedSet
from pydantic import BaseModel, ConfigDict

from modules.conversation_history import ConversationHistory
from modules.logs import get_logger
from modules.set_once_dict import SetOnceDictionary
from modules.typing import Command, LogLine, Player

main_logger = get_logger("main")
combo_logger = get_logger("combo")
gui_logger = get_logger("gui")


class ChatHistoryManager:
    model_config = ConfigDict(arbitrary_types_allowed=True)

    def __init__(self, /, **data: Any):
        super().__init__(**data)
        self.GLOBAL: ConversationHistory = ConversationHistory()
        self.PRIVATE_CHATS: Dict[str, ConversationHistory] = dict()

    def set_conversation_history(self, player: Player, conv_history: ConversationHistory) -> None:
        attr_name = self._get_conv_history_attr_name(player.steamid64)

        self.PRIVATE_CHATS[attr_name] = conv_history

    def get_conversation_history(self, player: Player) -> ConversationHistory:
        attr_name = self._get_conv_history_attr_name(player.steamid64)

        user_chat = self.PRIVATE_CHATS.get(attr_name)

        if user_chat:
            return user_chat

        main_logger.info(
            f"Conversation history for user '{player.name}' [{player.steamid64}] doesn't exist. Creating..."
        )
        new_chat = ConversationHistory()
        self.PRIVATE_CHATS[attr_name] = new_chat
        return new_chat

    def _get_conv_history_attr_name(self, id64: int) -> str:
        return f"USER_{id64}_CH"


class InitializerConfig(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    CHAT_CONVERSATION_HISTORY: ChatHistoryManager = pydantic.Field(
        default_factory=ChatHistoryManager
    )


class GuiCommandController:
    def __init__(
        self, initializer_config: Optional[dict] = None, disable_help: bool = False
    ) -> None:
        self.__named_commands_registry: SetOnceDictionary[str, Command] = SetOnceDictionary()
        self.__shared = dict()

        if not disable_help:
            self.__named_commands_registry.update(
                {"help": Command("help", self.help, "Prints this message.")}
            )

        if initializer_config is not None:
            self.__shared.update(initializer_config)

    def register_command(self, name: str, function: Callable, description: str) -> None:
        self.__named_commands_registry[name] = Command(name, function, description)

    def process_line(self, line: str):
        command_name = line.strip().split(" ")[0].lower()

        command: Optional[Command] = self.__named_commands_registry.get(command_name, None)
        if command is None:
            combo_logger.error(f"Command '{command_name}' not found.")
            return

        command.function(line, self.__shared)

    def help(self, command: str, shared_dict: dict):
        gui_logger.info("### HELP ###")
        max_cmd_length: Command = max(
            self.__named_commands_registry.values(), key=lambda cmd: len(cmd.name)
        )
        max_length = len(max_cmd_length.name)
        for cmd in self.__named_commands_registry.values():
            gui_logger.info(f"- {cmd.name:>{max_length}} | {cmd.description}")


class CommandController:
    def __init__(self, initializer_config: Optional[InitializerConfig] = None) -> None:
        self.__services: OrderedSet[Callable] = OrderedSet()
        self.__named_commands_registry: SetOnceDictionary[str, Callable] = SetOnceDictionary()
        self.__shared = InitializerConfig()

        if initializer_config is not None:
            self.__shared.__dict__.update(initializer_config)

    def register_command(self, name: str, function: Callable) -> None:
        self.__named_commands_registry[name] = function

    def register_service(self, function: Callable):
        self.__services.add(function)

    def process_line(self, logline: LogLine):
        for task in self.__services:
            task(logline, self.__shared)

        command_name = logline.prompt.strip().split(" ")[0].lower()

        handler: Optional[Callable] = self.__named_commands_registry.get(command_name, None)
        if handler is None:
            return

        handler(logline, self.__shared)
