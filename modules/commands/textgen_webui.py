from modules.api.llm.textgen_webui import TextGenerationWebUILLMProvider
from modules.commands.base import QuickQueryLLMCommand, GlobalChatLLMCommand, PrivateChatLLMCommand
from config import config


class TextgenWebUIQuickQueryCommand(QuickQueryLLMCommand):
    provider = TextGenerationWebUILLMProvider
    settings = config.CUSTOM_MODEL_SETTINGS


class TextgenWebUIGlobalChatCommand(GlobalChatLLMCommand):
    provider = TextGenerationWebUILLMProvider
    settings = config.CUSTOM_MODEL_SETTINGS


class TextgenWebUIPrivateChatCommand(PrivateChatLLMCommand):
    provider = TextGenerationWebUILLMProvider
    settings = config.CUSTOM_MODEL_SETTINGS
