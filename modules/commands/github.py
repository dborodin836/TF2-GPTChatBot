import time

from config import config
from modules.command_controllers import InitializerConfig
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine
from modules.utils.text import get_shortened_username

GITHUB_LINK = "bit.ly/tf2-gpt3"


def handle_gh_command(logline: LogLine, shared_dict: InitializerConfig) -> None:
    time.sleep(1)

    if config.ENABLE_SHORTENED_USERNAMES_RESPONSE:
        msg = f"{get_shortened_username(logline.username)}GitHub: {GITHUB_LINK}"
    else:
        msg = f"GitHub: {GITHUB_LINK}"

    send_say_command_to_tf2(msg, is_team_chat=logline.is_team_message)
