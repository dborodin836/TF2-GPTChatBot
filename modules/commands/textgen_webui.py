from modules.api.textgen_webui import TextGenerationWebUILLMProvider
from modules.logs import get_logger
from modules.commands.base import QuickQueryCommand, GlobalChatCommand, PrivateChatCommand

main_logger = get_logger("main")

DUMMY_MODEL_NAME = 'CUSTOM'


class TextgenWebUIQuickQueryCommand(QuickQueryCommand):
    provider = TextGenerationWebUILLMProvider
    model = DUMMY_MODEL_NAME


class TextgenWebUIGlobalChatCommand(GlobalChatCommand):
    provider = TextGenerationWebUILLMProvider
    model = DUMMY_MODEL_NAME


class TextgenWebUIPrivateChatCommand(PrivateChatCommand):
    provider = TextGenerationWebUILLMProvider
    model = DUMMY_MODEL_NAME
