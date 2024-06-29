import copy
import os.path
from typing import Dict, List

import oyaml as yaml

from modules.builder.loaders import COMMAND_TYPES, WRAPPERS, InvalidCommandException
from modules.command_controllers import CommandController
from modules.commands.base import BaseCommand
from modules.logs import gui_logger, main_logger


def get_commands_from_yaml() -> List[dict]:
    with open("commands.yaml", "r") as file:
        data = yaml.safe_load(file)

    return data["commands"]


def load_command_specific_attrs(type_: str, raw_data: dict) -> Dict:
    command_def = COMMAND_TYPES.get(type_)
    if command_def is None:
        raise InvalidCommandException(f"Command type {type_} not supported")
    loader = command_def.loader
    loader_instance = loader(raw_data)
    return loader_instance.get_data()


def create_command_from_dict(cmd: dict) -> BaseCommand:
    command_dict: Dict = {}
    command_dict.update(name=cmd["name"])
    class_name = f"DynamicCommand{cmd['name']}"

    # Command type
    try:
        type_ = COMMAND_TYPES[cmd["type"]].klass
    except Exception as e:
        raise InvalidCommandException(
            f"Command type is invalid or missing. Expected one of {list(COMMAND_TYPES.keys())}"
        )

    command_dict.update(load_command_specific_attrs(cmd["type"], cmd))

    # Update command wrappers
    if traits := cmd.get("traits"):
        wrappers = []
        for wrapper in traits:
            try:
                wrapper_id = wrapper["__id"]
                wrapper.pop("__id")
                if len(list(wrapper.keys())) > 0:
                    factory = WRAPPERS[wrapper_id]
                    wrappers.append(factory(**wrapper))  # type: ignore
                else:
                    wrappers.append(WRAPPERS[wrapper_id])
            except Exception as e:
                gui_logger.warning(f"{e} is not a valid trait.")
        command_dict.update(wrappers=wrappers)

    return type(class_name, (type_,), command_dict)  # type: ignore


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

    for raw_command_dict in commands:
        try:
            meta_info_copy = copy.deepcopy(raw_command_dict)
            klass = create_command_from_dict(raw_command_dict)
            chat_command_name = raw_command_dict["prefix"] + raw_command_dict["name"]
            controller.register_command(
                chat_command_name, klass.as_command(), raw_command_dict["name"], meta=meta_info_copy
            )
            loaded_commands_count += 1
        except Exception as e:
            errors_count += 1
            cmd_name = raw_command_dict.get("name", None)
            if cmd_name is None:
                gui_logger.error(f"Failed to load command. [{e}]")
            else:
                gui_logger.error(f'Failed to load command "{cmd_name}". [{e}]')

    gui_logger.info(f"Loaded {loaded_commands_count} command(s). ({errors_count} errors)")
