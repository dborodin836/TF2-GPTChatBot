import random
import time
from enum import Enum

from config import RTD_MODE
from services.network import send_say_command_to_tf2
from utils.logs import log_cmd_message

BOT_RUNNING = True
RICKROLL_LINK = "youtu.be/dQw4w9WgXcQ"


class RTDModes(Enum):
    DISABLED = 0
    RICKROLL = 1
    RANDOM_MEME = 2


def handle_rtd_command(username: str) -> None:
    """
    Handles the RTD (Roll The Dice) command for the given username.
    If RTD_MODE is set to RICKROLL, the user is rickrolled.
    If RTD_MODE is set to RANDOM_MEME, a random link for a meme is chosen from a file.
    """
    if RTD_MODE == RTDModes.RICKROLL:
        log_cmd_message("RICKROLLED!!11!!")
        time.sleep(1)
        send_say_command_to_tf2(f"[RTD] {username} rolled: {RICKROLL_LINK}")
    elif RTD_MODE == RTDModes.RANDOM_MEME:
        with open('vids.txt', 'r') as file:
            # Reads all lines and removes 'https://'
            lines = list(map(lambda x: x.removeprefix('https://').strip(), file.readlines()))
        time.sleep(1)
        send_say_command_to_tf2(f"[RTD] {username} rolled: {random.choice(lines)}")


def print_help_command():
    """
    Prints the available commands and their descriptions.
    """
    print("### HELP ###",
          "start - start the bot",
          "stop - stop the bot",
          "quit - quit the program",
          "bans - show all banned players",
          "ban <username> - ban user by username",
          "unban <username> - unban user by username",
          "gpt3 <prompt> - sends a response to GPT3",
          sep='\n')


def start_bot() -> None:
    global BOT_RUNNING
    BOT_RUNNING = True
    log_cmd_message("BOT STARTED")


def stop_bot() -> None:
    global BOT_RUNNING
    BOT_RUNNING = False
    log_cmd_message("BOT STOPPED")


def get_bot_state():
    return BOT_RUNNING
