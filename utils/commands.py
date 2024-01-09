from utils.logs import get_logger

main_logger = get_logger("main")
gui_logger = get_logger("gui")
combo_logger = get_logger("combo")


def print_help_command():
    """
    Prints the available commands and their descriptions.
    """
    gui_logger.info(
        "### HELP ###",
        "start - start the bot",
        "stop - stop the bot",
        "quit - quit the program",
        "bans - show all banned players",
        "ban <username> - ban user by username",
        "unban <username> - unban user by username",
        "gpt3 <prompt> - sends a response to GPT3",
        sep="\n",
    )


