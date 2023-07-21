import os
import sys
import time
import codecs
import asyncio

# PROMPTS is an empty list used to store prompts data that will be loaded later.
PROMPTS = []


async def load_prompt_async(path, filename):
    with codecs.open(f"{path}/prompts/{filename}", 'r', encoding='utf-8') as file:
        global PROMPTS
        PROMPTS.append(
            {
                "flag": f"\\{filename.removesuffix('.txt')}",
                "prompt": file.read()
            }
        )


def get_prompt_dir_path():
    # In order for pyinstaller to work
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


async def load_prompts() -> None:
    """
    Load prompt data from files in the 'prompts' directory.
    """
    try:
        files = [f for f in os.listdir("prompts") if f.endswith('.txt')]
    except FileNotFoundError:
        print("No prompts directory found. Creating...")
        os.makedirs('prompts')
        files = []

    path = get_prompt_dir_path()
    await asyncio.gather(*[load_prompt_async(path, file) for file in files])
    print(f'Loaded {len(files)} models.')
