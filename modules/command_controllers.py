import enum
from typing import Callable, Dict, List, Optional

import pydantic
from ordered_set import OrderedSet
from pydantic import BaseModel, ConfigDict

from modules.conversation_history import ConversationHistory
from modules.logs import get_logger, log_gui_model_message
from modules.set_once_dict import SetOnceDictionary
from modules.typing import GuiCommand, LogLine, Player, Command

main_logger = get_logger("main")
combo_logger = get_logger("combo")
gui_logger = get_logger("gui")

PRIVATE_CHAT_ID = "CMD_{0}_USR_{1}"
GLOBAL_CHAT_ID = "CMD_{0}"


class CommandChatTypes(enum.Enum):
    GLOBAL = 1
    PRIVATE = 2


class ChatHistoryManager(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    COMMAND: Dict = {}

    def get_or_create_command_chat_history(
            self, cmd_name: str, type_: CommandChatTypes, settings: dict = None, user: Player = None
    ):
        if settings is None:
            settings = {}

        match type_:
            case CommandChatTypes.PRIVATE:
                if chat_history := self.COMMAND.get(
                        PRIVATE_CHAT_ID.format(cmd_name, user.steamid64)
                ):
                    return chat_history
                main_logger.info(
                    f"Conversation history for command '{cmd_name}' [{type_}] doesn't exist. Creating..."
                )
                combo_logger.trace(
                    f'Creating chat history "{PRIVATE_CHAT_ID.format(cmd_name, user.steamid64)}"'
                )
                new_ch = ConversationHistory(settings)
                self.COMMAND[PRIVATE_CHAT_ID.format(cmd_name, user.steamid64)] = new_ch
                return new_ch

            case CommandChatTypes.GLOBAL:
                if chat_history := self.COMMAND.get(GLOBAL_CHAT_ID.format(cmd_name)):
                    return chat_history
                main_logger.info(
                    f"Conversation history for command '{cmd_name}' [{type_}] doesn't exist. Creating..."
                )
                new_ch = ConversationHistory(settings)
                self.COMMAND[GLOBAL_CHAT_ID.format(cmd_name)] = new_ch
                return new_ch

    def get_command_chat_history(
            self, command_name: str, type_: CommandChatTypes, user: Player = None
    ) -> Optional[ConversationHistory]:
        match type_:
            case CommandChatTypes.PRIVATE:
                if user is None:
                    raise Exception("User argument must be provided for private chat retrieval.")
                combo_logger.trace(PRIVATE_CHAT_ID.format(command_name, user.steamid64))
                if chat_history := self.COMMAND.get(
                        PRIVATE_CHAT_ID.format(command_name, user.steamid64)
                ):
                    return chat_history
                return None

            case CommandChatTypes.GLOBAL:
                combo_logger.trace(GLOBAL_CHAT_ID.format(command_name))
                if chat_history := self.COMMAND.get(GLOBAL_CHAT_ID.format(command_name)):
                    return chat_history
                return None

    def set_command_chat_history(
            self,
            name: str,
            type_: CommandChatTypes,
            chat_history: ConversationHistory,
            user: Player = None,
    ):
        match type_:
            case CommandChatTypes.PRIVATE:
                self.COMMAND[PRIVATE_CHAT_ID.format(name, user.steamid64)] = chat_history

            case CommandChatTypes.GLOBAL:
                self.COMMAND[GLOBAL_CHAT_ID.format(name)] = chat_history


class InitializerConfig(BaseModel):
    CHAT_CONVERSATION_HISTORY: ChatHistoryManager = pydantic.Field(
        default_factory=ChatHistoryManager
    )
    # Stores reference name for the commands e.g. !gpt3 ref. name is gpt3, prefix is !
    LOADED_COMMANDS: List[str] = []


class GuiCommandController:
    def __init__(self, initializer_config: dict = None, disable_help: bool = False) -> None:
        self.__named_commands_registry: SetOnceDictionary[str, GuiCommand] = SetOnceDictionary()
        self.__shared = dict()

        if not disable_help:
            self.__named_commands_registry.update(
                {"help": GuiCommand("help", self.help, "Prints this message.")}
            )

        if initializer_config is not None:
            self.__shared.update(initializer_config)

    def register_command(self, name: str, function: Callable, description: str) -> None:
        self.__named_commands_registry[name] = GuiCommand(name, function, description)

    def process_line(self, line: str):
        command_name = line.strip().split(" ")[0].lower()

        command: Optional[GuiCommand] = self.__named_commands_registry.get(command_name, None)
        if command is None:
            combo_logger.error(f"Command '{command_name}' not found.")
            return

        command.function(line, self.__shared)

    def help(self, command: str, shared_dict: dict):
        gui_logger.info("### HELP ###")
        max_cmd_length: GuiCommand = max(
            self.__named_commands_registry.values(), key=lambda cmd: len(cmd.name)
        )
        max_length = len(max_cmd_length.name)
        for cmd in self.__named_commands_registry.values():
            gui_logger.info(f"- {cmd.name:>{max_length}} | {cmd.description}")


class CommandController:
    def __init__(self, initializer_config: InitializerConfig = None) -> None:
        self.__services: OrderedSet = OrderedSet()
        self.__named_commands_registry: SetOnceDictionary[str, Command] = SetOnceDictionary()
        self.__shared = InitializerConfig()

        if initializer_config is not None:
            self.__shared.__dict__.update(initializer_config)

    def register_command(self, command_name: str, function: Callable, reference_name: str = None,
                         meta: Dict = None) -> None:
        cmd = Command(
            full_name=command_name,
            function=function,
            ref_name=reference_name,
            meta=meta
        )
        self.__named_commands_registry[command_name] = cmd
        main_logger.info(f"Loaded command '{command_name}'")
        self._update_shared()

    def _update_shared(self):
        keys = list(self.__named_commands_registry.keys())
        loaded_commands_new = []
        for key in keys:
            if self.__named_commands_registry[key].ref_name is not None:
                loaded_commands_new.append(self.__named_commands_registry[key].ref_name)

        self.__shared.LOADED_COMMANDS = loaded_commands_new

    def list_commands(self, custom_only: bool = False):
        if custom_only:
            return [cmd.full_name for cmd in self.__named_commands_registry.values() if cmd.meta is not None]
        else:
            return list(self.__named_commands_registry.keys())

    def register_service(self, function: Callable):
        self.__services.add(function)

    def delete_command(self, command_name: str) -> None:
        self.__named_commands_registry.pop(command_name)
        self._update_shared()

    def export_commands(self):
        commands = []

        for command in self.__named_commands_registry.values():
            if command.meta is not None:
                commands.append(command.meta)

        data = {
            "commands": commands
        }

        return data

    def get_command(self, command_name: str):
        return self.__named_commands_registry.get(command_name)

    def process_line(self, logline: LogLine):
        for task in self.__services:
            task(logline, self.__shared)

        command_name = logline.prompt.strip().split(" ")[0].lower()

        command: Optional[Command] = self.__named_commands_registry.get(command_name, None)
        if command is None:
            return
        handler = command.function

        cleaned_prompt = logline.prompt.removeprefix(command_name).strip()

        logline = LogLine(cleaned_prompt, logline.username, logline.is_team_message, logline.player)

        log_gui_model_message(command_name.upper(), logline.username, logline.prompt)
        try:
            result = handler(logline, self.__shared)
            if result:
                log_gui_model_message(command_name.upper(), logline.username, result)
        except Exception as e:
            log_gui_model_message(command_name.upper(), logline.username, f"Error occurred: [{e}]")
