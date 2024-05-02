import time
from typing import Callable, List

from config import config
from modules.api.llm.openai import is_flagged
from modules.command_controllers import InitializerConfig
from modules.permissions import is_admin
from modules.servers.tf2 import format_say_message, send_say_command_to_tf2
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


def empty_prompt_message_response(msg: str):
    def decorator(func):
        def wrapper(logline: LogLine, shared_dict: InitializerConfig):
            if logline.prompt == '':
                time.sleep(1)
                message = format_say_message(msg, logline.username)
                send_say_command_to_tf2(
                    message,
                    username=None,
                    is_team_chat=logline.is_team_message,
                )
                return None
            return func(logline, shared_dict)

        return wrapper

    return decorator


def admin_only(func):
    def wrapper(logline: LogLine, shared_dict: InitializerConfig):
        if is_admin(logline.player):
            return func(logline, shared_dict)
        raise Exception('User is not admin.')

    return wrapper


def gpt4_admin_only(func):
    def wrapper(logline: LogLine, shared_dict: InitializerConfig):
        if (
                config.GPT4_ADMIN_ONLY
                and is_admin(logline.player)
                or not config.GPT4_ADMIN_ONLY
        ):
            return func(logline, shared_dict)
        raise Exception('User is not admin.')

    return wrapper


def openai_moderated(func):
    def wrapper(logline: LogLine, shared_dict: InitializerConfig):
        if (
                not config.TOS_VIOLATION
                and is_flagged(logline.prompt)
                and not is_admin(logline.player)
        ):
            raise Exception("Request was flagged during moderation. Skipping...")

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


def disabled(func):
    def wrapper(logline: LogLine, shared_dict: InitializerConfig):
        raise Exception("This command is disabled.")

    return wrapper
