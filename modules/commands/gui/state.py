from modules.bot_state import state_manager


def handle_stop(command, shared_dict):
    state_manager.stop_bot()


def handle_start(command, shared_dict):
    state_manager.start_bot()
