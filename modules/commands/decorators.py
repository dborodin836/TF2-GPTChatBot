from typing import Callable, List

from config import config
from modules.api.openai import is_violated_tos
from modules.command_controllers import InitializerConfig
from modules.permissions import is_admin
from modules.typing import LogLine, Player
from modules.logs import get_logger

gui_logger = get_logger('gui')


def empty_prompt_wrapper_handler_factory(handler: Callable):
    def decorator(func):
        def wrapper(logline: LogLine, shared_dict: InitializerConfig):
            if logline.prompt == '':
                handler(logline, shared_dict)
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


def openai_moderated_message(func):
    def wrapper(logline: LogLine, shared_dict: InitializerConfig):
        if (
                not config.TOS_VIOLATION
                and is_violated_tos(logline.prompt)
                and not is_admin(logline.player)
        ):
            gui_logger.warning(
                f"Request '{logline.prompt}' by user '{logline.username}' violates OPENAI TOS. Skipping..."
            )
            return None

        return func(logline, shared_dict)

    return wrapper


def permission_decorator_factory(permissions_funcs: List[Callable[[Player], bool]]):
    def permissions_decorator(func):
        def wrapper(logline: LogLine, shared_dict: InitializerConfig):
            if all(map(lambda x: x(logline.player), permissions_funcs)):
                return func(logline, shared_dict)
            return None

        return wrapper

    return permissions_decorator
