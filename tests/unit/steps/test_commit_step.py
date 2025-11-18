import pytest

from repo_smith.steps.commit_step import CommitStep


def test_commit_step_parse_missing_message():
    with pytest.raises(ValueError, match='Missing "message" field in commit step.'):
        CommitStep.parse("n", "d", "id", {})


def test_commit_step_parse_empty_message():
    with pytest.raises(ValueError, match='Empty "message" field in commit step.'):
        CommitStep.parse("n", "d", "id", {"message": ""})


def test_commit_step_parse_missing_empty():
    step = CommitStep.parse("n", "d", "id", {"message": "Test"})
    assert isinstance(step, CommitStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.message == "Test"
    assert not step.empty


def test_commit_step_parse_with_empty():
    step = CommitStep.parse("n", "d", "id", {"message": "Test", "empty": True})
    assert isinstance(step, CommitStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.message == "Test"
    assert step.empty
