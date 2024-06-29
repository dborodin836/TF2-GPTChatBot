import random
import time

from config import RTDModes, config
from modules.command_controllers import InitializerConfig
from modules.logs import log_gui_general_message, main_logger
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import GameChatMessage

RICKROLL_LINK = "youtu.be/dQw4w9WgXcQ"


def handle_rtd(logline: GameChatMessage, shared_dict: InitializerConfig) -> None:
    """
    Handles the RTD (Roll The Dice) command for the given username.
    If RTD_MODE is set to RICKROLL, the user is rickrolled.
    If RTD_MODE is set to RANDOM_MEME, a random link for a meme is chosen from a file.
    """
    if config.RTD_MODE == RTDModes.RICKROLL.value:
        time.sleep(1)
        send_say_command_to_tf2(f"[RTD] {logline.username} rolled: {RICKROLL_LINK}")
    elif config.RTD_MODE == RTDModes.RANDOM_MEME.value:
        try:
            with open("vids.txt", "r") as file:
                # Reads all lines and removes 'https://'
                lines = list(map(lambda x: x.removeprefix("https://").strip(), file.readlines()))
        except Exception as e:
            main_logger.error(f"Failed to read 'vids.txt'. [{e}]")

        time.sleep(1)
        log_gui_general_message(f"[RTD] {logline.username} rolled: {random.choice(lines)}")
        send_say_command_to_tf2(
            f"[RTD] {logline.username} rolled: {random.choice(lines)}",
            is_team_chat=logline.is_team_message,
        )
