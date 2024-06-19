from modules.command_controllers import ChatHistoryManager, CommandChatTypes
from tests.common import get_player


def test_chat_conversation_history_basic():
    chat_manager = ChatHistoryManager()
    player_1 = get_player("user1", 1)

    # No user chats exist on init
    assert chat_manager.COMMAND == {}

    # test nonexistent retrieval
    result_none = chat_manager.get_command_chat_history("test", CommandChatTypes.GLOBAL, player_1)
    assert result_none is None

    # test creation global
    result_1 = chat_manager.get_or_create_command_chat_history(
        "test", CommandChatTypes.GLOBAL, {}, player_1
    )
    assert result_1 is not None

    # test creation private
    result_2 = chat_manager.get_or_create_command_chat_history(
        "test", CommandChatTypes.PRIVATE, {}, player_1
    )
    assert result_2 is not None
    assert result_2 != result_1
    assert id(result_2) != id(result_1)


def test_chat_conversation_history_isolation_private():
    chat_manager = ChatHistoryManager()

    player_1 = get_player("user1", 1)
    player_2 = get_player("user2", 2)

    # Create 2 chats
    chat_1 = chat_manager.get_or_create_command_chat_history(
        "test", CommandChatTypes.PRIVATE, {}, player_1
    )
    chat_2 = chat_manager.get_or_create_command_chat_history(
        "test", CommandChatTypes.PRIVATE, {}, player_2
    )
    assert chat_1 != chat_2
    assert id(chat_1) != id(chat_2)

    # test isolation
    chat_1_new = chat_manager.get_command_chat_history("test", CommandChatTypes.PRIVATE, player_1)
    chat_2_new = chat_manager.get_command_chat_history("test", CommandChatTypes.PRIVATE, player_2)
    assert chat_1 is chat_1_new
    assert chat_2 is chat_2_new

    chat_1_new.add_user_message_from_prompt(r"\l hello")
    assert chat_1.message_history == [{"content": "hello", "role": "user"}]
    assert chat_1.enable_soft_limit is False

    assert chat_2.message_history == []
    assert chat_2.enable_soft_limit is True


def test_chat_conversation_history_isolation_global():
    chat_manager = ChatHistoryManager()

    player_1 = get_player("user1", 1)
    player_2 = get_player("user2", 2)

    # Create 2 chats
    chat_1 = chat_manager.get_or_create_command_chat_history(
        "test", CommandChatTypes.GLOBAL, {}, player_1
    )
    chat_2 = chat_manager.get_or_create_command_chat_history(
        "test", CommandChatTypes.GLOBAL, {}, player_2
    )
    assert chat_1 == chat_2
    assert id(chat_1) == id(chat_2)

    # test isolation
    chat_1_new = chat_manager.get_command_chat_history("test", CommandChatTypes.GLOBAL, player_1)
    chat_2_new = chat_manager.get_command_chat_history("test", CommandChatTypes.GLOBAL, player_2)
    assert chat_1 is chat_1_new
    assert chat_2 is chat_2_new
    assert chat_1 is chat_2_new

    chat_1_new.add_user_message_from_prompt(r"\l hello")
    assert chat_1.message_history == [{"content": "hello", "role": "user"}]
    assert chat_1.enable_soft_limit is False

    assert chat_2.message_history == [{"content": "hello", "role": "user"}]
    assert chat_2.enable_soft_limit is False
