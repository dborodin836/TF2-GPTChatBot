from typing import Callable, Optional

from ordered_set import OrderedSet

from modules.logs import get_logger, get_time_stamp
from modules.set_once_dict import SetOnceDictionary
from modules.typing import LogLine

combo_logger = get_logger("combo")


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

        combo_logger.info(
            f"[{get_time_stamp()}] -- '{command_name}' command from user '{logline.username}'."
        )
        handler(logline, self.__shared)
