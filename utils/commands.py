import random
import time

import requests

from config import RTDModes, config
from services.source_game import send_say_command_to_tf2
from utils.logs import get_logger, log_gui_general_message, log_gui_model_message
from utils.text import get_shortened_username, add_prompts_by_flags
from utils.types import MessageHistory, Message

RICKROLL_LINK = "youtu.be/dQw4w9WgXcQ"
GITHUB_LINK = "bit.ly/tf2-gpt3"

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")


def handle_gh_command(username: str, is_team: bool = False) -> None:
    log_gui_general_message(f"User '{username}' GET GH LINK")
    time.sleep(1)

    if config.ENABLE_SHORTENED_USERNAMES_RESPONSE:
        msg = f"{get_shortened_username(username)}GitHub: {GITHUB_LINK}"
    else:
        msg = f"GitHub: {GITHUB_LINK}"

    send_say_command_to_tf2(msg, is_team_chat=is_team)


def handle_rtd_command(username: str, is_team: bool = False) -> None:
    """
    Handles the RTD (Roll The Dice) command for the given username.
    If RTD_MODE is set to RICKROLL, the user is rickrolled.
    If RTD_MODE is set to RANDOM_MEME, a random link for a meme is chosen from a file.
    """
    if config.RTD_MODE == RTDModes.RICKROLL.value:
        log_gui_general_message("RICKROLLED!!11!!")
        time.sleep(1)
        send_say_command_to_tf2(f"[RTD] {username} rolled: {RICKROLL_LINK}")
    elif config.RTD_MODE == RTDModes.RANDOM_MEME.value:
        try:
            with open("vids.txt", "r") as file:
                # Reads all lines and removes 'https://'
                lines = list(map(lambda x: x.removeprefix("https://").strip(), file.readlines()))
        except Exception as e:
            main_logger.error(f"Failed to read 'vids.txt'. [{e}]")

        time.sleep(1)
        log_gui_general_message(f"[RTD] {username} rolled: {random.choice(lines)}")
        send_say_command_to_tf2(f"[RTD] {username} rolled: {random.choice(lines)}", is_team_chat=is_team)


def print_help_command():
    """
    Prints the available commands and their descriptions.
    """
    gui_logger.info(
        "### HELP ###",
        "start - start the bot",
        "stop - stop the bot",
        "quit - quit the program",
        "bans - show all banned players",
        "ban <username> - ban user by username",
        "unban <username> - unban user by username",
        "gpt3 <prompt> - sends a response to GPT3",
        sep="\n",
    )


def get_custom_model_response(conversation_history: list[Message]) -> str | None:
    uri = f"http://{config.CUSTOM_MODEL_HOST}/v1/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "mode": "chat",
        "messages": conversation_history
    }

    try:
        response = requests.post(uri, headers=headers, json=data, verify=False)
    except Exception as e:
        combo_logger.error(f"Failed to get response from the text-generation-webui server. [{e}]")
        return

    if response.status_code == 200:
        try:
            data = response.json()['choices'][0]['message']['content']
            return data
        except Exception as e:
            combo_logger.error(f"Failed to parse data from server [{e}].")
    elif response.status_code == 500:
        combo_logger.error(f"There's error on the text-generation-webui server. [HTTP 500]")

    return None


def handle_custom_model_command(
        username: str,
        user_prompt: str,
        is_team: bool = False
) -> None:
    log_gui_model_message("CUSTOM", username, user_prompt.strip())

    message = add_prompts_by_flags(user_prompt)

    response = get_custom_model_response([{"role": "user", "content": message}, ])

    if response:
        log_gui_model_message("CUSTOM", username, response.strip())
        send_say_command_to_tf2(response, username, is_team)


def handle_custom_model_chat_command(
        username: str,
        user_prompt: str,
        conversation_history: MessageHistory,
        is_team: bool = False
) -> MessageHistory:
    log_gui_model_message("CUSTOM CHAT", username, user_prompt.strip())

    message = add_prompts_by_flags(user_prompt)
    conversation_history.append({"role": "user", "content": message})
    response = get_custom_model_response(conversation_history)

    if response:
        conversation_history.append({"role": "assistant", "content": response})
        log_gui_model_message("CUSTOM CHAT", username, response.strip())
        send_say_command_to_tf2(response, username, is_team)

    return conversation_history
