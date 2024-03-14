from modules.bot_state import state_manager


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
