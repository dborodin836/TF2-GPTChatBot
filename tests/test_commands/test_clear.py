import modules.commands.clear_chat
import modules.permissions
import modules.lobby_manager
from modules.command_controllers import CommandChatTypes, CommandController, InitializerConfig
from modules.commands.clear_chat import handle_clear
from modules.lobby_manager import LobbyManager
from modules.typing import LogLine, Message
from tests.common import MockConfig, get_player
from tests.common import DummyLLMChatCommand


def test_clear(mocker):
    # Init
    conf = MockConfig()
    cfg = InitializerConfig()
    lobby_manager = LobbyManager()
    controller = CommandController(cfg)

    # Mocking
    mocker.patch.object(modules.lobby_manager, "config", conf)
    mocker.patch.object(modules.commands.clear_chat, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.permissions, "config", conf)

    # Setup environment
    controller.register_command('!test', DummyLLMChatCommand.as_command(), 'test')
    player_1 = get_player("user1", 1)
    lobby_manager.add_player(player_1)

    # Create chat
    chat_1 = cfg.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(
        'test',
        CommandChatTypes.PRIVATE,
        {},
        player_1
    )
    chat_1.message_history.append(Message(content="hello", role="user"))
    assert chat_1.message_history == [Message(content="hello", role="user")]

    # Clear chat
    logline = LogLine(username="user1", prompt="!clear test", is_team_message=False, player=player_1)
    handle_clear(logline, cfg)
    assert chat_1.message_history == []


def test_clear_admin(mocker):
    # Init
    conf = MockConfig()
    cfg = InitializerConfig()
    lobby_manager = LobbyManager()
    controller = CommandController(cfg)

    # Mocking
    mocker.patch.object(modules.lobby_manager, "config", conf)
    mocker.patch.object(modules.commands.clear_chat, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.permissions, "config", conf)

    # Setup environment
    controller.register_command('!test', DummyLLMChatCommand.as_command(), 'test')
    controller.register_command('!test_p', DummyLLMChatCommand.as_command(), 'test_p')
    admin_player = get_player("admin", 0)
    player_1 = get_player("user1", 1)
    player_2 = get_player("user2", 2)
    lobby_manager.add_player(admin_player)
    lobby_manager.add_player(player_1)
    lobby_manager.add_player(player_2)

    # Create chats
    global_chat_1 = cfg.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(
        'test',
        CommandChatTypes.GLOBAL,
        {},
        player_1
    )
    global_chat_1.message_history.append(Message(content="hello", role="user"))
    assert global_chat_1.message_history == [Message(content="hello", role="user")]

    # Clear chat as admin
    logline_admin = LogLine(username="admin", prompt=r"\global test", is_team_message=False, player=admin_player)
    logline_admin_fail = LogLine(username="admin", prompt=r"test", is_team_message=False, player=admin_player)
    handle_clear(logline_admin_fail, cfg)
    assert global_chat_1.message_history != []
    handle_clear(logline_admin, cfg)
    assert global_chat_1.message_history == []

    # Create user chats
    chat_usr_1 = cfg.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(
        'test_p',
        CommandChatTypes.PRIVATE,
        {},
        player_1
    )
    chat_usr_1.message_history.append(Message(content="hello from user 1", role="user"))
    assert chat_usr_1.message_history == [Message(content="hello from user 1", role="user")]
    chat_usr_2 = cfg.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(
        'test_p',
        CommandChatTypes.PRIVATE,
        {},
        player_2
    )
    chat_usr_2.message_history.append(Message(content="hello from user 2", role="user"))
    assert chat_usr_2.message_history == [Message(content="hello from user 2", role="user")]

    # Test clear
    logline_admin = LogLine(username="admin", prompt=r"\user='user1' test_p", is_team_message=False,
                            player=admin_player)
    logline_admin_fail_0 = LogLine(username="admin", prompt=r"test_p", is_team_message=False, player=admin_player)
    logline_admin_fail_1 = LogLine(username="admin", prompt=r"\global test_p", is_team_message=False,
                                   player=admin_player)
    logline_admin_fail_2 = LogLine(username="admin", prompt=r"\global \user='unknown' test_p", is_team_message=False,
                                   player=admin_player)
    logline_admin_fail_3 = LogLine(username="admin", prompt=r"\user='unknown' test_p", is_team_message=False,
                                   player=admin_player)
    handle_clear(logline_admin_fail_0, cfg)
    assert chat_usr_1.message_history != []
    assert chat_usr_2.message_history != []
    handle_clear(logline_admin_fail_1, cfg)
    assert chat_usr_1.message_history != []
    assert chat_usr_2.message_history != []
    handle_clear(logline_admin_fail_2, cfg)
    assert chat_usr_1.message_history != []
    assert chat_usr_2.message_history != []
    handle_clear(logline_admin_fail_3, cfg)
    assert chat_usr_1.message_history != []
    assert chat_usr_2.message_history != []
    handle_clear(logline_admin, cfg)
    assert chat_usr_1.message_history == []
    assert chat_usr_2.message_history != []


def test_clear_admin_bypass(mocker):
    # Init
    conf = MockConfig()
    cfg = InitializerConfig()
    lobby_manager = LobbyManager()
    controller = CommandController(cfg)

    # Mocking
    mocker.patch.object(modules.lobby_manager, "config", conf)
    mocker.patch.object(modules.commands.clear_chat, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.permissions, "config", conf)

    # Setup environment
    controller.register_command('!test', DummyLLMChatCommand.as_command(), 'test')
    controller.register_command('!test_p', DummyLLMChatCommand.as_command(), 'test_p')
    admin_player = get_player("admin", 0)
    player_1 = get_player("user1", 1)
    player_2 = get_player("user2", 2)
    lobby_manager.add_player(admin_player)
    lobby_manager.add_player(player_1)
    lobby_manager.add_player(player_2)

    # Create chats
    global_chat_1 = cfg.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(
        'test',
        CommandChatTypes.GLOBAL,
        {},
        player_1
    )
    global_chat_1.message_history.append(Message(content="hello", role="user"))
    assert global_chat_1.message_history == [Message(content="hello", role="user")]

    # Create user chats
    chat_usr_1 = cfg.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(
        'test_p',
        CommandChatTypes.PRIVATE,
        {},
        player_1
    )
    chat_usr_1.message_history.append(Message(content="hello from user 1", role="user"))
    assert chat_usr_1.message_history == [Message(content="hello from user 1", role="user")]
    chat_usr_2 = cfg.CHAT_CONVERSATION_HISTORY.get_or_create_command_chat_history(
        'test_p',
        CommandChatTypes.PRIVATE,
        {},
        player_2
    )
    chat_usr_2.message_history.append(Message(content="hello from user 2", role="user"))
    assert chat_usr_2.message_history == [Message(content="hello from user 2", role="user")]

    # Test clear
    logline_usr_2 = LogLine(username="user2", prompt=r"test_p", is_team_message=False, player=player_2)
    logline_usr_1_fail_0 = LogLine(username="user1", prompt=r"\user='user2' test_p", is_team_message=False,
                                   player=player_1)
    logline_usr_1_fail_1 = LogLine(username="user1", prompt=r"\global test", is_team_message=False,
                                   player=player_1)
    logline_usr_1_fail_2 = LogLine(username="user1", prompt=r"\global \user='user2' test_p test", is_team_message=False,
                                   player=player_1)
    handle_clear(logline_usr_1_fail_0, cfg)
    assert chat_usr_1.message_history == []
    assert chat_usr_2.message_history != []
    assert global_chat_1.message_history != []
    handle_clear(logline_usr_1_fail_1, cfg)
    assert chat_usr_1.message_history == []
    assert chat_usr_2.message_history != []
    assert global_chat_1.message_history != []
    handle_clear(logline_usr_1_fail_2, cfg)
    assert chat_usr_1.message_history == []
    assert chat_usr_2.message_history != []
    assert global_chat_1.message_history != []
    handle_clear(logline_usr_2, cfg)
    assert chat_usr_1.message_history == []
    assert chat_usr_2.message_history == []
    assert global_chat_1.message_history != []
