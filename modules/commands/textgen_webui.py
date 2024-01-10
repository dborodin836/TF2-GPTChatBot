from config import config
from modules.servers.tf2 import send_say_command_to_tf2
from modules.api.textgen_webui import get_custom_model_response
from modules.logs import get_logger, log_gui_model_message
from modules.utils.text import add_prompts_by_flags
from modules.types import LogLine, MessageHistory

main_logger = get_logger("main")


def handle_custom_model(logline: LogLine, shared_dict: dict):
    if config.ENABLE_CUSTOM_MODEL:
        main_logger.info(f"'{config.CUSTOM_MODEL_COMMAND}' command from user '{logline.username}'. "
                         f"Message: '{logline.prompt.removeprefix(config.GPT_COMMAND).strip()}'")
        handle_custom_model_command(
            logline.username,
            logline.prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
            is_team=logline.is_team_message
        )


def handle_custom_chat(logline: LogLine, shared_dict: dict):
    if config.ENABLE_CUSTOM_MODEL:
        ch = handle_custom_model_chat_command(
            logline.username,
            logline.prompt.removeprefix(config.CHATGPT_COMMAND).strip(),
            shared_dict["CHAT_CONVERSATION_HISTORY"],
            is_team=logline.is_team_message
        )

        shared_dict.update({"CHAT_CONVERSATION_HISTORY": ch})


def handle_custom_model_command(
        username: str,
        user_prompt: str,
        is_team: bool = False
) -> None:
    log_gui_model_message("CUSTOM", username, user_prompt.strip())

    message = add_prompts_by_flags(user_prompt)

    response = get_custom_model_response([{"role": "user", "content": message}, ])

    if response:
        log_gui_model_message("CUSTOM", username, response.strip())
        send_say_command_to_tf2(response, username, is_team)


def handle_custom_model_chat_command(
        username: str,
        user_prompt: str,
        conversation_history: MessageHistory,
        is_team: bool = False
) -> MessageHistory:
    log_gui_model_message("CUSTOM CHAT", username, user_prompt.strip())

    message = add_prompts_by_flags(user_prompt)
    conversation_history.append({"role": "user", "content": message})
    response = get_custom_model_response(conversation_history)

    if response:
        conversation_history.append({"role": "assistant", "content": response})
        log_gui_model_message("CUSTOM CHAT", username, response.strip())
        send_say_command_to_tf2(response, username, is_team)

    return conversation_history
