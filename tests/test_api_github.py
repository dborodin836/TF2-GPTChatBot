import logging

import modules.api.github
from modules.api.github import check_for_updates
from tests.common import MockConfig, raise_


def test_check_for_updates_with_newer_version_available(mocker, caplog, requests_mock):
    remote_ver = "1.2.1"
    local_ver = "1.0.0"

    requests_mock.register_uri(
        "GET",
        "https://api.github.com/repos/dborodin836/TF2-GPTChatBot/releases/latest",
        text='{"tag_name": "%s"}' % remote_ver,
    )
    mocker.patch.object(modules.api.github, "config", MockConfig(app_version="1.0.0"))

    with caplog.at_level(logging.DEBUG):
        check_for_updates()

    assert f"A new version ({remote_ver}) of the app is available. Please update." in caplog.text
    assert f"Latest version on GitHub - {remote_ver}" in caplog.text
    assert f"Checking for updates... App version - {local_ver}" in caplog.text


def test_check_for_updates_with_no_new_version(mocker, caplog, requests_mock):
    remote_ver = "1.0.0"
    local_ver = "1.0.0"

    requests_mock.register_uri(
        "GET",
        "https://api.github.com/repos/dborodin836/TF2-GPTChatBot/releases/latest",
        text='{"tag_name": "%s"}' % remote_ver,
    )
    mocker.patch.object(modules.api.github, "config", MockConfig(app_version="1.0.0"))

    with caplog.at_level(logging.DEBUG):
        check_for_updates()

    assert f"Latest version on GitHub - {local_ver}" in caplog.text
    assert f"The app is up to date. ({local_ver})" in caplog.text


def test_check_for_updates_with_request_failure(mocker, caplog):
    mocker.patch(
        "modules.api.github.requests.get", return_value=(lambda: raise_(Exception("Network Error")))
    )

    mocker.patch.object(modules.api.github, "config", MockConfig(app_version="1.0.0"))

    with caplog.at_level(logging.DEBUG):
        check_for_updates()

    assert "Failed to check for updates." in caplog.text
