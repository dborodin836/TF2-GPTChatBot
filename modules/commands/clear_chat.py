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

        if len(commands) == 0:
            raise Exception(f"You didn't provide any commands to clear. (solly, demo etc.)")

        for command in commands:
            # Check if command exist
            if command not in shared_dict.LOADED_COMMANDS:
                combo_logger.warning(f'Trying to clear unknown command - {command}. Skipping...')
                continue

            # Decide what to clear personal/other users
            if args:
                # Clear global chat
                if r'\global' in args:
                    chat = shared_dict.CHAT_CONVERSATION_HISTORY.get_command_chat_history(
                        command,
                        CommandChatTypes.GLOBAL,
                        logline.player
                    )
                    if chat is not None:
                        chat.reset()
                        shared_dict.CHAT_CONVERSATION_HISTORY.set_command_chat_history(command,
                                                                                       CommandChatTypes.GLOBAL,
                                                                                       chat,
                                                                                       logline.player)
                        combo_logger.info(f"Clearing global chat history for command '{command}'.")
                        continue
                    combo_logger.warning(
                        f'Global chat for command "{command}" does not exist yet. Skipping...')

                # Clear users chats
                if True:
                    ...

            else:
                # Clear private chats
                chat = shared_dict.CHAT_CONVERSATION_HISTORY.get_command_chat_history(
                    command,
                    CommandChatTypes.PRIVATE,
                    logline.player
                )
                if chat is not None:
                    chat.reset()
                    shared_dict.CHAT_CONVERSATION_HISTORY.set_command_chat_history(command, CommandChatTypes.PRIVATE,
                                                                                   chat,
                                                                                   logline.player)
                    combo_logger.info(f"Clearing chat history for user '{logline.player.name}' [{command}].")
                    continue
                combo_logger.warning(
                    f'Private chat for user "{logline.player.name}" [{command}] does not exist yet. Skipping...')

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
