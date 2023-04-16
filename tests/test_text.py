from utils.text import has_cyrillic, get_chunks, get_chunk_size

MAX_LENGTH_CYRILLIC = 65
MAX_LENGTH_OTHER = 120


def test_has_cyrillic():
    assert has_cyrillic('Привет, мир!') is True
    assert has_cyrillic('Hello, world!') is False


def test_get_chunks():
    string = "Hello world, how are you doing today?"
    maxlength = 10
    expected_output = ['Hello', 'world, how', 'are you', 'doing', 'today?']

    for item in get_chunks(string, maxlength):
        assert len(item) <= maxlength

    assert list(get_chunks(string, maxlength)) == expected_output

    assert ' '.join(get_chunks(string, maxlength)) == string


def test_get_chunk_size_with_cyrillic_text():
    # Test the function with Cyrillic text
    text = "Привет, мир!"
    assert get_chunk_size(text) == MAX_LENGTH_CYRILLIC


def test_get_chunk_size_with_non_cyrillic_text():
    # Test the function with non-Cyrillic text
    text = "Hello, world!"
    assert get_chunk_size(text) == MAX_LENGTH_OTHER
