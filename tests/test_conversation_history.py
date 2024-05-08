from modules.conversation_history import ConversationHistory
from modules.typing import Message
from modules.utils.prompts import load_prompts


def test_empty():
    chat = ConversationHistory()

    assert chat.custom_prompt == ""
    assert chat.enable_soft_limit is True
    assert chat.enable_stats is False
    assert chat.message_history == []
    assert chat.get_messages_array() == [
        Message(role="system", content="Answer in less than 128 chars!")
    ]


def test_basic():
    chat = ConversationHistory()

    chat.add_user_message_from_prompt("2+2?")
    assert chat.get_messages_array() == [
        {"content": "Answer in less than 128 chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]
    assert chat.message_history == [{"content": "2+2?", "role": "user"}]

    chat.add_assistant_message(Message(role="assistant", content="4"))
    assert chat.get_messages_array() == [
        {"content": "Answer in less than 128 chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
        {"content": "4", "role": "assistant"},
    ]
    assert chat.message_history == [
        {"content": "2+2?", "role": "user"},
        {"content": "4", "role": "assistant"},
    ]


def test_settings_greeting():
    chat_settings = {
        "greeting": "TEST_GREETING"
    }
    chat = ConversationHistory(chat_settings)

    chat.add_user_message_from_prompt("2+2?")
    assert chat.get_messages_array() == [
        {"content": "Answer in less than 128 chars!", "role": "system"},
        {"content": "TEST_GREETING", "role": "assistant"},
        {"content": "2+2?", "role": "user"},
    ]

    chat.add_assistant_message(Message(content="4", role="assistant"))
    assert chat.get_messages_array() == [
        {"content": "Answer in less than 128 chars!", "role": "system"},
        {"content": "TEST_GREETING", "role": "assistant"},
        {"content": "2+2?", "role": "user"},
        {"content": "4", "role": "assistant"}
    ]

    chat.reset()
    chat.settings["greeting"] = None
    chat.add_user_message_from_prompt("2+2?")
    assert chat.get_messages_array() == [
        {"content": "Answer in less than 128 chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]


def test_settings_message_suffix():
    chat_settings = {
        "message-suffix": "MESSAGE_SUFFIX"
    }
    chat = ConversationHistory(chat_settings)

    chat.add_user_message_from_prompt("2+2?")
    assert chat.get_messages_array() == [
        {"content": "Answer in less than 128 chars! MESSAGE_SUFFIX", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]

    chat.add_assistant_message(Message(content='4', role="assistant"))
    chat.add_user_message_from_prompt("4+4")
    assert chat.get_messages_array() == [
        {'content': 'Answer in less than 128 chars! MESSAGE_SUFFIX', 'role': 'system'},
        {'content': '2+2?', 'role': 'user'},
        {'content': '4', 'role': 'assistant'},
        {'content': '4+4', 'role': 'user'}
    ]

    chat.reset()
    chat.settings['message-suffix'] = None
    chat.add_user_message_from_prompt("2+2?")
    assert chat.get_messages_array() == [
        {"content": "Answer in less than 128 chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]


def test_settings_allow_long():
    chat_settings = {
        "allow-long": False,
    }
    chat = ConversationHistory(chat_settings)

    chat.add_user_message_from_prompt("\l 2+2?")
    assert chat.get_messages_array() == [
        {"content": "Answer in less than 128 chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]

    chat.reset()
    chat.settings['allow-long'] = True
    chat.add_user_message_from_prompt("\l 2+2?")
    assert chat.get_messages_array() == [
        {"content": "", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]


def test_settings_soft_limit():
    chat_settings = {
        "soft-limit-length": 669,
        "enable-soft-limit": True,
    }
    chat = ConversationHistory(chat_settings)

    chat.add_user_message_from_prompt("2+2?")
    assert chat.get_messages_array() == [
        {"content": "Answer in less than 669 chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]

    chat.reset()
    chat.settings['enable-soft-limit'] = False
    chat.add_user_message_from_prompt("2+2?")
    assert chat.get_messages_array() == [
        {"content": "", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]


def test_with_flags(mocker):
    custom_prompt = "test_prompt"

    # Config setup
    chat = ConversationHistory()

    # Prompts setup
    mocker.patch("modules.utils.prompts.os.listdir", return_value=["medic.txt"])
    mocker.patch("codecs.open", mocker.mock_open(read_data=custom_prompt))
    load_prompts()

    # Testing long "\l" argument
    chat.add_user_message_from_prompt(r"\l 2+2?")
    assert chat.get_messages_array() == [
        {"content": "", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]

    chat.add_assistant_message(Message(role="assistant", content="4"))
    assert chat.message_history == [
        {"content": "2+2?", "role": "user"},
        {"content": "4", "role": "assistant"},
    ]

    # Testing custom prompt argument "\medic" and "\l"
    chat.reset()

    chat.add_user_message_from_prompt(r"\medic \l Hi!")
    assert chat.custom_prompt == custom_prompt
    assert chat.enable_soft_limit is False
    assert chat.get_messages_array() == [
        {"role": "system", "content": custom_prompt},
        {"role": "user", "content": "Hi!"},
    ]

    chat.add_assistant_message(Message(role="assistant", content="Hi! (as medic)"))
    assert chat.custom_prompt == custom_prompt
    assert chat.enable_soft_limit is True
    assert chat.message_history == [
        {"content": "Hi!", "role": "user"},
        {"content": "Hi! (as medic)", "role": "assistant"},
    ]


def test_settings_prompt_file(mocker):
    custom_prompt = "test_prompt"
    chat_settings = {
        "prompt-file": "medic"
    }
    chat = ConversationHistory(chat_settings)

    mocker.patch("modules.utils.prompts.os.listdir", return_value=["medic.txt"])
    mocker.patch("codecs.open", mocker.mock_open(read_data=custom_prompt))
    load_prompts()

    chat.add_user_message_from_prompt("2+2?")
    assert chat.get_messages_array() == [
        {"content": "test_prompt Answer in less than 128 chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]

    chat.add_assistant_message(Message(content="4", role="assistant"))
    assert chat.get_messages_array() == [
        {"content": "test_prompt Answer in less than 128 chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
        {"content": "4", "role": "assistant"}
    ]

    chat.add_user_message_from_prompt('\clear 3+3?')
    assert chat.get_messages_array() == [
        {"content": "test_prompt Answer in less than 128 chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
        {"content": "4", "role": "assistant"},
        {"content": "3+3?", "role": "user"},
    ]

    chat.reset()
    chat.settings["prompt-file"] = None
    chat.add_user_message_from_prompt("2+2?")
    assert chat.get_messages_array() == [
        {"content": "Answer in less than 128 chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]
