from modules.logs import get_logger
from modules.utils.config import (
    get_value_config,
    load_config,
    reload_config,
    save_config,
    set_value_config,
)

gui_logger = get_logger("gui")


def handle_config(command, shared_dict):
    parts = command.split()[1:]

    if len(parts) < 1:
        gui_logger.warning("Wrong usage! Check `help` command!")
        return

    # Extract the operation and potentially other arguments
    operation = parts[0].lower()
    args = parts[1:]

    if operation == "reload":
        reload_config()

    elif operation == "load":
        if len(args) == 0:
            gui_logger.warning("You didn't provide filename.")
            return

        load_config(args[0])

    elif operation == "save":
        if len(args) == 0:
            gui_logger.warning("You didn't provide filename.")
            return

        save_config(args[0])

    elif operation == "set":
        if len(args) == 0:
            gui_logger.warning("You didn't provide any setting to set.")
            return

        to_set = list()

        for arg in args:
            try:
                name, val = arg.split("=")
                to_set.append((name, val))
            except Exception as e:
                gui_logger.warning(f"Failed to parse input: {arg} [{e}]")

        set_value_config(to_set)

    elif operation == "get":
        if len(args) == 0:
            gui_logger.warning("You didn't provide any setting to get.")
            return
        get_value_config(args)

    else:
        gui_logger.warning(f"Unknown command config {operation}")
