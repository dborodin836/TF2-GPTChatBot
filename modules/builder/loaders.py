from abc import ABC
from typing import Callable, Dict

from modules.api.llm.groq import GroqCloudLLMProvider
from modules.api.llm.openai import OpenAILLMProvider
from modules.api.llm.textgen_webui import TextGenerationWebUILLMProvider
from modules.commands.decorators import (
    admin_only,
    blacklist_factory,
    deny_empty_prompt,
    disabled,
    empty_prompt_message_response,
    openai_moderated,
    whitelist_factory,
)
from modules.commands.llm import (
    CommandGlobalChatLLMChatCommand,
    CommandPrivateChatLLMChatCommand,
    ConfirmableQuickQueryLLMCommand,
    QuickQueryLLMCommand,
)
from modules.commands.rcon import RconCommand
from modules.commands.tts import TTSCommand
from modules.logs import get_logger
from modules.typing import CommandSchemaDefinition

main_logger = get_logger("main")
gui_logger = get_logger("gui")

LLM_COMMAND_SETTINGS = {
    "prompt-file",
    "enable-soft-limit",
    "soft-limit-length",
    "message-suffix",
    "greeting",
    "allow-prompt-overwrite",
    "allow-long",
    "enable-hard-limit",
    "hard-limit-length",
    "allow-img",
    "img-detail",
    "img-screen-id",
}

# Traits
WRAPPERS: Dict[str, Callable] = {
    "openai-moderated": openai_moderated,
    "admin-only": admin_only,
    "empty-prompt-message-response": empty_prompt_message_response,
    "disabled": disabled,
    "deny-empty-prompt": deny_empty_prompt,
    "whitelist": whitelist_factory,
    "blacklist": blacklist_factory,
}

LLM_PROVIDERS = {
    "open-ai": OpenAILLMProvider,
    "groq-cloud": GroqCloudLLMProvider,
    "text-generation-webui": TextGenerationWebUILLMProvider,
}


class InvalidCommandException(Exception): ...


class Loader(ABC):
    def __init__(self, raw_data: dict) -> None:
        self.raw_command_data = raw_data
        self.command_data: Dict = {}

    def get_data(self) -> dict:
        self.__load_settings()

        return self.command_data

    def __load_settings(self):
        if command_settings := self.raw_command_data.get("settings"):
            # Verify for unknown keys
            for option in command_settings.keys():
                if option not in COMMAND_TYPES.get(self.raw_command_data["type"]).settings:
                    gui_logger.warning(f'"{option}" is not a valid option.')
            # Update dict
            self.command_data.update(settings=command_settings)


class LLMCommandLoader(Loader):
    def get_data(self) -> dict:
        super().get_data()
        self.__load_provider()
        self.__load_model()
        self.__load_model_settings()

        return self.command_data

    def __load_provider(self):
        try:
            provider = LLM_PROVIDERS[self.raw_command_data["provider"]]
            self.command_data.update(provider=provider)
        except Exception:
            raise InvalidCommandException(
                f"Command type is invalid or missing. Expected one of {list(LLM_PROVIDERS.keys())}"
            )

    def __load_model(self):
        if self.raw_command_data["provider"] == "text-generation-webui":
            return None

        try:
            model = self.raw_command_data["model"]
            self.command_data.update(model=model)
        except Exception:
            raise InvalidCommandException("Model name is invalid or missing.")

    def __load_model_settings(self):
        if model_settings := self.raw_command_data.get("model_settings"):
            self.command_data.update(model_settings=model_settings)


class RCONCommandLoader(Loader):
    def get_data(self) -> dict:
        super().get_data()
        self.__load_rcon_command()

        return self.command_data

    def __load_rcon_command(self):
        try:
            cmd = self.raw_command_data["command"]
            self.command_data.update(command=cmd)
        except Exception:
            raise InvalidCommandException("RCON command name is invalid or missing.")


COMMAND_TYPES: Dict[str, CommandSchemaDefinition] = {
    "quick-query": CommandSchemaDefinition(
        klass=QuickQueryLLMCommand, loader=LLMCommandLoader, settings=LLM_COMMAND_SETTINGS
    ),
    "command-private": CommandSchemaDefinition(
        klass=CommandPrivateChatLLMChatCommand,
        loader=LLMCommandLoader,
        settings=LLM_COMMAND_SETTINGS,
    ),
    "command-global": CommandSchemaDefinition(
        klass=CommandGlobalChatLLMChatCommand,
        loader=LLMCommandLoader,
        settings=LLM_COMMAND_SETTINGS,
    ),
    "rcon": CommandSchemaDefinition(
        klass=RconCommand, loader=RCONCommandLoader, settings={"wait-ms"}
    ),
    "openai-tts": CommandSchemaDefinition(
        klass=TTSCommand,
        loader=Loader,
        settings={"model", "voice", "speed", "volume", "output_device"},
    ),
    "confirmable-quick-query": CommandSchemaDefinition(
        klass=ConfirmableQuickQueryLLMCommand,
        loader=LLMCommandLoader,
        settings=LLM_COMMAND_SETTINGS,
    ),
}
