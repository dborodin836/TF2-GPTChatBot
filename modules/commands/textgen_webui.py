from modules.api.llm.textgen_webui import TextGenerationWebUILLMProvider
from modules.commands.base import QuickQueryLLMCommand, GlobalChatChatLLMCommand, PrivateChatChatLLMCommand
from config import config


class TextgenWebUIQuickQueryCommand(QuickQueryLLMCommand):
    provider = TextGenerationWebUILLMProvider
    model_settings = config.CUSTOM_MODEL_SETTINGS


class TextgenWebUIGlobalChatCommand(GlobalChatChatLLMCommand):
    provider = TextGenerationWebUILLMProvider
    model_settings = config.CUSTOM_MODEL_SETTINGS


class TextgenWebUIPrivateChatCommand(PrivateChatChatLLMCommand):
    provider = TextGenerationWebUILLMProvider
    model_settings = config.CUSTOM_MODEL_SETTINGS
