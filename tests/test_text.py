import time

import modules.utils.text
from modules.lobby_manager import LobbyManager
from modules.typing import Message, LogLine, Player
from modules.utils.text import (
    get_system_message,
    get_chunk_size,
    has_cyrillic,
    split_into_chunks,
    get_args,
    parse_line,
    get_shortened_username,
    remove_hashtags,
    get_chunks,
    get_console_logline
)
from tests.common import MockConfig, get_player

MAX_LENGTH_CYRILLIC = 65
MAX_LENGTH_OTHER = 120


def test_has_cyrillic():
    assert has_cyrillic("Привет, мир!") is True
    assert has_cyrillic("Hello, world!") is False


def test_split_into_chunks():
    string = "Hello world, how are you doing today?"
    maxlength = 10
    expected_output = ["Hello", "world, how", "are you", "doing", "today?"]

    for item in split_into_chunks(string, maxlength):
        assert len(item) <= maxlength

    assert list(split_into_chunks(string, maxlength)) == expected_output

    assert " ".join(split_into_chunks(string, maxlength)) == string


def test_get_chunk():
    text = (
        "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the "
        "industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and "
        "scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into"
        " electronic typesetting, remaining essentially unchanged."
    )

    assert list(get_chunks(text)) == ['Lorem Ipsum is simply dummy text of the printing and typesetting industry. '
                                      "Lorem Ipsum has been the industry's standard",
                                      'dummy text ever since the 1500s, when an unknown printer took a galley of '
                                      'type and scrambled it to make a type specimen',
                                      'book. It has survived not only five centuries, but also the leap into '
                                      'electronic typesetting, remaining essentially',
                                      'unchanged.']


def test_get_chunk_size_with_cyrillic_text():
    # Test the function with Cyrillic text
    text = "Привет, мир!"
    assert get_chunk_size(text) == MAX_LENGTH_CYRILLIC


def test_get_chunk_size_with_non_cyrillic_text():
    # Test the function with non-Cyrillic text
    text = "Hello, world!"
    assert get_chunk_size(text) == MAX_LENGTH_OTHER


def test_get_system_message():
    expected_output = Message(role="system", content="")
    result = get_system_message(r"\l Please enter your name")
    assert result == expected_output


def test_get_args():
    assert get_args(r'\user="123" \global') == [r'\user="123"', r'\global']
    assert get_args(r"\user='123' \global") == [r"\user='123'", r'\global']
    assert get_args(r'\user="123 123" \global') == [r'\user="123 123"', r'\global']
    assert get_args(r"\user='123 123' \global") == [r"\user='123 123'", r'\global']
    assert get_args(r"\medic Hi dude!") == [r"\medic"]
    assert get_args(r"\medic Hi dude! 'some text'") == [r"\medic"]
    assert get_args(r'\medic Hi dude! "some text"') == [r"\medic"]
    assert get_args(r"\medic \l Hi dude!") == [r"\medic", r"\l"]


def test_get_shortened_username(mocker):
    conf = MockConfig()
    mocker.patch.object(modules.utils.text, "config", conf)

    assert get_shortened_username("silly goose") == "[silly goose] "
    assert get_shortened_username("really really long username") == "[really reall..] "


def test_remove_hashtags():
    assert remove_hashtags("blah-blah-blah #blah #blah") == "blah-blah-blah"
    assert remove_hashtags("#blah blah-blah-blah #blah") == "blah-blah-blah"


def test_get_console_logline(mocker):
    conf = MockConfig()
    lobby_manager = LobbyManager()

    def follow_tail_overwrite(x: str):
        text = [
            "03/21/2024 - 20:20:51: #      3 \"silly goose\"       [U:1:220946399]     01:06      111    0 active",
            "03/69/2024 - 20:20:55: *SPEC* [Owner]silly goose :  !gpt3 test",
            "03/69/2024 - 20:20:58: [Owner]silly goose :  !gpt3 test2",
            "03/69/2024 - 20:20:58: [Owner]silly goose :  !gpt3 test2",
        ]
        for i in text:
            yield i

    mocker.patch.object(modules.utils.text, "follow_tail", follow_tail_overwrite)
    mocker.patch.object(modules.utils.text, "get_status", lambda: ...)
    mocker.patch.object(modules.utils.text, "config", conf)
    mocker.patch.object(modules.utils.text, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.lobby_manager, "config", conf)
    mocker.patch.object(time, "time", lambda: 1)

    gen = get_console_logline()

    assert next(gen) == LogLine(prompt='!gpt3 test', username='silly goose', is_team_message=False,
                                player=Player(name='silly goose', steamid3='[U:1:220946399]',
                                              steamid64=76561198181212127, kills=0, melee_kills=0, crit_melee_kills=0,
                                              deaths=0, minutes_on_server=1, last_updated=1, ping_list=[], ping=111))

    assert next(gen) == LogLine(prompt='!gpt3 test2', username='silly goose', is_team_message=False,
                                player=Player(name='silly goose', steamid3='[U:1:220946399]',
                                              steamid64=76561198181212127, kills=0, melee_kills=0, crit_melee_kills=0,
                                              deaths=0, minutes_on_server=1, last_updated=1, ping_list=[], ping=111))


def test_get_tf2bd(mocker):
    conf = MockConfig()
    lobby_manager = LobbyManager()

    def follow_tail_overwrite(x: str):
        text = [
            "03/21/2024 - 20:20:51: #      3 \"jeff\"       [U:1:220946399]     01:06      111    0 active",
            "03/69/2024 - 20:20:58: \u200d\u200d\u200d\u2060\u2060\u200djeff\ufeff\u2060\u200b :  \u200d\u200b\u200b!gpt3 2+2\u2060\u200b\u200b\u2060\ufeff\ufeff"
        ]
        for i in text:
            yield i

    mocker.patch.object(modules.utils.text, "follow_tail", follow_tail_overwrite)
    mocker.patch.object(modules.utils.text, "get_status", lambda: ...)
    mocker.patch.object(modules.utils.text, "config", conf)
    mocker.patch.object(modules.utils.text, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.lobby_manager, "config", conf)
    mocker.patch.object(time, "time", lambda: 1)

    gen = get_console_logline()

    assert next(gen) == LogLine(prompt='!gpt3 2+2', username='jeff', is_team_message=False,
                                player=Player(name='jeff', steamid3='[U:1:220946399]',
                                              steamid64=76561198181212127, kills=0, melee_kills=0,
                                              crit_melee_kills=0, deaths=0, minutes_on_server=1, last_updated=1,
                                              ping_list=[], ping=111))


def test_parse_line_tf2bd(mocker):
    lobby_manager = LobbyManager()
    cfg = MockConfig()
    mocker.patch.object(modules.utils.text, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.lobby_manager, "config", cfg)

    pl = get_player("jeff", 1)
    lobby_manager.add_player(pl)

    line = "(TEAM) jeff :  !cgpt 2+2"
    assert parse_line(line) == LogLine(prompt='!cgpt 2+2', username='jeff', is_team_message=True, player=pl)

    line = "*DEAD*(TEAM) jeff :  !cgpt 2+2"
    assert parse_line(line) == LogLine(prompt='!cgpt 2+2', username='jeff', is_team_message=True, player=pl)

    line = "*DEAD*(TEAM) jeff : !cgpt 2+2"
    assert parse_line(line) == LogLine(prompt='!cgpt 2+2', username='jeff', is_team_message=True, player=pl)

    line = "*DEAD*(TEAM) jeff : !cgpt yo dude help me"
    assert parse_line(line) == LogLine(prompt='!cgpt yo dude help me', username='jeff', is_team_message=True, player=pl)

    # TODO: fix bugs
    # line = "*DEAD*(TEAM) jeff : !cgpt hey : dude"
    # assert parse_line(line) == LogLine(prompt='!cgpt hey : dude', username='jeff', is_team_message=True)
    #
    # line = "*DEAD*(TEAM) jeff : !cgpt hey :  dude"
    # assert parse_line(line) == LogLine(prompt='!cgpt hey :  dude', username='jeff', is_team_message=True)
