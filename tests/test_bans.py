from modules.bans import BansManager
from tests.common import get_player, temp_file


def test_is_banned_username(temp_file):
    bans_manager = BansManager(temp_file)
    plr1 = get_player("player1", 1)
    plr2 = get_player("player2", 2)
    plr3 = get_player("player3", 3)

    bans_manager.ban_player(plr1)
    bans_manager.ban_player(plr2)

    assert bans_manager.is_banned_player(plr1) is True
    assert bans_manager.is_banned_player(plr3) is False


def test_list_banned_players(capsys, temp_file):
    bans_manager = BansManager(temp_file)

    plr1 = get_player("player1", 1)
    plr2 = get_player("player2", 2)

    bans_manager.ban_player(plr1)
    bans_manager.ban_player(plr2)

    ban_list = bans_manager.banned_players_steamid3
    assert plr1.steamid3 in ban_list
    assert plr2.steamid3 in ban_list

    # Test with no bans
    bans_manager.banned_players_steamid3 = set()
    ban_list = bans_manager.banned_players_steamid3
    assert len(ban_list) == 0


def test_unban_player(temp_file):
    bans_manager = BansManager(temp_file)

    plr1 = get_player("player1", 1)

    assert bans_manager.banned_players_steamid3 == set()
    bans_manager.ban_player(plr1)
    assert bans_manager.banned_players_steamid3 == {plr1.steamid3}
    bans_manager.unban_player(plr1)
    assert bans_manager.banned_players_steamid3 == set()


def test_ban_player(temp_file):
    bans_manager = BansManager(temp_file)

    plr1 = get_player("player1", 1)

    bans_manager.ban_player(plr1)
    bans_manager.load_banned_players()
    assert plr1.steamid3 in bans_manager.banned_players_steamid3


def test_ban_twice(temp_file):
    bans_manager = BansManager(temp_file)

    plr1 = get_player("player1", 1)

    bans_manager.ban_player(plr1)
    bans_manager.load_banned_players()
    bans_manager.ban_player(plr1)
    assert plr1.steamid3 in bans_manager.banned_players_steamid3


def test_unban_twice(temp_file):
    bans_manager = BansManager(temp_file)
    plr1 = get_player("player1", 1)

    bans_manager.ban_player(plr1)
    bans_manager.load_banned_players()
    bans_manager.unban_player(plr1)
    bans_manager.unban_player(plr1)
    assert plr1.steamid3 not in bans_manager.banned_players_steamid3
