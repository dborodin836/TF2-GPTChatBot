from config import config
from modules.api.textgen_webui import get_custom_model_response
from modules.logs import get_logger, log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import LogLine
from modules.utils.text import get_system_message

main_logger = get_logger("main")


def handle_custom_model(logline: LogLine, shared_dict: dict):
    main_logger.info(
        f"'{config.CUSTOM_MODEL_COMMAND}' command from user '{logline.username}'. "
        f"Message: '{logline.prompt.removeprefix(config.CUSTOM_MODEL_COMMAND).strip()}'"
    )
    log_gui_model_message(
        "CUSTOM",
        logline.username,
        logline.prompt.removeprefix(config.CUSTOM_MODEL_COMMAND).strip(),
    )

    user_message = logline.prompt
    sys_message = get_system_message(
        logline.prompt, enable_soft_limit=config.ENABLE_SOFT_LIMIT_FOR_CUSTOM_MODEL
    )

    message = message.removeprefix(config.CUSTOM_MODEL_COMMAND).strip()

    response = get_custom_model_response(
        [
            sys_message,
            {"role": "assistant", "content": config.GREETING},
            {"role": "user", "content": user_message},
        ]
    )

    if response:
        log_gui_model_message("CUSTOM", logline.username, response.strip())
        send_say_command_to_tf2(response, logline.username, logline.is_team_message)


def handle_custom_chat(logline: LogLine, shared_dict: dict):
    conversation_history = shared_dict["CHAT_CONVERSATION_HISTORY"]

    log_gui_model_message(
        "CUSTOM CHAT",
        logline.username,
        logline.prompt.removeprefix(config.CUSTOM_MODEL_CHAT_COMMAND).strip(),
    )

    sys_message = get_system_message(logline.prompt)
    message = add_prompts_by_flags(logline.prompt)
    message = message.removeprefix(config.CUSTOM_MODEL_CHAT_COMMAND).strip()
    # TODO: fix required
    if not conversation_history:
        conversation_history.append({"role": "assistant", "content": config.GREETING})
    conversation_history.append({"role": "user", "content": message})
    conversation_history.append(sys_message)
    response = get_custom_model_response(conversation_history)

    if response:
        conversation_history.append({"role": "assistant", "content": response})
        log_gui_model_message("CUSTOM CHAT", logline.username, response.strip())
        send_say_command_to_tf2(response, logline.username, logline.is_team_message)
        shared_dict.update({"CHAT_CONVERSATION_HISTORY": conversation_history})
