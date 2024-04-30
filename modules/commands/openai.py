import time

from config import config
from modules.api.openai import OpenAILLMProvider
from modules.command_controllers import InitializerConfig
from modules.logs import get_logger
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine
from modules.commands.base import GlobalChatLLMCommand, PrivateChatLLMCommand, QuickQueryLLMCommand
from modules.commands.decorators import empty_prompt_wrapper_handler_factory, gpt4_admin_only, openai_moderated

main_logger = get_logger("main")


def handle_empty(logline: LogLine, shared_dict: InitializerConfig):
    time.sleep(1)
    send_say_command_to_tf2(
        "Hello there! I am ChatGPT, a ChatGPT plugin integrated into"
        " Team Fortress 2. Ask me anything!",
        username=None,
        is_team_chat=logline.is_team_message,
    )
    main_logger.info(f"Empty '{config.GPT_COMMAND}' command from user '{logline.username}'.")


class OpenAIGPT3QuickQueryCommand(QuickQueryLLMCommand):
    provider = OpenAILLMProvider
    model = config.GPT3_MODEL
    wrappers = [
        empty_prompt_wrapper_handler_factory(handle_empty),
        openai_moderated
    ]


class OpenAIPrivateChatCommand(PrivateChatLLMCommand):
    provider = OpenAILLMProvider
    model = config.GPT3_CHAT_MODEL
    wrappers = [
        openai_moderated
    ]


class OpenAIGlobalChatCommand(GlobalChatLLMCommand):
    provider = OpenAILLMProvider
    model = config.GPT3_CHAT_MODEL
    wrappers = [
        openai_moderated
    ]


class OpenAIGPT4QuickQueryCommand(QuickQueryLLMCommand):
    provider = OpenAILLMProvider
    model = config.GPT4_MODEL
    wrappers = [
        gpt4_admin_only,
        openai_moderated
    ]


class OpenAIGPT4LQuickQueryCommand(QuickQueryLLMCommand):
    provider = OpenAILLMProvider
    model = config.GPT4L_MODEL
    wrappers = [
        gpt4_admin_only,
        openai_moderated
    ]
