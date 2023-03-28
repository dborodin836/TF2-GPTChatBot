import os
import sys
import codecs

# PROMPTS is an empty list used to store prompts data that will be loaded later.
PROMPTS = []


def load_prompts():
    try:
        files = [f for f in os.listdir("prompts") if f.endswith('.txt')]
    except FileNotFoundError:
        print("No prompts directory found. Creating...")
        os.makedirs('prompts')
        files = []

    if getattr(sys, 'frozen', False):
        path = os.path.dirname(sys.executable)
    else:
        path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    for filename in files:
        with codecs.open(f"{path}/prompts/{filename}", 'r', encoding='utf-8') as file:
            global PROMPTS
            PROMPTS.append(
                {
                    "flag": f"\\{filename.removesuffix('.txt')}",
                    "prompt": file.read()
                }
            )
    print(f'Loaded {len([f for f in os.listdir("prompts") if f.endswith(".txt")])} models!')
