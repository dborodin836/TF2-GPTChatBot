from modules.command_controllers import InitializerConfig
from modules.logs import gui_logger
from modules.utils.audio import get_devices


def handle_list_devices(command: str, shared_dict: InitializerConfig):
    gui_logger.info("Available devices:")
    gui_logger.info("#" * 10)
    for device in get_devices():
        gui_logger.info(f"- {device}")
    gui_logger.info("#" * 10)
