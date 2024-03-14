import logging

from modules.utils.prompts import load_prompts, PROMPTS


def test_load_prompts(mocker, caplog):
    mocker.patch("modules.utils.prompts.os.listdir",
                 return_value=["medic_test.txt", "demoman_test.txt", "heavy.md", "warrior.png"])
    mocker.patch("codecs.open", mocker.mock_open(read_data="test_prompt"))
    with caplog.at_level(logging.DEBUG):
        load_prompts()

    assert len(PROMPTS) == 2
    assert "Loaded 2 models!" in caplog.text
