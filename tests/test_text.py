from modules.typing import Message, LogLine
from modules.utils.text import (
    get_system_message,
    get_chunk_size,
    has_cyrillic,
    split_into_chunks,
    get_args,
    parse_line
)

MAX_LENGTH_CYRILLIC = 65
MAX_LENGTH_OTHER = 120


def test_has_cyrillic():
    assert has_cyrillic("Привет, мир!") is True
    assert has_cyrillic("Hello, world!") is False


def test_get_chunks():
    string = "Hello world, how are you doing today?"
    maxlength = 10
    expected_output = ["Hello", "world, how", "are you", "doing", "today?"]

    for item in split_into_chunks(string, maxlength):
        assert len(item) <= maxlength

    assert list(split_into_chunks(string, maxlength)) == expected_output

    assert " ".join(split_into_chunks(string, maxlength)) == string


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


def test_parse_line_tf2bd():
    line = "\u200d\u200d\u200d\u2060\u2060\u200djeff\ufeff\u2060\u200b :  \u200d\u200b\u200b!cgpt 2+2\u2060\u200b\u200b\u2060\ufeff\ufeff"
    assert parse_line(line) == LogLine(prompt='!cgpt 2+2', username='jeff', is_team_message=False)

    line = "(TEAM) jeff :  !cgpt 2+2"
    assert parse_line(line) == LogLine(prompt='!cgpt 2+2', username='jeff', is_team_message=True)

    line = "*DEAD*(TEAM) jeff :  !cgpt 2+2"
    assert parse_line(line) == LogLine(prompt='!cgpt 2+2', username='jeff', is_team_message=True)

    line = "*DEAD*(TEAM) jeff : !cgpt 2+2"
    assert parse_line(line) == LogLine(prompt='!cgpt 2+2', username='jeff', is_team_message=True)

    line = "*DEAD*(TEAM) jeff : !cgpt yo dude help me"
    assert parse_line(line) == LogLine(prompt='!cgpt yo dude help me', username='jeff', is_team_message=True)

    # TODO: fix bugs
    # line = "*DEAD*(TEAM) jeff : !cgpt hey : dude"
    # assert parse_line(line) == LogLine(prompt='!cgpt hey : dude', username='jeff', is_team_message=True)
    #
    # line = "*DEAD*(TEAM) jeff : !cgpt hey :  dude"
    # assert parse_line(line) == LogLine(prompt='!cgpt hey :  dude', username='jeff', is_team_message=True)


