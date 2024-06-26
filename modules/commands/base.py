from abc import ABC, abstractmethod
from typing import Callable, List

from modules.command_controllers import InitializerConfig
from modules.logs import get_logger
from modules.typing import LogLine

main_logger = get_logger("main")
gui_logger = get_logger("gui")


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
