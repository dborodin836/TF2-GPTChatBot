from typing import Callable, List

from config import config
from modules.command_controllers import InitializerConfig
from modules.permissions import is_admin
from modules.typing import LogLine, Player


def empty_prompt_wrapper_handler_factory(handler: Callable):
    def decorator(func):
        def wrapper(logline: LogLine, shared_dict: InitializerConfig):
            if logline.prompt == '':
                handler()
                return None
            return func(logline, shared_dict)

        return wrapper

    return decorator


def gpt4_admin_only(func):
    def wrapper(logline: LogLine, shared_dict: InitializerConfig):
        if (
            config.GPT4_ADMIN_ONLY
            and is_admin(logline.player)
            or not config.GPT4_ADMIN_ONLY
        ):
            return func(logline, shared_dict)
        return None

    return wrapper


def permission_decorator_factory(permissions_funcs: List[Callable[[Player], bool]]):
    def permissions_decorator(func):
        def wrapper(logline: LogLine, shared_dict: InitializerConfig):
            if all(map(lambda x: x(logline.player), permissions_funcs)):
                return func(logline, shared_dict)
            return None

        return wrapper

    return permissions_decorator
