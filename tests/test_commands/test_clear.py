import modules.commands.clear_chat
import modules.permissions
import modules.lobby_manager
from modules.command_controllers import InitializerConfig
from modules.commands.clear_chat import handle_clear
from modules.lobby_manager import LobbyManager
from modules.typing import LogLine, Message, Player
from tests.common import MockConfig, get_player


def test_clear(mocker):
    conf = MockConfig()
    lobby_manager = LobbyManager()
    mocker.patch.object(modules.lobby_manager, "config", conf)

    pl1 = get_player("user1", 1)
    lobby_manager.add_player(pl1)

    mocker.patch.object(modules.commands.clear_chat, "config", conf)
    mocker.patch.object(modules.commands.clear_chat, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.permissions, "config", conf)

    logline = LogLine(username="user1", prompt="!clear", is_team_message=False, player=pl1)
    cfg = InitializerConfig()

    cvh1 = cfg.CHAT_CONVERSATION_HISTORY.get_conversation_history(pl1)
    cvh1.message_history.append(Message(content="hello", role="user"))
    assert cvh1.message_history == [Message(content="hello", role="user")]

    handle_clear(logline, cfg)

    assert cvh1.message_history == []


def test_clear_admin(mocker):
    conf = MockConfig()
    lobby_manager = LobbyManager()
    mocker.patch.object(modules.commands.clear_chat, "config", conf)
    mocker.patch.object(modules.commands.clear_chat, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.permissions, "config", conf)
    mocker.patch.object(modules.lobby_manager, "config", conf)

    pl_admin = get_player("admin", 0)
    pl1 = get_player("user1", 1)
    pl2 = get_player("user2", 2)

    lobby_manager.add_player(pl_admin)
    lobby_manager.add_player(pl1)
    lobby_manager.add_player(pl2)

    logline_admin = LogLine(username="admin", prompt=r"!clear \user='user1'", is_team_message=False, player=pl_admin)
    cfg = InitializerConfig()

    # Init global chat
    cfg.CHAT_CONVERSATION_HISTORY.GLOBAL.message_history.append(Message(content="global message", role="user"))
    assert cfg.CHAT_CONVERSATION_HISTORY.GLOBAL.message_history != []

    # Create chats for users
    cvh1 = cfg.CHAT_CONVERSATION_HISTORY.get_conversation_history(pl1)
    cvh1.message_history.append(Message(content="hello from user1", role="user"))
    cvh2 = cfg.CHAT_CONVERSATION_HISTORY.get_conversation_history(pl2)
    cvh2.message_history.append(Message(content="hello from user2", role="user"))
    assert cvh1.message_history != []
    assert cvh2.message_history != []

    # create chat for admin
    cvh_admin = cfg.CHAT_CONVERSATION_HISTORY.get_conversation_history(pl_admin)
    cvh_admin.message_history.append(Message(content="hello from admin", role="user"))
    assert cvh_admin.message_history != []

    # test for admin
    logline_admin_self = LogLine(username="admin", prompt=r"!clear", is_team_message=False, player=pl_admin)
    handle_clear(logline_admin_self, cfg)

    assert cvh_admin.message_history == []
    assert cvh1.message_history != []
    assert cvh2.message_history != []
    assert cfg.CHAT_CONVERSATION_HISTORY.GLOBAL.message_history != []

    # test users
    handle_clear(logline_admin, cfg)

    assert cvh1.message_history == []
    assert cvh2.message_history != []
    assert cfg.CHAT_CONVERSATION_HISTORY.GLOBAL.message_history != []

    # test global
    logline_admin_global = LogLine(username="admin", prompt=r"!clear \global", is_team_message=False, player=pl_admin)
    handle_clear(logline_admin_global, cfg)

    assert cvh1.message_history == []
    assert cvh2.message_history != []
    assert cfg.CHAT_CONVERSATION_HISTORY.GLOBAL.message_history == []


def test_clear_admin_bypass(mocker):
    conf = MockConfig()
    lobby_manager = LobbyManager()
    mocker.patch.object(modules.commands.clear_chat, "config", conf)
    mocker.patch.object(modules.commands.clear_chat, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.permissions, "config", conf)
    mocker.patch.object(modules.lobby_manager, "config", conf)
    cfg = InitializerConfig()

    pl1 = get_player("user1", 1)
    pl2 = get_player("user2", 2)
    pl3 = get_player("user3", 3)
    lobby_manager.add_player(pl1)
    lobby_manager.add_player(pl2)
    lobby_manager.add_player(pl3)

    # Init global chat
    cfg.CHAT_CONVERSATION_HISTORY.GLOBAL.message_history.append(Message(content="global message", role="user"))
    assert cfg.CHAT_CONVERSATION_HISTORY.GLOBAL.message_history != []

    # Create chats for users
    cvh1 = cfg.CHAT_CONVERSATION_HISTORY.get_conversation_history(pl1)
    cvh1.message_history.append(Message(content="hello from user1", role="user"))
    cvh2 = cfg.CHAT_CONVERSATION_HISTORY.get_conversation_history(pl2)
    cvh2.message_history.append(Message(content="hello from user2", role="user"))
    assert cvh1.message_history != []
    assert cvh2.message_history != []

    logline_user1 = LogLine(username="user3", prompt=r"!clear \user='user1'", is_team_message=False, player=pl3)
    logline_user2 = LogLine(username="user3", prompt=r"!clear \user='user2'", is_team_message=False, player=pl3)
    logline_global = LogLine(username="user3", prompt=r"!clear \global", is_team_message=False, player=pl3)

    handle_clear(logline_user1, cfg)
    handle_clear(logline_user2, cfg)
    handle_clear(logline_global, cfg)

    assert cvh1.message_history != []
    assert cvh2.message_history != []
    assert cfg.CHAT_CONVERSATION_HISTORY.GLOBAL.message_history != []
