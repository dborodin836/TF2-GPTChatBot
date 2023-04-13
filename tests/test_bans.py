import pytest
import os

from utils.bans import load_banned_players, BANS_FILE


@pytest.fixture
def setup_bans_file(tmpdir):
    """
    Creates a temporary bans file for testing.
    """
    bans_file = tmpdir.join(BANS_FILE)
    with open(str(bans_file), 'w') as f:
        f.write('["player1", "player2", "player3"]')
    return bans_file


def test_load_banned_players(setup_bans_file):
    """
    Tests if load_banned_players returns the expected set of banned players.
    """
    # Arrange
    expected_banned_players = {"player1", "player2", "player3"}

    with open('test_bans.json', 'w') as f:
        f.write('["player1", "player2", "player3"]')

    # Act
    banned_players = load_banned_players()

    # Assert
    assert banned_players == expected_banned_players
