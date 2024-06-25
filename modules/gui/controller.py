import sys

from modules.command_controllers import GuiCommandController
from modules.commands.gui.audio import handle_list_devices
from modules.commands.gui.bans import handle_ban, handle_list_bans, handle_unban
from modules.commands.gui.config import handle_config
from modules.commands.gui.invoke import invoke
from modules.commands.gui.openai import handle_gpt3
from modules.commands.gui.state import handle_start, handle_stop

config_command_description = """Commands to manipulate config file.
   - reload - reloads config file from disk
   - set <name>=<value> ... - set value(s) in config (session)
   - get <name> ... - get value(s) from the config
   - save <filename> - write current session config to a file
   - load <filename> - load config from disk
   - dump - prints whole config to console"""

command_controller = GuiCommandController()
command_controller.register_command("@", invoke, "Invoke any non-gui command.")
command_controller.register_command("stop", handle_stop, "Start the bot.")
command_controller.register_command("start", handle_start, "Stop the bot.")
command_controller.register_command("ban", handle_ban, "Ban user by username. e.g ban <username>")
command_controller.register_command(
    "unban", handle_unban, "Unban user by username. e.g unban <username>"
)
command_controller.register_command("bans", handle_list_bans, "Show all banned players.")
command_controller.register_command(
    "gpt3", handle_gpt3, "Send a response to GPT3 model. e.g gpt3 <prompt>"
)
command_controller.register_command("quit", lambda *args: sys.exit(0), "Quit the program.")
command_controller.register_command("config", handle_config, config_command_description)
command_controller.register_command("audio-devices", handle_list_devices, "List output audio devices.")
