import random
import time

import requests

from config import config, RTDModes
from services.source_game import send_say_command_to_tf2
from utils.logs import log_cmd_message, log_message

RICKROLL_LINK = "youtu.be/dQw4w9WgXcQ"
GITHUB_LINK = "bit.ly/tf2-gpt3"


def handle_gh_command(username: str, is_team: bool = False) -> None:
    log_cmd_message(f"User '{username}' GET GH LINK")
    time.sleep(1)
    send_say_command_to_tf2(f"GitHub: {GITHUB_LINK}", is_team)


def handle_rtd_command(username: str, is_team: bool = False) -> None:
    """
    Handles the RTD (Roll The Dice) command for the given username.
    If RTD_MODE is set to RICKROLL, the user is rickrolled.
    If RTD_MODE is set to RANDOM_MEME, a random link for a meme is chosen from a file.
    """
    if config.RTD_MODE == RTDModes.RICKROLL.value:
        log_cmd_message("RICKROLLED!!11!!")
        time.sleep(1)
        send_say_command_to_tf2(f"[RTD] {username} rolled: {RICKROLL_LINK}")
    elif config.RTD_MODE == RTDModes.RANDOM_MEME.value:
        with open('vids.txt', 'r') as file:
            # Reads all lines and removes 'https://'
            lines = list(map(lambda x: x.removeprefix('https://').strip(), file.readlines()))
        time.sleep(1)
        log_cmd_message(f"[RTD] {username} rolled: {random.choice(lines)}")
        send_say_command_to_tf2(f"[RTD] {username} rolled: {random.choice(lines)}", is_team)


def print_help_command():
    """
    Prints the available commands and their descriptions.
    """
    print("### HELP ###",
          "start - start the bot",
          "stop - stop the bot",
          "quit - quit the program",
          "bans - show all banned players",
          "ban <username> - ban user by username",
          "unban <username> - unban user by username",
          "gpt3 <prompt> - sends a response to GPT3",
          sep='\n')


def handle_custom_model_command(user, is_team, prompt):
    log_message('CUSTOM', user, prompt.strip())
    uri = f'http://{config.CUSTOM_MODEL_HOST}/api/v1/generate'

    prompt = f'Below is an instruction that describes a task. Write a response that appropriately completes' \
             f' the request. Write response in less than 128 characters!\n### Instruction:\n' \
             f'{prompt.removeprefix(config.CUSTOM_MODEL_COMMAND).strip()}\n\n### Response:\n'

    try:
        request = {
            'prompt': prompt,
            'max_new_tokens': 150,
            'do_sample': True,
            'temperature': 1.3,
            'top_p': 0.1,
            'typical_p': 1,
            'epsilon_cutoff': 0,  # In units of 1e-4
            'eta_cutoff': 0,  # In units of 1e-4
            'repetition_penalty': 1.18,
            'top_k': 40,
            'min_length': 0,
            'no_repeat_ngram_size': 0,
            'num_beams': 1,
            'penalty_alpha': 0,
            'length_penalty': 1,
            'early_stopping': False,
            'mirostat_mode': 0,
            'mirostat_tau': 5,
            'mirostat_eta': 0.1,
            'seed': -1,
            'add_bos_token': True,
            'truncation_length': 2048,
            'ban_eos_token': False,
            'skip_special_tokens': True,
            'stopping_strings': []
        }

        response = requests.post(uri, json=request)

        if response.status_code == 200:
            result = response.json()['results'][0]['text']
            log_message('CUSTOM', user, result)
            send_say_command_to_tf2(result, is_team)

    except Exception as e:
        print(e)
