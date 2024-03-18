from modules.typing import Player


def raise_(ex):
    raise ex


def get_player(name: str, id: int) -> Player:
    return Player(
        name=name,
        minutes_on_server=0,
        last_updated=0,
        ping=1,
        steamid3=f"[U:1:{id}]"
    )


class MockConfig:
    APP_VERSION = "1.0.0"
    SOFT_COMPLETION_LIMIT = 128
    CUSTOM_PROMPT = ""
    GREETING = ""
    HOST_USERNAME = "admin"
    HOST_STEAMID3 = "[U:0:0]"
    CLEAR_CHAT_COMMAND = "!clear"
    FALLBACK_TO_USERNAME = True

    def __init__(
            self,
            app_version=None,
            soft_completion_limit=None,
            custom_prompt=None,
            host_username=None,
            clear_chat_command=None,
            fallback_to_username=None,
    ):
        if app_version is not None:
            self.APP_VERSION = app_version
        if soft_completion_limit is not None:
            self.SOFT_COMPLETION_LIMIT = soft_completion_limit
        if custom_prompt is not None:
            self.CUSTOM_PROMPT = custom_prompt
        if host_username is not None:
            self.HOST_USERNAME = host_username
        if clear_chat_command is not None:
            self.CLEAR_CHAT_COMMAND = clear_chat_command
        if fallback_to_username is not None:
            self.FALLBACK_TO_USERNAME = fallback_to_username
