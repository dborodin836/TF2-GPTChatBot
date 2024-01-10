from modules.utils.text import add_prompts_by_flags, get_chunk_size, split_into_chunks, has_cyrillic

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


def test_add_prompts_by_flags():
    expected_output = "Please enter your name"
    result = add_prompts_by_flags(r"\l Please enter your name")
    assert result == expected_output
