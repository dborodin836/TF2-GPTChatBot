import os
import tempfile

import pytest

from modules.typing import Player
from modules.utils.steam import steamid3_to_steamid64


def raise_(ex):
    raise ex


def get_player(name: str, id: int) -> Player:
    return Player(
        name=name,
        minutes_on_server=0,
        last_updated=0,
        ping=1,
        steamid3=f"[U:1:{id}]",
        steamid64=steamid3_to_steamid64(f"[U:1:{id}]")
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
    ENABLE_STATS_LOGS = True
    SHORTENED_USERNAMES_FORMAT = "[$username] "
    SHORTENED_USERNAME_LENGTH = 12
    TF2_LOGFILE_PATH = "/"

    def __init__(
            self,
            app_version=None,
            soft_completion_limit=None,
            custom_prompt=None,
            host_username=None,
            clear_chat_command=None,
            fallback_to_username=None,
            enable_stats_logs=None,
            shortened_username_format=None,
            shortened_username_length=None,
            tf2_logfile_path=None
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
        if enable_stats_logs is not None:
            self.ENABLE_STATS_LOGS = enable_stats_logs
        if shortened_username_format is not None:
            self.SHORTENED_USERNAMES_FORMAT = shortened_username_format
        if shortened_username_length is not None:
            self.SHORTENED_USERNAME_LENGTH = shortened_username_length
        if tf2_logfile_path is not None:
            self.TF2_LOGFILE_PATH = tf2_logfile_path


@pytest.fixture
def temp_file():
    # Create a temporary file and get its name
    fd, path = tempfile.mkstemp()

    # Pre-test setup: Close the file descriptor as we don't need it
    os.close(fd)

    # Provide the temporary file path to the test
    yield path

    # Post-test teardown: Remove the temporary file
    os.remove(path)
