from modules.api.textgen_webui import TextGenerationWebUILLMProvider
from modules.logs import get_logger
from modules.commands.base import QuickQueryLLMCommand, GlobalChatLLMCommand, PrivateChatLLMCommand

main_logger = get_logger("main")


class TextgenWebUIQuickQueryCommand(QuickQueryLLMCommand):
    provider = TextGenerationWebUILLMProvider


class TextgenWebUIGlobalChatCommand(GlobalChatLLMCommand):
    provider = TextGenerationWebUILLMProvider


class TextgenWebUIPrivateChatCommand(PrivateChatLLMCommand):
    provider = TextGenerationWebUILLMProvider
