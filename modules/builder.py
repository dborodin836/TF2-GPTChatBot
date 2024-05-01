import enum
import os.path
from typing import List

import yaml

from modules.api.llm.groq import GroqCloudLLMProvider
from modules.api.llm.openai import OpenAILLMProvider
from modules.api.llm.textgen_webui import TextGenerationWebUILLMProvider

from modules.commands.base import LLMCommand, GlobalChatLLMCommand, PrivateChatLLMCommand, QuickQueryLLMCommand
from modules.commands.decorators import admin_only, openai_moderated, empty_prompt_message_response
from modules.logs import get_logger

main_logger = get_logger('main')
gui_logger = get_logger("gui")


class Types(enum.Enum):
    quick_query = QuickQueryLLMCommand
    global_chat = GlobalChatLLMCommand
    private_chat = PrivateChatLLMCommand


class Providers(enum.Enum):
    OpenAI = OpenAILLMProvider
    GroqCloud = GroqCloudLLMProvider
    TextGenerationWebUI = TextGenerationWebUILLMProvider


class Wrappers(enum.Enum):
    moderated = openai_moderated
    admin_only = admin_only
    empty_prompt_message_response = empty_prompt_message_response


def get_commands_from_yaml() -> List[dict]:
    with open('commands.yaml', 'r') as file:
        data = yaml.safe_load(file)

    return data['commands']


def create_command_from_dict(cmd: dict) -> LLMCommand:
    class_name = f"DynamicCommand"
    command_dict = {}

    # Command type
    try:
        type_ = getattr(Types, cmd['type']).value
    except Exception as e:
        raise Exception(f'Command type is invalid or missing. Expected one of {[type_.value for type_ in Types]}')

    # Provider type
    try:
        provider = getattr(Providers, cmd['provider']).value
    except Exception as e:
        raise Exception(
            f'Command type is invalid or missing. Expected one of {[provider.value for provider in Providers]}'
        )

    # Model
    try:
        model = cmd['model']
        command_dict.update(model=model)
    except Exception as e:
        raise Exception(f'Model name is invalid or missing.')

    # Update command wrappers
    if cmd.get('traits'):
        wrappers = []
        for item in cmd['traits']:
            if isinstance(item, dict):
                key = list(item)[0]
                values = item[key]
                factory = getattr(Wrappers, key)
                wrappers.append(factory(*values))
            elif isinstance(item, str):
                wrapper = getattr(Wrappers, item)
                wrappers.append(wrapper)
        command_dict.update(wrappers=wrappers)

    # Update command settings
    if settings := cmd.get('settings'):
        command_dict.update(settings=settings)

    return type(class_name, (type_,), command_dict)


def load_commands(controller):
    if not os.path.exists('./commands.yaml'):
        main_logger.info('commands.yaml file is missing')
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
            controller.register_command(cmd['name'], klass.as_command())
            loaded_commands_count += 1
        except Exception as e:
            errors_count += 1
            cmd_name = cmd.get('name', None)
            if cmd_name is None:
                gui_logger.error(f'Failed to load command. [{e}]')
            else:
                gui_logger.error(f'Failed to load command "{cmd_name}". [{e}]')

    gui_logger.info(f'Loaded {loaded_commands_count} command(s). ({errors_count} errors)')
