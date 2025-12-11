import pytest

from repo_smith.steps.revert_step import RevertStep


def test_add_step_parse_missing_files():
    with pytest.raises(ValueError, match='Missing "commit" field in revert step.'):
        RevertStep.parse("n", "d", "id", {})


def test_add_step_parse_empty_files():
    with pytest.raises(ValueError, match='Empty "commit" field in revert step.'):
        RevertStep.parse("n", "d", "id", {"commit": ""})


def test_revert_step_parse():
    step = RevertStep.parse("n", "d", "id", {"commit": "HEAD~4"})
    assert isinstance(step, RevertStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.commit == "HEAD~4"
