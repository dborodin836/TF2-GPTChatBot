from modules.utils.steam import steamid3_to_steamid64


def test_steamid3_to_steamid64():
    assert steamid3_to_steamid64("[U:1:220946399]") == 76561198181212127
