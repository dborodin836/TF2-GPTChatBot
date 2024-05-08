import pytest

import modules.commands.base
import modules.commands.clear_chat
import modules.commands.decorators
import modules.permissions
import modules.servers.tf2
import modules.utils.text
from modules.command_controllers import CommandController, InitializerConfig
from modules.commands import decorators as traits
from modules.commands.base import LLMChatCommand
from modules.conversation_history import ConversationHistory
from modules.lobby_manager import LobbyManager
from modules.typing import LogLine
from tests.common import DummyProvider, MockConfig, get_player


def dummy_func(*args):
    return args


@pytest.fixture
def setup_mocks(mocker):
    # Init
    conf = MockConfig()
    cfg = InitializerConfig()
    lobby_manager = LobbyManager()
    controller = CommandController(cfg)
    chat = ConversationHistory()

    # Mocking
    mocker.patch.object(modules.lobby_manager, "config", conf)
    mocker.patch.object(modules.commands.clear_chat, "lobby_manager", lobby_manager)
    mocker.patch.object(modules.permissions, "config", conf)
    mocker.patch.object(modules.commands.base, "send_say_command_to_tf2", dummy_func)
    mocker.patch.object(modules.servers.tf2, "config", conf)
    mocker.patch.object(modules.utils.text, "config", conf)
    spy = mocker.spy(modules.commands.base, "send_say_command_to_tf2")

    return lobby_manager, controller, chat, spy


def test_deny_empty(setup_mocks):
    lobby_manager, controller, chat, spy = setup_mocks

    # Setup environment
    class TestCmd(LLMChatCommand):
        provider = DummyProvider
        wrappers = [traits.deny_empty_prompt]

        @classmethod
        def get_chat(cls, logline: LogLine, shared_dict: InitializerConfig) -> ConversationHistory:
            return chat

    controller.register_command("!test", TestCmd.as_command(), "test")
    admin_player = get_player("admin", 0)
    player_1 = get_player("user1", 1)
    lobby_manager.add_player(admin_player)
    lobby_manager.add_player(player_1)

    # Test
    logline = LogLine(
        username="user1", player=player_1, is_team_message=False, prompt="!test TEST PROMPT"
    )
    controller.process_line(logline)
    assert spy.call_count == 1

    logline_1 = LogLine(username="user1", player=player_1, is_team_message=False, prompt="!test")
    controller.process_line(logline_1)
    assert spy.call_count == 1


def test_admin_only(setup_mocks):
    lobby_manager, controller, chat, spy = setup_mocks

    # Setup environment
    class TestCmd(LLMChatCommand):
        provider = DummyProvider
        wrappers = [traits.admin_only]

        @classmethod
        def get_chat(cls, logline: LogLine, shared_dict: InitializerConfig) -> ConversationHistory:
            return chat

    controller.register_command("!test", TestCmd.as_command(), "test")
    admin_player = get_player("admin", 0)
    player_1 = get_player("user1", 1)
    lobby_manager.add_player(admin_player)
    lobby_manager.add_player(player_1)

    # Test
    logline = LogLine(
        username="admin", player=admin_player, is_team_message=False, prompt="!test TEST PROMPT"
    )
    controller.process_line(logline)
    assert spy.call_count == 1

    logline_1 = LogLine(username="user1", player=player_1, is_team_message=False, prompt="!test")
    controller.process_line(logline_1)
    assert spy.call_count == 1


def test_disabled(setup_mocks):
    lobby_manager, controller, chat, spy = setup_mocks

    # Setup environment
    class TestCmd(LLMChatCommand):
        provider = DummyProvider
        wrappers = [traits.disabled]

        @classmethod
        def get_chat(cls, logline: LogLine, shared_dict: InitializerConfig) -> ConversationHistory:
            return chat

    controller.register_command("!test", TestCmd.as_command(), "test")
    admin_player = get_player("admin", 0)
    player_1 = get_player("user1", 1)
    lobby_manager.add_player(admin_player)
    lobby_manager.add_player(player_1)

    # Test
    logline = LogLine(
        username="admin", player=admin_player, is_team_message=False, prompt="!test TEST PROMPT"
    )
    controller.process_line(logline)
    assert spy.call_count == 0

    logline_1 = LogLine(username="user1", player=player_1, is_team_message=False, prompt="!test")
    controller.process_line(logline_1)
    assert spy.call_count == 0


def test_moderation(setup_mocks, mocker):
    lobby_manager, controller, chat, spy = setup_mocks
    mocker.patch.object(modules.commands.decorators, "is_flagged", lambda *args: True)

    # Setup environment
    class TestCmd(LLMChatCommand):
        provider = DummyProvider
        wrappers = [traits.openai_moderated]

        @classmethod
        def get_chat(cls, logline: LogLine, shared_dict: InitializerConfig) -> ConversationHistory:
            return chat

    controller.register_command("!test", TestCmd.as_command(), "test")
    admin_player = get_player("admin", 0)
    player_1 = get_player("user1", 1)
    lobby_manager.add_player(admin_player)
    lobby_manager.add_player(player_1)

    # Test
    logline = LogLine(
        username="admin", player=admin_player, is_team_message=False, prompt="!test TEST PROMPT"
    )
    controller.process_line(logline)
    assert spy.call_count == 1

    logline_1 = LogLine(
        username="user1", player=player_1, is_team_message=False, prompt="!test TEST PROMPT"
    )
    controller.process_line(logline_1)
    assert spy.call_count == 1


def test_empty_prompt_response(setup_mocks):
    lobby_manager, controller, chat, spy = setup_mocks

    # Setup environment
    class TestCmd(LLMChatCommand):
        provider = DummyProvider
        wrappers = [traits.empty_prompt_message_response("EMPTY RESPONSE")]

        @classmethod
        def get_chat(cls, logline: LogLine, shared_dict: InitializerConfig) -> ConversationHistory:
            return chat

    controller.register_command("!test", TestCmd.as_command(), "test")
    admin_player = get_player("admin", 0)
    player_1 = get_player("user1", 1)
    lobby_manager.add_player(admin_player)
    lobby_manager.add_player(player_1)

    # Test
    logline = LogLine(
        username="admin", player=admin_player, is_team_message=False, prompt="!test TEST PROMPT"
    )
    controller.process_line(logline)
    assert spy.call_count == 1
    assert spy.spy_return == ("completion text", "admin", False)

    logline_1 = LogLine(username="user1", player=player_1, is_team_message=False, prompt="!test")
    controller.process_line(logline_1)
    assert spy.call_count == 1
