from config import config
from modules.api.llm.groq import GroqCloudLLMProvider
from modules.commands.base import QuickQueryLLMCommand, GlobalChatChatLLMCommand, PrivateChatChatLLMCommand


class GroqQuickQueryCommand(QuickQueryLLMCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
    model_settings = config.GROQ_SETTINGS


class GroqGlobalChatCommand(GlobalChatChatLLMCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
    model_settings = config.GROQ_SETTINGS


class GroqPrivateChatCommand(PrivateChatChatLLMCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
    model_settings = config.GROQ_SETTINGS
