import pytest

from repo_smith.steps.fetch_step import FetchStep


def test_fetch_step_parse_missing_remote_name():
    with pytest.raises(ValueError, match='Missing "remote-name" field in fetch step.'):
        FetchStep.parse("n", "d", "id", {})


def test_fetch_step_parse_empty_remote_name():
    with pytest.raises(ValueError, match='Empty "remote-name" field in fetch step.'):
        FetchStep.parse("n", "d", "id", {"remote-name": ""})


def test_commit_step_parse_with_empty():
    step = FetchStep.parse("n", "d", "id", {"remote-name": "test"})
    assert isinstance(step, FetchStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.remote_name == "test"
