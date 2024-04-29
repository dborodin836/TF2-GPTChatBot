import time

from config import config
from modules.api.openai import OpenAILLMProvider
from modules.command_controllers import InitializerConfig
from modules.logs import get_logger, log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine
from modules.commands.base import GlobalChatCommand, PrivateChatCommand

main_logger = get_logger("main")


def handle_gpt3(logline: LogLine, shared_dict: InitializerConfig) -> None:
    if logline.prompt == "":
        time.sleep(1)
        send_say_command_to_tf2(
            "Hello there! I am ChatGPT, a ChatGPT plugin integrated into"
            " Team Fortress 2. Ask me anything!",
            username=None,
            is_team_chat=logline.is_team_message,
        )
        log_gui_model_message(config.GPT3_MODEL, logline.username, logline.prompt.strip())
        main_logger.info(f"Empty '{config.GPT_COMMAND}' command from user '{logline.username}'.")
        return

    OpenAILLMProvider.get_quick_query_completion(
        logline.username,
        logline.prompt,
        model=config.GPT3_MODEL,
        is_team_chat=logline.is_team_message,
    )


class OpenAIPrivateChatCommand(PrivateChatCommand):
    provider = OpenAILLMProvider
    model = config.GPT3_CHAT_MODEL


class OpenAIGlobalChatCommand(GlobalChatCommand):
    provider = OpenAILLMProvider
    model = config.GPT3_CHAT_MODEL


def handle_gpt4(logline: LogLine, shared_dict: InitializerConfig):
    if (
            config.GPT4_ADMIN_ONLY
            and config.HOST_USERNAME == logline.username
            or not config.GPT4_ADMIN_ONLY
    ):
        OpenAILLMProvider.get_quick_query_completion(
            logline.username,
            logline.prompt,
            model=config.GPT4_MODEL,
            is_team_chat=logline.is_team_message,
        )


def handle_gpt4l(logline: LogLine, shared_dict: InitializerConfig):
    if (
            config.GPT4_ADMIN_ONLY
            and config.HOST_USERNAME == logline.username
            or not config.GPT4_ADMIN_ONLY
    ):
        OpenAILLMProvider.get_quick_query_completion(
            logline.username,
            logline.prompt,
            model=config.GPT4L_MODEL,
            is_team_chat=logline.is_team_message,
        )
