from config import config
from modules.api.textgen_webui import get_custom_model_response
from modules.command_controllers import InitializerConfig
from modules.conversation_history import ConversationHistory
from modules.logs import get_logger, log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine, Message
from modules.utils.text import get_system_message

main_logger = get_logger("main")


def handle_custom_model(logline: LogLine, shared_dict: InitializerConfig):
    main_logger.info(
        f"'{config.CUSTOM_MODEL_COMMAND}' command from user '{logline.username}'. "
        f"Message: '{logline.prompt.removeprefix(config.CUSTOM_MODEL_COMMAND).strip()}'"
    )
    log_gui_model_message(
        "CUSTOM",
        logline.username,
        logline.prompt.removeprefix(config.CUSTOM_MODEL_COMMAND).strip(),
    )

    user_message = logline.prompt.removeprefix(config.CUSTOM_MODEL_COMMAND).strip()
    sys_message = get_system_message(
        logline.prompt, enable_soft_limit=config.ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL
    )

    response = get_custom_model_response(
        [
            sys_message,
            Message(role="assistant", content=config.GREETING),
            Message(role="user", content=user_message),
        ]
    )

    if response:
        log_gui_model_message("CUSTOM", logline.username, response.strip())
        send_say_command_to_tf2(response, logline.username, logline.is_team_message)


def handle_custom_user_chat(logline: LogLine, shared_dict: InitializerConfig):
    conversation_history: ConversationHistory = shared_dict.CHAT_CONVERSATION_HISTORY.get_conversation_history_by_name(
        logline.username)

    log_gui_model_message(
        "CUSTOM CHAT",
        logline.username,
        logline.prompt.removeprefix(config.CUSTOM_MODEL_CHAT_COMMAND).strip(),
    )

    user_message = logline.prompt.removeprefix(config.CUSTOM_MODEL_CHAT_COMMAND).strip()
    conversation_history.add_user_message_from_prompt(user_message)
    response = get_custom_model_response(conversation_history.get_messages_array())

    if response:
        conversation_history.add_assistant_message(Message(role="assistant", content=response))
        log_gui_model_message("CUSTOM CHAT", logline.username, response.strip())
        send_say_command_to_tf2(response, logline.username, logline.is_team_message)
        shared_dict.CHAT_CONVERSATION_HISTORY.set_conversation_history_by_name(logline.username, conversation_history)


def handle_custom_global_chat(logline: LogLine, shared_dict: InitializerConfig):
    conversation_history: ConversationHistory = shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL

    log_gui_model_message(
        "GLOBAL CUSTOM CHAT",
        logline.username,
        logline.prompt.removeprefix(config.CUSTOM_MODEL_CHAT_COMMAND).strip(),
    )

    user_message = logline.prompt.removeprefix(config.GLOBAL_CUSTOM_CHAT_COMMAND).strip()
    conversation_history.add_user_message_from_prompt(user_message)
    response = get_custom_model_response(conversation_history.get_messages_array())

    if response:
        conversation_history.add_assistant_message(Message(role="assistant", content=response))
        log_gui_model_message("GLOBAL CUSTOM CHAT", logline.username, response.strip())
        send_say_command_to_tf2(response, logline.username, logline.is_team_message)
        shared_dict.CHAT_CONVERSATION_HISTORY.GLOBAL = conversation_history
