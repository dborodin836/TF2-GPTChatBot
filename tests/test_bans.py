import os
from unittest.mock import patch

from modules.bans import BansManager

# Set up test data
BANS_FILE = "test_bans.json"
TEST_BANNED_PLAYERS = {"player1", "player2"}

bans_manager = BansManager(bans_file=BANS_FILE)


def setup_module(module):
    # Create a test bans file
    with open(BANS_FILE, "w") as f:
        f.write('["player1", "player2"]')
    bans_manager.load_banned_players()


def teardown_module(module):
    # Delete the test bans file
    os.remove(BANS_FILE)


def test_load_banned_players():
    assert bans_manager.banned_usernames == TEST_BANNED_PLAYERS


def test_is_banned_username():
    bans_manager.banned_usernames = set()
    bans_manager.ban_player("player1")
    bans_manager.ban_player("player2")
    assert bans_manager.is_banned_username("player1") is True
    assert bans_manager.is_banned_username("player3") is False


def test_list_banned_players(capsys):
    bans_manager.banned_usernames = set()
    bans_manager.ban_player("player1")
    bans_manager.ban_player("player2")
    ban_list = bans_manager.banned_usernames
    assert "player1" in ban_list
    assert "player2" in ban_list

    # Test with no bans
    bans_manager.banned_usernames = set()
    ban_list = bans_manager.banned_usernames
    assert len(ban_list) == 0


def test_unban_player():
    assert bans_manager.banned_usernames == set()
    bans_manager.ban_player("test1")
    assert bans_manager.banned_usernames == {"test1"}
    bans_manager.unban_player("test1")
    assert bans_manager.banned_usernames == set()


def test_ban_player():
    with patch("modules.logs.log_gui_general_message") as mock_log_cmd_message:
        bans_manager.ban_player("player3")
        bans_manager.load_banned_players()
        assert "player3" in bans_manager.banned_usernames
