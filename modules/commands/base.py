from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from modules.command_controllers import InitializerConfig
from modules.logs import get_logger
from modules.typing import GameChatMessage

main_logger = get_logger("main")
gui_logger = get_logger("gui")


class BaseCommand(ABC):
    name: str
    settings: Dict[str, Any] = {}
    wrappers: List[Callable] = []

    @classmethod
    @abstractmethod
    def get_handler(cls): ...

    @classmethod
    def as_command(cls) -> Callable[[GameChatMessage, InitializerConfig], None]:
        func = cls.get_handler()

        for decorator in cls.wrappers:
            func = decorator(func)

        return func
