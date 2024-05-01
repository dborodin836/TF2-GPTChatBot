from config import config
from modules.api.llm.groq import GroqCloudLLMProvider
from modules.commands.base import QuickQueryLLMCommand, GlobalChatLLMCommand, PrivateChatLLMCommand


class GroqQuickQueryCommand(QuickQueryLLMCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
    settings = config.GROQ_SETTINGS


class GroqGlobalChatCommand(GlobalChatLLMCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
    settings = config.GROQ_SETTINGS


class GroqPrivateChatCommand(PrivateChatLLMCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
    settings = config.GROQ_SETTINGS
