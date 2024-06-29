from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List

from modules.command_controllers import InitializerConfig
from modules.typing import GameChatMessage


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
