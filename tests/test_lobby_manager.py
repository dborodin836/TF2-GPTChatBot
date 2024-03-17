from modules.lobby_manager import find_username


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
