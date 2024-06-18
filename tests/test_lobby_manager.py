import modules.lobby_manager
from modules.lobby_manager import LobbyManager, find_username
from tests.common import MockConfig, get_player


def test_find_username_basic():
    data = [
        "LOLOL",
        "silly goose",
        "baby",
        "Baby",
        "Boss Baby",
        "pablo.gonzalez.2012",
        "[ADMIN] Not An Admin",
        "Pyro",
        "Pootis",
        "Pootis (1)",
        "Pootis (2)",
        "aaaaa",
        "aaa",
        "aa",
    ]

    # Basic
    assert find_username("TEST", data) == None
    assert find_username("[UWU]Pyro", data) == "Pyro"
    assert find_username("[OWNER]silly goose", data) == "silly goose"
    assert find_username("[GOD]Pootis", data) == "Pootis"
    assert find_username("[VIP]Pootis (1)", data) == "Pootis (1)"
    assert find_username("[GOD]Pootis (2)", data) == "Pootis (2)"

    # Confusing
    assert find_username("Ann", data) == None
    assert find_username("[PRO]Baby", data) == "Baby"
    assert find_username("[PRO]a", data) == None
    assert find_username("[A]a", data) == None
    assert find_username("[A]aa", data) == "aa"
    assert find_username("[A]aaaa", data) == None
    assert find_username("[A]aaaaaaa", data) == None
    assert find_username("[ADMIN]Jotaro", data) == None
    assert find_username("[LOL]Boss B", data) == None


def test_regex_player(mocker):
    lobby_manager = LobbyManager()
    conf = MockConfig()
    mocker.patch.object(modules.lobby_manager, "config", conf)

    line = r'#    878 "silly goose"       [U:1:220946399]     24:31      107    0 active'
    res = lobby_manager.stats_regexes(line)
    assert res is True
    assert lobby_manager.get_player_by_name("silly goose") is not None


def test_regex_map(mocker):
    lobby_manager = LobbyManager()
    conf = MockConfig()
    mocker.patch.object(modules.lobby_manager, "config", conf)

    line = r"Map: ctf_2fort"
    res = lobby_manager.stats_regexes(line)
    assert res is True
    assert lobby_manager.map == "ctf_2fort"


def test_regex_ip(mocker):
    lobby_manager = LobbyManager()
    conf = MockConfig()
    mocker.patch.object(modules.lobby_manager, "config", conf)

    line = r"udp/ip  : 169.254.239.115:45288"
    res = lobby_manager.stats_regexes(line)
    assert res is True
    assert lobby_manager.server_ip == "169.254.239.115:45288"


def test_regex_empty(mocker):
    lobby_manager = LobbyManager()
    conf = MockConfig()
    mocker.patch.object(modules.lobby_manager, "config", conf)

    line = r"nothing :D"
    res = lobby_manager.stats_regexes(line)
    assert res is False


def test_regex_suicide(mocker):
    lobby_manager = LobbyManager()
    conf = MockConfig()
    mocker.patch.object(modules.lobby_manager, "config", conf)
    plr = get_player("Gamer", 1)
    lobby_manager.add_player(plr)

    line = r"Gamer suicided."
    res = lobby_manager.stats_regexes(line)
    assert res is True
    assert lobby_manager.get_player_by_name("Gamer").deaths == 1


def test_regex_kill(mocker):
    lobby_manager = LobbyManager()
    conf = MockConfig()
    mocker.patch.object(modules.lobby_manager, "config", conf)
    plr1 = get_player("Gamer 1", 1)
    plr2 = get_player("Gamer 2", 2)
    lobby_manager.add_player(plr1)
    lobby_manager.add_player(plr2)

    line = r"Gamer 1 killed Gamer 2 with bazaar_bargain. (crit)"
    res = lobby_manager.stats_regexes(line)
    assert res is True
    assert len(lobby_manager.players) == 2

    assert plr1.deaths == 0
    assert plr1.kills == 1

    assert plr2.deaths == 1
    assert plr2.kills == 0
