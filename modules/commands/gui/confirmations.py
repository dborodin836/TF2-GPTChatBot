from modules.command_controllers import InitializerConfig
from modules.commands.gui.invoke import invoke
from modules.logs import gui_logger
from modules.typing import ConfirmationStatus


def confirm(command: str, shared_dict: InitializerConfig):
    command_name = command.removeprefix("c").strip()
    if command_name not in shared_dict.LOADED_COMMANDS:
        gui_logger.warning("Command with specified name not found.")
        return None

    try:
        shared_dict.CONFIRMATIONS[command_name]["status"]
    except KeyError:
        gui_logger.warning("Command with specified name not found.")
        return None

    shared_dict.CONFIRMATIONS[command_name]["status"] = ConfirmationStatus.CONFIRMED

    invoke(f"@ !{command_name}", shared_dict)
