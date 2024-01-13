from typing import Callable, Optional

from ordered_set import OrderedSet

from modules.logs import get_logger, get_time_stamp
from modules.set_once_dict import SetOnceDictionary
from modules.typing import Command, LogLine

combo_logger = get_logger("combo")
gui_logger = get_logger("gui")


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
    def __init__(self, initializer_config: dict = None) -> None:
        self.__services = OrderedSet()
        self.__named_commands_registry: SetOnceDictionary[str, Callable] = SetOnceDictionary()
        self.__shared = dict()

        if initializer_config is not None:
            self.__shared.update(initializer_config)

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
