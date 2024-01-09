import requests

from config import config
from utils.logs import get_logger
from utils.types import Message

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")


def print_help_command():
    """
    Prints the available commands and their descriptions.
    """
    gui_logger.info(
        "### HELP ###",
        "start - start the bot",
        "stop - stop the bot",
        "quit - quit the program",
        "bans - show all banned players",
        "ban <username> - ban user by username",
        "unban <username> - unban user by username",
        "gpt3 <prompt> - sends a response to GPT3",
        sep="\n",
    )


def get_custom_model_response(conversation_history: list[Message]) -> str | None:
    uri = f"http://{config.CUSTOM_MODEL_HOST}/v1/chat/completions"

    headers = {
        "Content-Type": "application/json"
    }

    data = {
        "mode": "chat",
        "messages": conversation_history
    }

    data.update(config.CUSTOM_MODEL_SETTINGS)

    try:
        response = requests.post(uri, headers=headers, json=data, verify=False)
    except Exception as e:
        combo_logger.error(f"Failed to get response from the text-generation-webui server. [{e}]")
        return

    if response.status_code == 200:
        try:
            data = response.json()['choices'][0]['message']['content']
            return data
        except Exception as e:
            combo_logger.error(f"Failed to parse data from server [{e}].")
    elif response.status_code == 500:
        combo_logger.error(f"There's error on the text-generation-webui server. [HTTP 500]")
    else:
        main_logger.error(f"Got non-200 status code from the text-generation-webui server. [HTTP {response.status_code}]")

    return None


