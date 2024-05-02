from modules.api.llm.textgen_webui import TextGenerationWebUILLMProvider
from modules.commands.base import QuickQueryLLMCommand, GlobalChatLLMChatCommand, PrivateChatLLMChatCommand
from config import config


class TextgenWebUIQuickQueryCommand(QuickQueryLLMCommand):
    provider = TextGenerationWebUILLMProvider
    model_settings = config.CUSTOM_MODEL_SETTINGS


class TextgenWebUIGlobalChatCommand(GlobalChatLLMChatCommand):
    provider = TextGenerationWebUILLMProvider
    model_settings = config.CUSTOM_MODEL_SETTINGS


class TextgenWebUIPrivateChatCommand(PrivateChatLLMChatCommand):
    provider = TextGenerationWebUILLMProvider
    model_settings = config.CUSTOM_MODEL_SETTINGS
