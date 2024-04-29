from config import config
from modules.api.groq import GroqCloudLLMProvider
from modules.commands.base import QuickQueryCommand, GlobalChatCommand, PrivateChatCommand
from modules.logs import get_logger

main_logger = get_logger('main')


class GroqQuickQueryCommand(QuickQueryCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL


class GroqGlobalChatCommand(GlobalChatCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL


class GroqPrivateChatCommand(PrivateChatCommand):
    provider = GroqCloudLLMProvider
    model = config.GROQ_MODEL
