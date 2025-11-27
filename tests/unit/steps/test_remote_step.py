import pytest

from repo_smith.steps.remote_step import RemoteStep


def test_remote_step_parse_missing_remote_url():
    with pytest.raises(ValueError, match='Missing "remote-url" field in remote step.'):
        RemoteStep.parse("n", "d", "id", {})


def test_remote_step_parse_empty_remote_url():
    with pytest.raises(ValueError, match='Empty "remote-url" field in remote step.'):
        RemoteStep.parse("n", "d", "id", {"remote-url": ""})


def test_remote_step_parse_missing_remote_name():
    with pytest.raises(ValueError, match='Missing "remote-name" field in remote step.'):
        RemoteStep.parse("n", "d", "id", {"remote-url": "https://test.com"})


def test_remote_step_parse_empty_remote_name():
    with pytest.raises(ValueError, match='Empty "remote-name" field in remote step.'):
        RemoteStep.parse(
            "n", "d", "id", {"remote-url": "https://test.com", "remote-name": ""}
        )


def test_remote_step_parse():
    step = RemoteStep.parse(
        "n", "d", "id", {"remote-url": "https://test.com", "remote-name": "upstream"}
    )
    assert isinstance(step, RemoteStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.remote_url == "https://test.com"
    assert step.remote_name == "upstream"
