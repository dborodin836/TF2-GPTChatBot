import os.path
from typing import Dict, List

import yaml

from modules.api.llm.groq import GroqCloudLLMProvider
from modules.api.llm.openai import OpenAILLMProvider
from modules.api.llm.textgen_webui import TextGenerationWebUILLMProvider
from modules.command_controllers import CommandController
from modules.commands.base import (
    BaseCommand,
    CommandGlobalChatLLMChatCommand,
    CommandPrivateChatLLMChatCommand,
    QuickQueryLLMCommand,
)
from modules.commands.decorators import (
    admin_only,
    deny_empty_prompt,
    disabled,
    empty_prompt_message_response,
    openai_moderated,
)
from modules.logs import get_logger

main_logger = get_logger("main")
gui_logger = get_logger("gui")


class InvalidCommandException(Exception): ...


TYPES = {
    "quick-query": QuickQueryLLMCommand,
    "command-private": CommandPrivateChatLLMChatCommand,
    "command-global": CommandGlobalChatLLMChatCommand,
}

PROVIDERS = {
    "open-ai": OpenAILLMProvider,
    "groq-cloud": GroqCloudLLMProvider,
    "text-generation-webui": TextGenerationWebUILLMProvider,
}

# Traits
WRAPPERS = {
    "openai-moderated": openai_moderated,
    "admin-only": admin_only,
    "empty-prompt-message-response": empty_prompt_message_response,
    "disabled": disabled,
    "deny-empty-prompt": deny_empty_prompt,
}

CHAT_SETTINGS = {
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
    "img-screen-id"
}


def get_commands_from_yaml() -> List[dict]:
    with open("commands.yaml", "r") as file:
        data = yaml.safe_load(file)

    return data["commands"]


def create_command_from_dict(cmd: dict) -> BaseCommand:
    command_dict: Dict = {}
    command_dict.update(name=cmd["name"])
    class_name = f"DynamicCommand{cmd['name']}"

    # Command type
    try:
        type_ = TYPES[cmd["type"]]
    except Exception as e:
        raise InvalidCommandException(
            f"Command type is invalid or missing. Expected one of {list(TYPES.keys())}"
        )

    # Provider type
    try:
        provider = PROVIDERS[cmd["provider"]]
        command_dict.update(provider=provider)
    except Exception as e:
        raise InvalidCommandException(
            f"Command type is invalid or missing. Expected one of {list(PROVIDERS.keys())}"
        )

    # Model
    if provider != PROVIDERS.get("text-generation-webui"):
        try:
            model = cmd["model"]
            command_dict.update(model=model)
        except Exception as e:
            raise InvalidCommandException("Model name is invalid or missing.")

    # Update command wrappers
    if traits := cmd.get("traits"):
        wrappers = []
        # Reverse the order to make it natural, to make wrappers applied from top to bottom in yaml file.
        for wrapper_obj in traits[::-1]:
            try:
                if isinstance(wrapper_obj, dict):
                    key = list(wrapper_obj)[0]
                    values = wrapper_obj[key]
                    factory = WRAPPERS[key]
                    wrappers.append(factory(**values))
                elif isinstance(wrapper_obj, str):
                    wrapper = WRAPPERS[wrapper_obj]
                    wrappers.append(wrapper)
            except Exception as e:
                gui_logger.warning(f"{e} is not a valid trait.")
        command_dict.update(wrappers=wrappers)

    # Update command settings
    if model_settings := cmd.get("model_settings"):
        command_dict.update(model_settings=model_settings)

    # Update command settings
    if chat_settings := cmd.get("settings"):
        # Verify for unknown keys
        for option in chat_settings.keys():
            if option not in CHAT_SETTINGS:
                gui_logger.warning(f'"{option}" is not a valid option.')
        # Update dict
        command_dict.update(chat_settings=chat_settings)

    return type(class_name, (type_,), command_dict)


def load_commands(controller: CommandController) -> None:
    if not os.path.exists("./commands.yaml"):
        main_logger.info("commands.yaml file is missing")
        return None

    try:
        commands = get_commands_from_yaml()
    except Exception as e:
        gui_logger.error(f"Failed to to load commands from yaml file. [{e}]")
        return None

    loaded_commands_count = 0
    errors_count = 0

    for cmd in commands:
        try:
            klass = create_command_from_dict(cmd)
            chat_command_name = cmd["prefix"] + cmd["name"]
            controller.register_command(chat_command_name, klass.as_command(), cmd["name"])
            loaded_commands_count += 1
        except Exception as e:
            errors_count += 1
            cmd_name = cmd.get("name", None)
            if cmd_name is None:
                gui_logger.error(f"Failed to load command. [{e}]")
            else:
                gui_logger.error(f'Failed to load command "{cmd_name}". [{e}]')

    gui_logger.info(f"Loaded {loaded_commands_count} command(s). ({errors_count} errors)")
