from typing import Callable, List, Optional
import enum
import pydantic
from ordered_set import OrderedSet
from pydantic import BaseModel, BaseConfig

from modules.conversation_history import ConversationHistory
from modules.logs import get_logger, log_gui_model_message
from modules.set_once_dict import SetOnceDictionary
from modules.typing import Command, LogLine, Player

main_logger = get_logger("main")
combo_logger = get_logger("combo")
gui_logger = get_logger("gui")

PRIVATE_CHAT_ID = "CMD_{0}_USR_{1}"
GLOBAL_CHAT_ID = "CMD_{0}"


class CommandChatTypes(enum.Enum):
    GLOBAL = 1
    PRIVATE = 2


class ChatHistoryManager(BaseModel):
    GLOBAL = ConversationHistory()
    COMMAND = {}

    def set_user_chat_history(self, player: Player, conv_history: ConversationHistory) -> None:
        attr_name = self._get_user_chat_history_attr_name(player.steamid64)
        setattr(self, attr_name, conv_history)

    def get_user_chat_history(self, player: Player) -> ConversationHistory:
        attr_name = self._get_user_chat_history_attr_name(player.steamid64)

        if hasattr(self, attr_name):
            return getattr(self, attr_name)
        else:
            main_logger.info(
                f"Conversation history for user '{player.name}' [{player.steamid64}] doesn't exist. Creating...")
            setattr(self, attr_name, ConversationHistory())
            return getattr(self, attr_name)

    def _get_user_chat_history_attr_name(self, id64: int) -> str:
        return f"USER_{id64}_CH"

    def get_or_create_command_chat_history(self, name: str, type_: CommandChatTypes, settings: dict = None, user: Player = None):
        if settings is None:
            settings = {}

        match type_:
            case CommandChatTypes.PRIVATE:
                if chat_history := self.COMMAND.get(name):
                    return chat_history
                main_logger.info(
                    f"Conversation history for command '{name}' [{type_}] doesn't exist. Creating...")
                combo_logger.trace(f'Creating chat history "{PRIVATE_CHAT_ID.format(name, user.steamid64)}"')
                new_ch = ConversationHistory(settings)
                self.COMMAND[PRIVATE_CHAT_ID.format(name, user.steamid64)] = new_ch
                return new_ch

            case CommandChatTypes.GLOBAL:
                if chat_history := self.COMMAND.get(name):
                    return chat_history
                main_logger.info(
                    f"Conversation history for command '{name}' [{type_}] doesn't exist. Creating...")
                new_ch = ConversationHistory(settings)
                self.COMMAND[GLOBAL_CHAT_ID.format(name)] = new_ch
                return new_ch

    def get_command_chat_history(self, name: str, type_: CommandChatTypes, user: Player = None):
        match type_:
            case CommandChatTypes.PRIVATE:
                if user is None:
                    raise Exception('User argument must be provided for private chat retrieval.')
                combo_logger.trace(PRIVATE_CHAT_ID.format(name, user.steamid64))
                if chat_history := self.COMMAND.get(PRIVATE_CHAT_ID.format(name, user.steamid64)):
                    return chat_history
                raise Exception('Command with this name not found.')

            case CommandChatTypes.GLOBAL:
                combo_logger.trace(GLOBAL_CHAT_ID.format(name))
                if chat_history := self.COMMAND.get(GLOBAL_CHAT_ID.format(name)):
                    return chat_history
                raise Exception('Command with this name not found.')

    def set_command_chat_history(self, name: str, type_: CommandChatTypes, chat_history: ConversationHistory,
                                 user: Player = None):
        match type_:
            case CommandChatTypes.PRIVATE:
                self.COMMAND[PRIVATE_CHAT_ID.format(name, user.steamid64)] = chat_history

            case CommandChatTypes.GLOBAL:
                self.COMMAND[GLOBAL_CHAT_ID.format(name)] = chat_history

    class Config(BaseConfig):
        extra = "allow"
        arbitrary_types_allowed = "allow"


class InitializerConfig(BaseModel):
    CHAT_CONVERSATION_HISTORY: ChatHistoryManager = pydantic.Field(default_factory=ChatHistoryManager)
    LOADED_COMMANDS: List[str] = []


class GuiCommandController:
    def __init__(self, initializer_config: dict = None, disable_help: bool = False) -> None:
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
        for command in self.__named_commands_registry.values():
            gui_logger.info(f"- {command.name:>{max_length}} | {command.description}")


class CommandController:
    def __init__(self, initializer_config: InitializerConfig = None) -> None:
        self.__services = OrderedSet()
        self.__named_commands_registry: SetOnceDictionary[
            str, Callable[[LogLine, InitializerConfig], Optional[str]]] = SetOnceDictionary()
        self.__shared = InitializerConfig()

        if initializer_config is not None:
            self.__shared.__dict__.update(initializer_config)

    def register_command(self, cmd: str, function: Callable, name: str = None) -> None:
        if name is not None:
            self.__shared.LOADED_COMMANDS.append(name)
        self.__named_commands_registry[cmd] = function

    def register_service(self, function: Callable):
        self.__services.add(function)

    def process_line(self, logline: LogLine):
        for task in self.__services:
            task(logline, self.__shared)

        command_name = logline.prompt.strip().split(" ")[0].lower()

        handler: Optional[Callable] = self.__named_commands_registry.get(command_name, None)
        if handler is None:
            return

        cleaned_prompt = logline.prompt.removeprefix(command_name).strip()

        logline = LogLine(cleaned_prompt, logline.username, logline.is_team_message, logline.player)

        log_gui_model_message(command_name.upper(), logline.username, logline.prompt)
        # try:
        result = handler(logline, self.__shared)
        #     if result:
        #         log_gui_model_message(command_name.upper(), logline.username, result)
        # except Exception as e:
        #     log_gui_model_message(command_name.upper(), logline.username, f"Error occurred: [{e}]")
