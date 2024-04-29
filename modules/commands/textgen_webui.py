from modules.api.textgen_webui import TextGenerationWebUILLMProvider
from modules.commands.base import QuickQueryLLMCommand, GlobalChatLLMCommand, PrivateChatLLMCommand


class TextgenWebUIQuickQueryCommand(QuickQueryLLMCommand):
    provider = TextGenerationWebUILLMProvider


class TextgenWebUIGlobalChatCommand(GlobalChatLLMCommand):
    provider = TextGenerationWebUILLMProvider


class TextgenWebUIPrivateChatCommand(PrivateChatLLMCommand):
    provider = TextGenerationWebUILLMProvider
