from utils.commands import print_help_command
from utils.bot_state import start_bot, stop_bot, get_bot_state


def test_print_help_command(capsys):
    print_help_command()
    captured = capsys.readouterr()
    assert "start - start the bot" in captured.out
    assert "stop - stop the bot" in captured.out
    assert "quit - quit the program" in captured.out
    assert "bans - show all banned players" in captured.out
    assert "ban <username> - ban user by username" in captured.out
    assert "unban <username> - unban user by username" in captured.out
    assert "gpt3 <prompt> - sends a response to GPT3" in captured.out


def test_start_bot():
    start_bot()
    assert get_bot_state() is True


def test_stop_bot():
    stop_bot()
    assert get_bot_state() is False


def test_get_bot_state():
    start_bot()
    assert get_bot_state() is True

    stop_bot()
    assert get_bot_state() is False
