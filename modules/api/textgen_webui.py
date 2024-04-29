import requests

from config import config
from modules.api.base import LLMProvider
from modules.logs import get_logger

main_logger = get_logger("main")
combo_logger = get_logger("combo")


class TextGenerationWebUILLMProvider(LLMProvider):

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
