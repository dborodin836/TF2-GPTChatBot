from config import config
from modules.api.llm.groq import GroqCloudLLMProvider
from modules.commands.base import QuickQueryLLMCommand, GlobalChatLLMChatCommand, PrivateChatLLMChatCommand


class GroqQuickQueryCommand(QuickQueryLLMCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
    model_settings = config.GROQ_SETTINGS


class GroqGlobalChatCommand(GlobalChatLLMChatCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
    model_settings = config.GROQ_SETTINGS


class GroqPrivateChatCommand(PrivateChatLLMChatCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
    model_settings = config.GROQ_SETTINGS