import pytest

from repo_smith.steps.branch_delete_step import BranchDeleteStep


def test_branch_delete_step_parse_missing_branch_name():
    with pytest.raises(
        ValueError, match='Missing "branch-name" field in branch-delete step.'
    ):
        BranchDeleteStep.parse("n", "d", "id", {})


def test_branch_delete_step_parse_empty_branch_name():
    with pytest.raises(
        ValueError, match='Empty "branch-name" field in branch-delete step.'
    ):
        BranchDeleteStep.parse("n", "d", "id", {"branch-name": ""})


def test_branch_delete_step_parse():
    step = BranchDeleteStep.parse("n", "d", "id", {"branch-name": "test"})
    assert isinstance(step, BranchDeleteStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.branch_name == "test"

