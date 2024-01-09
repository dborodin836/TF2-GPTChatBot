import sys
import subprocess

os_name = sys.platform

if os_name.startswith("win"):
    commands = [
        "py -m venv venv",
        "call venv/scripts/activate",
        "pip install -r requirements.txt",
        "python main.py"
    ]
else:
    print("Unsupported operating system")
    exit()

# execute the commands in a shell
subprocess.run(' & '.join(commands), shell=True)
