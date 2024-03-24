import requests

from config import config
from modules.logs import get_logger
from modules.typing import Message

main_logger = get_logger("main")
combo_logger = get_logger("combo")


def get_custom_model_response(conversation_history: list[Message]) -> str | None:
    uri = f"http://{config.CUSTOM_MODEL_HOST}/v1/chat/completions"

    headers = {"Content-Type": "application/json"}

    data = {"mode": "chat", "messages": conversation_history}

    data.update(config.CUSTOM_MODEL_SETTINGS)  # type: ignore[arg-type]

    try:
        response = requests.post(uri, headers=headers, json=data, verify=False)
    except Exception as e:
        combo_logger.error(f"Failed to get response from the text-generation-webui server. [{e}]")
        return None

    if response.status_code == 200:
        try:
            model_response = response.json()["choices"][0]["message"]["content"]
            return model_response
        except Exception as e:
            combo_logger.error(f"Failed to parse data from server [{e}].")
    elif response.status_code == 500:
        combo_logger.error(f"There's error on the text-generation-webui server. [HTTP 500]")
    else:
        main_logger.error(
            f"Got non-200 status code from the text-generation-webui server. [HTTP {response.status_code}]"
        )

    return None
