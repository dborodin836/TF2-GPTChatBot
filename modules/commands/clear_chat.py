from modules.command_controllers import InitializerConfig
from modules.permissions import is_admin
from modules.typing import LogLine
from modules.utils.text import get_args
from modules.logs import get_logger
from config import config

main_logger = get_logger("main")
combo_logger = get_logger("combo")


def handle_clear(logline: LogLine, shared_dict: InitializerConfig):
    if is_admin(logline.player):
        args = get_args(logline.prompt.removeprefix(config.CLEAR_CHAT_COMMAND).strip())

        if len(args) == 0:
            combo_logger.info(f"Clearing chat history for user '{logline.username}'.")
            conv_history = shared_dict.CHAT_CONVERSATION_HISTORY.get_conversation_history_by_name(logline.username)
            conv_history.reset()
            shared_dict.CHAT_CONVERSATION_HISTORY.set_conversation_history_by_name(logline.username, conv_history)
            return

        if r"\global" in args:
            shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL.reset()
            args.remove(r"\global")
            combo_logger.info("Clearing global chat!")

        for arg in args:
            try:
                parts = arg.split("=")
                if len(parts) != 2:
                    combo_logger.error(r'Wrong syntax! e.g. !clear \global \user="username"')
                    continue

                name: str
                arg: str
                arg, name = parts

                if arg != r"\user":
                    combo_logger.error(r'Wrong syntax! e.g. !clear \global \user="username"')
                    continue

                if not (name.startswith("'") and name.endswith("'")):
                    combo_logger.error(r'Wrong syntax! e.g. !clear \global \user="username"')
                    continue

                name = name.removeprefix("'")
                name = name.removesuffix("'")

                combo_logger.info(f"Clearing chat history for user '{name}'.")
                conv_history = shared_dict.CHAT_CONVERSATION_HISTORY.get_conversation_history_by_name(name)
                conv_history.reset()
                shared_dict.CHAT_CONVERSATION_HISTORY.set_conversation_history_by_name(name, conv_history)

            except Exception as e:
                main_logger.trace(f"Failed to parse arg in clear chat command. [{e}]")
                continue

    else:
        combo_logger.info(f"Clearing chat history for user '{logline.username}'.")
        conv_history = shared_dict.CHAT_CONVERSATION_HISTORY.get_conversation_history_by_name(logline.username)
        conv_history.reset()
        shared_dict.CHAT_CONVERSATION_HISTORY.set_conversation_history_by_name(logline.username, conv_history)
