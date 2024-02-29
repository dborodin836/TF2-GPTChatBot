import sys

from modules.command_controllers import GuiCommandController
from modules.commands.gui.bans import handle_ban, handle_list_bans, handle_unban
from modules.commands.gui.openai import handle_gpt3
from modules.commands.gui.state import handle_start, handle_stop

command_controller = GuiCommandController()
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