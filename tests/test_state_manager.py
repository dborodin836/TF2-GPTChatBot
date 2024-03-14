from modules.bot_state import StateManager


def test_start():
    state_manager = StateManager()
    assert state_manager.bot_running is True
    state_manager.start_bot()
    assert state_manager.bot_running is True


def test_stop():
    state_manager = StateManager()
    assert state_manager.bot_running is True
    state_manager.stop_bot()
    assert state_manager.bot_running is False


def test_manual_restart():
    state_manager = StateManager()
    assert state_manager.bot_running is True
    state_manager.stop_bot()
    assert state_manager.bot_running is False
    state_manager.start_bot()
    assert state_manager.bot_running is True


def test_switch():
    state_manager = StateManager()
    assert state_manager.bot_running is True
    state_manager.switch_state()
    assert state_manager.bot_running is False
    state_manager.switch_state()
    assert state_manager.bot_running is True
