import json

import requests

from config import config

GITHUB_API_REPO_LINK = 'https://api.github.com/repos/dborodin836/TF2-GPTChatBot/releases/latest'


def check_for_updates() -> None:
    """
    Checks if there's a new release of a GitHub repository available.
    """
    try:
        response = requests.get(GITHUB_API_REPO_LINK)
    except Exception as e:
        print(f"Failed to check for updates! [{e}]")
        return

    data = json.loads(response.content)
    latest_version = data['tag_name']

    if latest_version > config.APP_VERSION:
        print(f'A new version ({latest_version}) of the app is available. Please update.')
    else:
        print(f'The app is up to date. ({latest_version})')