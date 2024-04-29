import time

from config import config
from modules.api.openai import OpenAILLMProvider
from modules.command_controllers import InitializerConfig
from modules.logs import get_logger, log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine
from modules.commands.base import GlobalChatCommand, PrivateChatCommand, QuickQueryCommand
from modules.commands.decorators import empty_prompt_wrapper_handler_factory, gpt4_admin_only, openai_moderated_message

main_logger = get_logger("main")


def handle_empty(logline: LogLine, shared_dict: InitializerConfig):
    time.sleep(1)
    send_say_command_to_tf2(
        "Hello there! I am ChatGPT, a ChatGPT plugin integrated into"
        " Team Fortress 2. Ask me anything!",
        username=None,
        is_team_chat=logline.is_team_message,
    )
    log_gui_model_message(config.GPT3_MODEL, logline.username, logline.prompt.strip())
    main_logger.info(f"Empty '{config.GPT_COMMAND}' command from user '{logline.username}'.")


class OpenAIGPT3QuickQueryCommand(QuickQueryCommand):
    provider = OpenAILLMProvider
    model = config.GPT3_MODEL
    wrappers = [
        empty_prompt_wrapper_handler_factory(handle_empty),
        openai_moderated_message
    ]


class OpenAIPrivateChatCommand(PrivateChatCommand):
    provider = OpenAILLMProvider
    model = config.GPT3_CHAT_MODEL
    wrappers = [
        openai_moderated_message
    ]


class OpenAIGlobalChatCommand(GlobalChatCommand):
    provider = OpenAILLMProvider
    model = config.GPT3_CHAT_MODEL
    wrappers = [
        openai_moderated_message
    ]


class OpenAIGPT4QuickQueryCommand(QuickQueryCommand):
    provider = OpenAILLMProvider
    model = config.GPT4_MODEL
    wrappers = [
        gpt4_admin_only,
        openai_moderated_message
    ]


class OpenAIGPT4LQuickQueryCommand(QuickQueryCommand):
    provider = OpenAILLMProvider
    model = config.GPT4L_MODEL
    wrappers = [
        gpt4_admin_only,
        openai_moderated_message
    ]
