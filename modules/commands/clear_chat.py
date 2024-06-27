from modules.command_controllers import CommandChatTypes, InitializerConfig
from modules.lobby_manager import lobby_manager
from modules.logs import get_logger
from modules.permissions import is_admin
from modules.typing import GameChatMessage
from modules.utils.text import get_args

main_logger = get_logger("main")
combo_logger = get_logger("combo")

CLEAR_WRONG_SYNTAX_MSG = r'Wrong syntax! e.g. !clear \global \user="username" !solly !medic'


def handle_clear(logline: GameChatMessage, shared_dict: InitializerConfig):
    args = get_args(logline.prompt)
    commands = [cmd for cmd in logline.prompt.split() if not cmd.startswith("\\")]

    if is_admin(logline.player):
        if len(commands) == 0:
            raise Exception(f"You didn't provide any commands to clear. (solly, demo etc.)")

        for command in commands:
            # Check if command exist
            if command not in shared_dict.LOADED_COMMANDS:
                combo_logger.warning(f"Trying to clear unknown command - {command}. Skipping...")
                continue

            # Decide what to clear personal/other users
            if args:
                # Clear global chat
                if r"\global" in args:
                    chat = shared_dict.CHAT_CONVERSATION_HISTORY.get_command_chat_history(
                        command, CommandChatTypes.GLOBAL, logline.player
                    )
                    if chat is not None:
                        chat.reset()
                        shared_dict.CHAT_CONVERSATION_HISTORY.set_command_chat_history(
                            command, CommandChatTypes.GLOBAL, chat, logline.player
                        )
                        combo_logger.info(f"Clearing global chat history for command '{command}'.")
                        continue
                    combo_logger.warning(
                        f'Global chat for command "{command}" does not exist yet. Skipping...'
                    )

                # Clear users chats
                for arg in args:
                    # Ignore global arg
                    if arg == r"\global":
                        continue

                    # Ignore if it's anything else than \user='whatever'
                    if not arg.startswith(r"\user="):
                        combo_logger.error(CLEAR_WRONG_SYNTAX_MSG)
                        continue

                    try:
                        parts = arg.split("=")
                        if len(parts) != 2:
                            combo_logger.error(CLEAR_WRONG_SYNTAX_MSG)
                            continue

                        name: str
                        arg: str
                        arg, name = parts

                        if not (name.startswith("'") and name.endswith("'")):
                            combo_logger.error(CLEAR_WRONG_SYNTAX_MSG)
                            continue

                        name = name.removeprefix("'")
                        name = name.removesuffix("'")

                        player = lobby_manager.get_player_by_name(name)
                        if player is not None:
                            chat = shared_dict.CHAT_CONVERSATION_HISTORY.get_command_chat_history(
                                command, CommandChatTypes.PRIVATE, player
                            )
                            if chat is not None:
                                chat.reset()
                                shared_dict.CHAT_CONVERSATION_HISTORY.set_command_chat_history(
                                    command, CommandChatTypes.PRIVATE, chat, logline.player
                                )
                                combo_logger.info(
                                    f"Clearing chat history for user '{player.name}' [{command}]."
                                )
                                continue
                            combo_logger.warning(
                                f'Private chat for user "{player.name}" [{command}] does not exist yet. Skipping...'
                            )

                        else:
                            combo_logger.info(f"Failed to find user with name: '{name}'.")

                    except Exception as e:
                        main_logger.trace(f"Failed to parse arg in clear chat command. [{e}]")
                        continue

            else:
                # Clear private chats
                chat = shared_dict.CHAT_CONVERSATION_HISTORY.get_command_chat_history(
                    command, CommandChatTypes.PRIVATE, logline.player
                )
                if chat is not None:
                    chat.reset()
                    shared_dict.CHAT_CONVERSATION_HISTORY.set_command_chat_history(
                        command, CommandChatTypes.PRIVATE, chat, logline.player
                    )
                    combo_logger.info(
                        f"Clearing chat history for user '{logline.player.name}' [{command}]."
                    )
                    continue
                combo_logger.warning(
                    f'Private chat for user "{logline.player.name}" [{command}] does not exist yet. Skipping...'
                )

    else:
        if len(commands) == 0:
            raise Exception(f"You didn't provide any commands to clear. (solly, demo etc.)")

        for command in commands:
            if command not in shared_dict.LOADED_COMMANDS:
                combo_logger.warning(f"Trying to clear unknown command - {command}. Skipping...")

            chat = shared_dict.CHAT_CONVERSATION_HISTORY.get_command_chat_history(
                command, CommandChatTypes.PRIVATE, logline.player
            )
            if chat is not None:
                chat.reset()
                shared_dict.CHAT_CONVERSATION_HISTORY.set_command_chat_history(
                    command, CommandChatTypes.PRIVATE, chat, logline.player
                )
                combo_logger.info(
                    f"Clearing chat history for user '{logline.player.name}' [{command}]."
                )
                continue
            combo_logger.warning(
                f'Private chat for user "{logline.player.name}" [{command}] does not exist yet. Skipping...'
            )
