from modules.typing import Message
from modules.utils.text import (
    get_system_message,
    get_chunk_size,
    has_cyrillic,
    split_into_chunks, get_args,
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
