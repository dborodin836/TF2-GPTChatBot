import requests

from config import config
from modules.api.base import LLMProvider
from modules.logs import get_logger

main_logger = get_logger("main")
combo_logger = get_logger("combo")


class TextGenerationWebUILLMProvider(LLMProvider):

    @staticmethod
    def get_completion_text(conversation_history, username, model, settings):
        uri = f"http://{config.CUSTOM_MODEL_HOST}/v1/chat/completions"
        headers = {"Content-Type": "application/json"}

        data = {"mode": "chat", "messages": conversation_history}
        if isinstance(settings, dict):
            data.update(settings)

        response = requests.post(uri, headers=headers, json=data, verify=False)
        if response.status_code == 500:
            raise Exception("HTTP 500")
        data = response.json()["choices"][0]["message"]["content"]
        return data
