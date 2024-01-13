import time

from config import config
from modules.api.openai import handle_cgpt_request, handle_gpt_request
from modules.logs import get_logger, log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine

main_logger = get_logger("main")


def handle_gpt3(logline: LogLine, shared_dict: dict) -> None:
    if logline.prompt.removeprefix(config.GPT_COMMAND).strip() == "":
        time.sleep(1)
        send_say_command_to_tf2(
            "Hello there! I am ChatGPT, a ChatGPT plugin integrated into"
            " Team Fortress 2. Ask me anything!",
            username=None,
            is_team_chat=logline.is_team_message,
        )
        log_gui_model_message("gpt-3.5-turbo", logline.username, logline.prompt.strip())
        main_logger.info(f"Empty '{config.GPT_COMMAND}' command from user '{logline.username}'.")
        return

    main_logger.info(
        f"'{config.GPT_COMMAND}' command from user '{logline.username}'. "
        f"Message: '{logline.prompt.removeprefix(config.GPT_COMMAND).strip()}'"
    )
    handle_gpt_request(
        logline.username,
        logline.prompt.removeprefix(config.GPT_COMMAND).strip(),
        model="gpt-3.5-turbo",
        is_team_chat=logline.is_team_message,
    )


def handle_cgpt(logline: LogLine, shared_dict: dict):
    conv_his = handle_cgpt_request(
        logline.username,
        logline.prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
        shared_dict["CHAT_CONVERSATION_HISTORY"],
        is_team=logline.is_team_message,
        model="gpt-3.5-turbo",
    )
    shared_dict.update({"CHAT_CONVERSATION_HISTORY": conv_his})


def handle_gpt4(logline: LogLine, shared_dict: dict):
    if (
        config.GPT4_ADMIN_ONLY
        and config.HOST_USERNAME == logline.username
        or not config.GPT4_ADMIN_ONLY
    ):
        handle_gpt_request(
            logline.username,
            logline.prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
            model="gpt-4-1106-preview",
            is_team_chat=logline.is_team_message,
        )


def handle_gpt4l(logline: LogLine, shared_dict: dict):
    if (
        config.GPT4_ADMIN_ONLY
        and config.HOST_USERNAME == logline.username
        or not config.GPT4_ADMIN_ONLY
    ):
        handle_gpt_request(
            logline.username,
            logline.prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
            model="gpt-4",
            is_team_chat=logline.is_team_message,
        )
