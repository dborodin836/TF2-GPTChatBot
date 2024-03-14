import os
import tempfile

import pytest

from modules.bans import BansManager


@pytest.fixture
def temp_ban_file():
    # Create a temporary file and get its name
    fd, path = tempfile.mkstemp()

    # Pre-test setup: Close the file descriptor as we don't need it
    os.close(fd)

    # Provide the temporary file path to the test
    yield path

    # Post-test teardown: Remove the temporary file
    os.remove(path)


def test_is_banned_username(temp_ban_file):
    bans_manager = BansManager(temp_ban_file)
    bans_manager.banned_usernames = set()
    bans_manager.ban_player("player1")
    bans_manager.ban_player("player2")
    assert bans_manager.is_banned_username("player1") is True
    assert bans_manager.is_banned_username("player3") is False


def test_list_banned_players(capsys, temp_ban_file):
    bans_manager = BansManager(temp_ban_file)
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


def test_unban_player(temp_ban_file):
    bans_manager = BansManager(temp_ban_file)
    bans_manager.banned_usernames = set()
    assert bans_manager.banned_usernames == set()
    bans_manager.ban_player("test1")
    assert bans_manager.banned_usernames == {"test1"}
    bans_manager.unban_player("test1")
    assert bans_manager.banned_usernames == set()


def test_ban_player(temp_ban_file):
    bans_manager = BansManager(temp_ban_file)
    bans_manager.ban_player("player3")
    bans_manager.load_banned_players()
    assert "player3" in bans_manager.banned_usernames


def test_ban_twice(temp_ban_file):
    bans_manager = BansManager(temp_ban_file)
    bans_manager.ban_player("player")
    bans_manager.load_banned_players()
    bans_manager.ban_player("player")
    assert "player" in bans_manager.banned_usernames


def test_unban_twice(temp_ban_file):
    bans_manager = BansManager(temp_ban_file)
    bans_manager.ban_player("player")
    bans_manager.load_banned_players()
    bans_manager.unban_player("player")
    bans_manager.unban_player("player")
    assert "player" not in bans_manager.banned_usernames
