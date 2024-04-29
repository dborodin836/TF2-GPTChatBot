import requests

from config import config
from modules.api.base import LLMProvider
from modules.logs import get_logger, log_gui_model_message
from modules.servers.tf2 import send_say_command_to_tf2
from modules.typing import Message
from modules.utils.text import get_system_message, remove_args

main_logger = get_logger("main")
combo_logger = get_logger("combo")


class TextGenerationWebUILLMProvider(LLMProvider):

    @staticmethod
    def get_quick_query_completion(username, user_prompt, model, is_team_chat=False):
        log_gui_model_message(model, username, user_prompt)

        user_message = remove_args(user_prompt)
        sys_message = get_system_message(user_prompt)

        payload = [
            sys_message,
            Message(role="assistant", content=config.GREETING),
            Message(role="user", content=user_message),
        ]

        response = TextGenerationWebUILLMProvider._try_get_response(payload, username, model)

        if response:
            log_gui_model_message(model, username, " ".join(response.split()))
            send_say_command_to_tf2(response, username, is_team_chat)

    @staticmethod
    def get_chat_completion(username, user_prompt, conversation_history, model, is_team=False):
        log_gui_model_message(model, username, user_prompt)

        user_message = remove_args(user_prompt)

        conversation_history.add_user_message_from_prompt(user_message)

        response = TextGenerationWebUILLMProvider._try_get_response(conversation_history.get_messages_array(), username,
                                                                    model)

        if response:
            conversation_history.add_assistant_message(Message(role="assistant", content=response))
            log_gui_model_message(model, username, " ".join(response.split()))
            send_say_command_to_tf2(response, username, is_team)

        return conversation_history

    @staticmethod
    def _get_provider_response(conversation_history, username, model):
        uri = f"http://{config.CUSTOM_MODEL_HOST}/v1/chat/completions"

        headers = {"Content-Type": "application/json"}

        data = {"mode": "chat", "messages": conversation_history}

        data.update(config.CUSTOM_MODEL_SETTINGS)

        response = requests.post(uri, headers=headers, json=data, verify=False)

        if response.status_code == 200:
            try:
                data = response.json()["choices"][0]["message"]["content"]
                return data
            except Exception as e:
                combo_logger.error(f"Failed to parse data from server [{e}].")
        elif response.status_code == 500:
            combo_logger.error(f"There's error on the text-generation-webui server. [HTTP 500]")
        main_logger.error(
            f"Got non-200 status code from the text-generation-webui server. [HTTP {response.status_code}]"
        )
        raise Exception('Non-200 response received.')

    @staticmethod
    def _try_get_response(conversation_history, username, model):
        try:
            return TextGenerationWebUILLMProvider._get_provider_response(conversation_history, username, model)
        except Exception as e:
            combo_logger.error(f"Failed to get response from the text-generation-webui server. [{e}]")
            return None
