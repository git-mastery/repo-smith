import pytest

from repo_smith.steps.branch_step import BranchStep


def test_branch_step_parse_missing_branch_name():
    with pytest.raises(ValueError, match='Missing "branch-name" field in branch step.'):
        BranchStep.parse("n", "d", "id", {})


def test_branch_step_parse_empty_branch_name():
    with pytest.raises(ValueError, match='Empty "branch-name" field in branch step.'):
        BranchStep.parse("n", "d", "id", {"branch-name": ""})


def test_branch_step_parse():
    step = BranchStep.parse("n", "d", "id", {"branch-name": "test"})
    assert isinstance(step, BranchStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.branch_name == "test"
