import modules.conversation_history
from modules.conversation_history import ConversationHistory
from modules.typing import Message
from modules.utils.prompts import load_prompts
from tests.common import MockConfig


def test_empty(mocker):
    conf = MockConfig()
    mocker.patch.object(modules.conversation_history, "config", conf)
    convh = ConversationHistory()

    assert convh.custom_prompt == ""
    assert convh.enable_soft_limit is True
    assert convh.enable_stats is False
    assert convh.message_history == []
    assert convh.get_messages_array() == [
        Message(role="system", content=f"Answer in less than {conf.SOFT_COMPLETION_LIMIT} chars!")
    ]


def test_basic(mocker):
    conf = MockConfig()
    mocker.patch.object(modules.conversation_history, "config", conf)
    convh = ConversationHistory()

    convh.add_user_message_from_prompt("2+2?")
    assert convh.get_messages_array() == [
        {"content": f"Answer in less than {conf.SOFT_COMPLETION_LIMIT} chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]
    assert convh.message_history == [{"content": "2+2?", "role": "user"}]

    convh.add_assistant_message(Message(role="assistant", content="4"))
    assert convh.get_messages_array() == [
        {"content": f"Answer in less than {conf.SOFT_COMPLETION_LIMIT} chars!", "role": "system"},
        {"content": "2+2?", "role": "user"},
        {"content": "4", "role": "assistant"},
    ]
    assert convh.message_history == [
        {"content": "2+2?", "role": "user"},
        {"content": "4", "role": "assistant"},
    ]


def test_with_flags(mocker):
    custom_prompt = "test_prompt"

    # Config setup
    conf = MockConfig()
    mocker.patch.object(modules.conversation_history, "config", conf)
    convh = ConversationHistory()

    # Prompts setup
    mocker.patch("modules.utils.prompts.os.listdir", return_value=["medic.txt"])
    mocker.patch("codecs.open", mocker.mock_open(read_data=custom_prompt))
    load_prompts()

    # Testing long "\l" argument
    convh.add_user_message_from_prompt(r"\l 2+2?")
    assert convh.get_messages_array() == [
        {"content": "", "role": "system"},
        {"content": "2+2?", "role": "user"},
    ]

    convh.add_assistant_message(Message(role="assistant", content="4"))
    assert convh.message_history == [
        {"content": "2+2?", "role": "user"},
        {"content": "4", "role": "assistant"},
    ]

    # Testing custom prompt argument "\medic" and "\l"
    convh.reset()

    convh.add_user_message_from_prompt(r"\medic \l Hi!")
    assert convh.custom_prompt == custom_prompt
    assert convh.enable_soft_limit is False
    assert convh.get_messages_array() == [
        {"role": "system", "content": custom_prompt},
        {"role": "user", "content": "Hi!"},
    ]

    convh.add_assistant_message(Message(role="assistant", content="Hi! (as medic)"))
    assert convh.custom_prompt == custom_prompt
    assert convh.enable_soft_limit is True
    assert convh.message_history == [
        {"content": "Hi!", "role": "user"},
        {"content": "Hi! (as medic)", "role": "assistant"},
    ]
