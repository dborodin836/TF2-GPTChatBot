import sys
import subprocess

# detect the user's operating system
os_name = sys.platform

# run the commands depending on the os
if os_name.startswith("linux"):
    commands = [
        "python3 -m venv venv",
        "source venv/scripts/activate",
        "pip install -r requirements.txt",
        "python main.py"
    ]
elif os_name.startswith("win"):
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
for command in commands:
    subprocess.run(command, shell=True)
