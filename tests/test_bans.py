import os
from unittest.mock import patch
from utils import bans

# Set up test data
BANS_FILE = 'test_bans.json'
TEST_BANNED_PLAYERS = {'player1', 'player2'}


def setup_module(module):
    # Create a test bans file
    with open(BANS_FILE, 'w') as f:
        f.write('["player1", "player2"]')
    bans.BANS_FILE = BANS_FILE


def teardown_module(module):
    # Delete the test bans file
    os.remove(BANS_FILE)


def test_load_banned_players():
    banned_players = bans.load_banned_players()
    assert banned_players == TEST_BANNED_PLAYERS


def test_is_banned_username():
    bans.BANNED_PLAYERS = set()
    bans.ban_player("player1")
    bans.ban_player("player2")
    assert bans.is_banned_username('player1') is True
    assert bans.is_banned_username('player3') is False


def test_list_banned_players(capsys):
    bans.BANNED_PLAYERS = set()
    bans.ban_player("player1")
    bans.ban_player("player2")
    bans.list_banned_players()
    captured = capsys.readouterr()
    assert "### BANNED PLAYERS ###\nplayer1\nplayer2\n" in captured.out \
           or "### BANNED PLAYERS ###\nplayer2\nplayer1\n" in captured.out

    # Test with no bans
    bans.BANNED_PLAYERS = set()
    bans.list_banned_players()
    captured = capsys.readouterr()
    assert captured.out == "### NO BANS ###\n"


def test_unban_player():
    with patch('utils.bans.log_cmd_message') as mock_log_cmd_message:
        bans.unban_player('player1')
        banned_players = bans.load_banned_players()
        assert 'player1' not in banned_players
        mock_log_cmd_message.assert_called_once_with("UNBANNED 'player1'")


def test_ban_player():
    with patch('utils.bans.log_cmd_message') as mock_log_cmd_message:
        bans.ban_player('player3')
        banned_players = bans.load_banned_players()
        assert 'player3' in banned_players
        mock_log_cmd_message.assert_called_once_with("BANNED 'player3'")
