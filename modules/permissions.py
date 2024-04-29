from typing import Callable, List

from config import config
from modules.command_controllers import InitializerConfig
from modules.typing import LogLine, Player


def is_admin(user: Player) -> bool:
    if config.HOST_STEAMID3 == user.steamid3:
        return True

    if not config.FALLBACK_TO_USERNAME:
        return False

    if config.HOST_USERNAME == user.name:
        return True

    return False


def permission_decorator_factory(permissions_funcs: List[Callable[[Player], bool]]):
    def permissions_decorator(func):
        def wrapper(logline: LogLine, shared_dict: InitializerConfig):
            if all(map(lambda x: x(logline.player), permissions_funcs)):
                return func(logline, shared_dict)
            return None

        return wrapper

    return permissions_decorator
