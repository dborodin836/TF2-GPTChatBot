import codecs
import os
import sys
from typing import List

from modules.logs import combo_logger, gui_logger

# PROMPTS is an empty list used to store prompts data that will be loaded later.
# TODO: create Prompt type
PROMPTS: List[dict] = []


def load_prompts() -> None:
    """
    Load prompt data from files in the 'prompts' directory.
    """
    global PROMPTS
    PROMPTS.clear()

    try:
        files = [f for f in os.listdir("prompts") if f.endswith(".txt")]
    except FileNotFoundError:
        combo_logger.warning("No prompts directory found. Creating...")
        try:
            os.makedirs("prompts")
        except Exception as e:
            combo_logger.error(f"Failed to create prompts directory. [{e}]")
        files = []

    # In order for pyinstaller to work
    if getattr(sys, "frozen", False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    for filename in files:
        with codecs.open(f"{path}/prompts/{filename}", "r", encoding="utf-8") as file:
            PROMPTS.append({"flag": f"\\{filename.removesuffix('.txt')}", "prompt": file.read()})
    combo_logger.info(
        f'Loaded {len([f for f in os.listdir("prompts") if f.endswith(".txt")])} models!'
    )


def get_prompt_by_name(name: str) -> str:
    for prompt in PROMPTS:
        if prompt["flag"] == f"\\{name}":
            return prompt["prompt"]
    gui_logger.warning(f"Prompt {name} does not exist.")
    return ""
