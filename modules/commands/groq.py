from config import config
from modules.api.groq import GroqCloudLLMProvider
from modules.commands.base import QuickQueryLLMCommand, GlobalChatLLMCommand, PrivateChatLLMCommand


class GroqQuickQueryCommand(QuickQueryLLMCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL


class GroqGlobalChatCommand(GlobalChatLLMCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL


class GroqPrivateChatCommand(PrivateChatLLMCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
