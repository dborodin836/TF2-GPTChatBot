import time
from typing import Callable, List

from modules.api.llm.openai import is_flagged
from modules.command_controllers import InitializerConfig
from modules.logs import get_logger
from modules.permissions import is_admin
from modules.servers.tf2 import format_say_message, send_say_command_to_tf2
from modules.typing import LogLine, Player

gui_logger = get_logger("gui")


def empty_prompt_wrapper_handler_factory(handler: Callable):
    def decorator(func):
        def wrapper(logline: LogLine, shared_dict: InitializerConfig):
            if logline.prompt == "":
                handler(logline, shared_dict)
                return None
            return func(logline, shared_dict)

        return wrapper

    return decorator


def empty_prompt_message_response(msg: str):
    def decorator(func):
        def wrapper(logline: LogLine, shared_dict: InitializerConfig):
            if logline.prompt == "":
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
        raise Exception("User is not admin.")

    return wrapper


def openai_moderated(func):
    def wrapper(logline: LogLine, shared_dict: InitializerConfig):
        if is_flagged(logline.prompt) and not is_admin(logline.player):
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


def deny_empty_prompt(func):
    def wrapper(logline: LogLine, shared_dict: InitializerConfig):
        if logline.prompt.strip() == "":
            raise Exception("Prompt is empty. Skipping...")

        return func(logline, shared_dict)

    return wrapper


def disabled(func):
    def wrapper(logline: LogLine, shared_dict: InitializerConfig):
        raise Exception("This command is disabled.")

    return wrapper
