from modules.api.textgen_webui import TextGenerationWebUILLMProvider
from modules.logs import get_logger
from modules.commands.base import QuickQueryLLMCommand, GlobalChatLLMCommand, PrivateChatLLMCommand

main_logger = get_logger("main")

DUMMY_MODEL_NAME = 'CUSTOM'


class TextgenWebUIQuickQueryCommand(QuickQueryLLMCommand):
    provider = TextGenerationWebUILLMProvider
    model = DUMMY_MODEL_NAME


class TextgenWebUIGlobalChatCommand(GlobalChatLLMCommand):
    provider = TextGenerationWebUILLMProvider
    model = DUMMY_MODEL_NAME


class TextgenWebUIPrivateChatCommand(PrivateChatLLMCommand):
    provider = TextGenerationWebUILLMProvider
    model = DUMMY_MODEL_NAME
