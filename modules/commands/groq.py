from config import config
from modules.api.groq import handle_groq_chat_request, handle_groq_request
from modules.command_controllers import InitializerConfig
from modules.typing import LogLine
from modules.logs import get_logger

main_logger = get_logger('main')


def handle_groq(logline: LogLine, shared_dict: InitializerConfig) -> None:
    main_logger.info(
        f"'{config.GPT_COMMAND}' command from user '{logline.username}'. "
        f"Message: '{logline.prompt.removeprefix(config.GPT_COMMAND).strip()}'"
    )
    handle_groq_request(
        logline.username,
        logline.prompt.removeprefix(config.GROQ_COMMAND).strip(),
        model=config.GROQ_MODEL,
        is_team_chat=logline.is_team_message,
    )


def handle_groq_private_chat(logline: LogLine, shared_dict: InitializerConfig):
    user_chat = shared_dict.CHAT_CONVERSATION_HISTORY.get_conversation_history(logline.player)

    conv_his = handle_groq_chat_request(
        logline.username,
        logline.prompt.removeprefix(config.GROQ_PRIVATE_CHAT).strip(),
        user_chat,
        is_team=logline.is_team_message,
        model=config.GROQ_MODEL,
    )
    shared_dict.CHAT_CONVERSATION_HISTORY.set_conversation_history(logline.player, conv_his)


def handle_groq_global_chat(logline: LogLine, shared_dict: InitializerConfig):
    conv_his = handle_groq_chat_request(
        logline.username,
        logline.prompt.removeprefix(config.GROQ_CHAT_COMMAND).strip(),
        shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL,
        is_team=logline.is_team_message,
        model=config.GROQ_MODEL,
    )
    shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL = conv_his
