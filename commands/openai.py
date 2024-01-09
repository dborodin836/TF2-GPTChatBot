import time

from config import config
from services.chatgpt import handle_gpt_request, handle_cgpt_request
from services.source_game import send_say_command_to_tf2
from utils.logs import log_gui_model_message, get_logger
from utils.types import LogLine

main_logger = get_logger("main")


def gpt3_handler(logline: LogLine, **kwargs):
    if logline.prompt.removeprefix(config.GPT_COMMAND).strip() == "":
        time.sleep(1)
        send_say_command_to_tf2(
            "Hello there! I am ChatGPT, a ChatGPT plugin integrated into"
            " Team Fortress 2. Ask me anything!", username=None,
            is_team_chat=logline.is_team_message,
        )
        log_gui_model_message("gpt-3.5-turbo", logline.username, logline.prompt.strip())
        main_logger.info(f"Empty '{config.GPT_COMMAND}' command from user '{logline.username}'.")

    main_logger.info(f"'{config.GPT_COMMAND}' command from user '{logline.username}'. "
                     f"Message: '{logline.prompt.removeprefix(config.GPT_COMMAND).strip()}'")
    handle_gpt_request(
        logline.username,
        logline.prompt.removeprefix(config.GPT_COMMAND).strip(),
        model="gpt-3.5-turbo",
        is_team_chat=logline.is_team_message,
    )


def handle_cgpt(logline: LogLine, **kwargs):
    conv_his = handle_cgpt_request(
        logline.username,
        logline.prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
        kwargs["CHAT_CONVERSATION_HISTORY"],
        is_team=logline.is_team_message,
        model="gpt-3.5-turbo",
    )
    kwargs.update({"CHAT_CONVERSATION_HISTORY": conv_his})
    return kwargs


def h_gpt4(logline: LogLine, **kwargs):
    if config.GPT4_ADMIN_ONLY and config.HOST_USERNAME == logline.username or not config.GPT4_ADMIN_ONLY:
        handle_gpt_request(
            logline.username,
            logline.prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
            model="gpt-4-1106-preview",
            is_team_chat=logline.is_team_message,
        )


def h_gpt4l(logline: LogLine, **kwargs):
    if config.GPT4_ADMIN_ONLY and config.HOST_USERNAME == logline.username or not config.GPT4_ADMIN_ONLY:
        handle_gpt_request(
            logline.username,
            logline.prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
            model="gpt-4",
            is_team_chat=logline.is_team_message,
        )
