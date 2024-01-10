import json

import requests

from config import config
from modules.logs import get_logger

GITHUB_API_REPO_LINK = "https://api.github.com/repos/dborodin836/TF2-GPTChatBot/releases/latest"

main_logger = get_logger("main")
gui_logger = get_logger("gui")


def check_for_updates() -> None:
    """
    Checks if there's a new release of a GitHub repository available.
    """
    main_logger.info(f"Checking for updates... App version - {config.APP_VERSION}")
    try:
        response = requests.get(GITHUB_API_REPO_LINK)
        data = json.loads(response.content)
        latest_version = data["tag_name"]
    except Exception as e:
        gui_logger.info("Failed to check for updates.")
        main_logger.error(f"Failed to fetch latest version. [{e}]")
        return

    main_logger.info(f"Latest version on GitHub - {latest_version}")

    if latest_version > config.APP_VERSION:
        gui_logger.info(f"A new version ({latest_version}) of the app is available. Please update.")
    else:
        gui_logger.info(f"The app is up to date. ({config.APP_VERSION})")
