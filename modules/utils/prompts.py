import codecs
import os
import sys

from modules.logs import get_logger

gui_logger = get_logger("gui")
combo_logger = get_logger("combo")

# PROMPTS is an empty list used to store prompts data that will be loaded later.
PROMPTS = []


def load_prompts() -> None:
    """
    Load prompt data from files in the 'prompts' directory.
    """
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
            global PROMPTS
            PROMPTS.append({"flag": f"\\{filename.removesuffix('.txt')}", "prompt": file.read()})
    combo_logger.info(
        f'Loaded {len([f for f in os.listdir("prompts") if f.endswith(".txt")])} models!'
    )
