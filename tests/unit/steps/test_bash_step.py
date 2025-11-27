import pytest

from repo_smith.steps.bash_step import BashStep


def test_bash_step_parse_missing_runs():
    with pytest.raises(ValueError, match='Missing "runs" field in bash step.'):
        BashStep.parse("a", "d", "id", {})


def test_bash_step_parse_empty_runs():
    with pytest.raises(ValueError, match='Empty "runs" field in bash step.'):
        BashStep.parse("a", "d", "id", {"runs": ""})


def test_bash_step_parse():
    step = BashStep.parse("a", "d", "id", {"runs": "ls"})
    assert isinstance(step, BashStep)
    assert step.name == "a"
    assert step.description == "d"
    assert step.id == "id"
    assert step.body == "ls"
