from modules.command_controllers import CommandChatTypes, InitializerConfig
from modules.lobby_manager import lobby_manager
from modules.permissions import is_admin
from modules.typing import LogLine
from modules.utils.text import get_args
from modules.logs import get_logger

main_logger = get_logger("main")
combo_logger = get_logger("combo")

CLEAR_WRONG_SYNTAX_MSG = r'Wrong syntax! e.g. !clear \global \user="username" !solly !medic'


def handle_clear(logline: LogLine, shared_dict: InitializerConfig):
    if is_admin(logline.player):
        args = get_args(logline.prompt)
        commands = [cmd for cmd in logline.prompt.split() if not cmd.startswith('\\')]
        print(args)
        print(commands)

        if len(commands) == 0:
            raise Exception(f"You didn't provide any commands to clear. (solly, demo etc.)")

        for command in commands:
            if command not in shared_dict.LOADED_COMMANDS:
                combo_logger.warning(f'Trying to clear unknown command - {command}. Skipping...')

            if len(args) == 0:
                for command in commands:
                    if command not in shared_dict.LOADED_COMMANDS:
                        combo_logger.warning(f'Trying to clear unknown command - {command}. Skipping...')

                    if logline.player is not None:
                        combo_logger.info(f"Clearing chat history for user '{logline.player.name}' [{command}].")
                        combo_logger.trace(f'Trying to clear for command "{command}", user:{logline.player.steamid64}')
                        conv_history = shared_dict.CHAT_CONVERSATION_HISTORY.get_command_chat_history(command,
                                                                                                      CommandChatTypes.PRIVATE,
                                                                                                      logline.player)
                        conv_history.reset()
                        shared_dict.CHAT_CONVERSATION_HISTORY.set_command_chat_history(command,
                                                                                       CommandChatTypes.PRIVATE,
                                                                                       conv_history, logline.player)
                    else:
                        combo_logger.info(f"Failed to find user with name: '{logline.username}'.")

            for arg in args:
                if arg == r'\global':
                    try:
                        shared_dict.CHAT_CONVERSATION_HISTORY.get_command_chat_history(command, CommandChatTypes.GLOBAL)
                        combo_logger.warning(f'Clearing global command chat - {command}.')
                    except Exception:
                        pass
                    finally:
                        continue

                try:
                    parts = arg.split("=")
                    if len(parts) != 2:
                        combo_logger.error(CLEAR_WRONG_SYNTAX_MSG)
                        continue

                    name: str
                    arg: str
                    arg, name = parts

                    if arg != r"\user":
                        combo_logger.error(CLEAR_WRONG_SYNTAX_MSG)
                        continue

                    if not (name.startswith("'") and name.endswith("'")):
                        combo_logger.error(CLEAR_WRONG_SYNTAX_MSG)
                        continue

                    name = name.removeprefix("'")
                    name = name.removesuffix("'")

                    player = lobby_manager.get_player_by_name(name)
                    if player is not None:
                        combo_logger.info(f"Clearing chat history for user '{player.name}' [{command}].")
                        conv_history = shared_dict.CHAT_CONVERSATION_HISTORY.get_command_chat_history(command,
                                                                                                      CommandChatTypes.PRIVATE,
                                                                                                      player)
                        conv_history.reset()
                        shared_dict.CHAT_CONVERSATION_HISTORY.set_command_chat_history(command,
                                                                                       CommandChatTypes.PRIVATE,
                                                                                       conv_history, player)
                    else:
                        combo_logger.info(f"Failed to find user with name: '{name}'.")

                except Exception as e:
                    main_logger.trace(f"Failed to parse arg in clear chat command. [{e}]")
                    continue

    else:
        player = lobby_manager.get_player_by_name(logline.username)
        commands = [cmd for cmd in logline.prompt.split() if not cmd.startswith('\\')]

        if len(commands) == 0:
            raise Exception(f"You didn't provide any commands to clear. (solly, demo etc.)")

        for command in commands:
            if command not in shared_dict.LOADED_COMMANDS:
                combo_logger.warning(f'Trying to clear unknown command - {command}. Skipping...')

            if player is not None:
                combo_logger.info(f"Clearing chat history for user '{player.name}' [{command}].")
                conv_history = shared_dict.CHAT_CONVERSATION_HISTORY.get_command_chat_history(command,
                                                                                              CommandChatTypes.PRIVATE,
                                                                                              player)
                conv_history.reset()
                shared_dict.CHAT_CONVERSATION_HISTORY.set_command_chat_history(command, CommandChatTypes.PRIVATE,
                                                                               conv_history, player)
            else:
                combo_logger.info(f"Failed to find user with name: '{logline.username}'.")
