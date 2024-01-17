from modules.bot_state import state_manager

# def test_print_help_command(capsys):
#     print_help_command()
#     captured = capsys.readouterr()
#     assert "start - start the bot" in captured.out
#     assert "stop - stop the bot" in captured.out
#     assert "quit - quit the program" in captured.out
#     assert "bans - show all banned players" in captured.out
#     assert "ban <username> - ban user by username" in captured.out
#     assert "unban <username> - unban user by username" in captured.out
#     assert "gpt3 <prompt> - sends a response to GPT3" in captured.out


def test_start_bot():
    state_manager.start_bot()
    assert state_manager.bot_running is True


def test_stop_bot():
    state_manager.stop_bot()
    assert state_manager.bot_running is False


def test_get_bot_state():
    state_manager.start_bot()
    assert state_manager.bot_running is True

    state_manager.stop_bot()
    assert state_manager.bot_running is False
