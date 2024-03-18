from modules.command_controllers import ChatHistoryManager
from tests.common import get_player


def test_chat_conversation_history_basic():
    chm = ChatHistoryManager()
    pl1 = get_player("user1", 1)

    # global chat is empty
    assert chm.GLOBAL.message_history == []

    # No user chats exist on init
    user_chats_keys = [x for x in list(chm.__dict__) if x.startswith("USER_")]
    assert len(user_chats_keys) == 0

    # test creation
    chm.get_conversation_history(pl1)
    user_chats_keys = [x for x in list(chm.__dict__) if x.startswith("USER_")]
    assert len(user_chats_keys) == 1
    assert chm._get_conv_history_attr_name(pl1.steamid64) in user_chats_keys


def test_chat_conversation_history_isolation():
    chm = ChatHistoryManager()

    # global chat is empty
    assert chm.GLOBAL.message_history == []

    pl1 = get_player("user1", 1)
    pl2 = get_player("user2", 2)

    # Create 2 user chats
    cvh1 = chm.get_conversation_history(pl1)
    cvh2 = chm.get_conversation_history(pl2)
    user_chats_keys = [x for x in list(chm.__dict__) if x.startswith("USER_")]
    assert len(user_chats_keys) == 2

    # test isolation
    assert cvh1 is not cvh2
    cvh1.add_user_message_from_prompt(r"\l hello")
    assert cvh1.message_history == [{'content': 'hello', 'role': 'user'}]
    assert cvh1.enable_soft_limit is False

    assert cvh2.message_history == []
    assert cvh2.enable_soft_limit is True



