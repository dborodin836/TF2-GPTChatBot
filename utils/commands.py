import random
import time
from config import config, RTDModes
from services.network import send_say_command_to_tf2
from utils.logs import log_cmd_message

BOT_RUNNING = True
RICKROLL_LINK = "youtu.be/dQw4w9WgXcQ"
GITHUB_LINK = "bit.ly/tf2-gpt3"


def handle_gh_command(username: str, is_team: bool = False) -> None:
    log_cmd_message(f"User '{username}' GET GH LINK")
    time.sleep(1)
    send_say_command_to_tf2(f"GitHub: {GITHUB_LINK}", is_team)


def handle_rtd_command(username: str, is_team: bool = False) -> None:
    """
    Handles the RTD (Roll The Dice) command for the given username.
    If RTD_MODE is set to RICKROLL, the user is rickrolled.
    If RTD_MODE is set to RANDOM_MEME, a random link for a meme is chosen from a file.
    """
    if config.RTD_MODE == RTDModes.RICKROLL.value:
        log_cmd_message("RICKROLLED!!11!!")
        time.sleep(1)
        send_say_command_to_tf2(f"[RTD] {username} rolled: {RICKROLL_LINK}")
    elif config.RTD_MODE == RTDModes.RANDOM_MEME.value:
        with open('vids.txt', 'r') as file:
            # Reads all lines and removes 'https://'
            lines = list(map(lambda x: x.removeprefix('https://').strip(), file.readlines()))
        time.sleep(1)
        log_cmd_message(f"[RTD] {username} rolled: {random.choice(lines)}")
        send_say_command_to_tf2(f"[RTD] {username} rolled: {random.choice(lines)}", is_team)


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
