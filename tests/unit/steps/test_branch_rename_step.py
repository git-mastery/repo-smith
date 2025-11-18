import pytest

from repo_smith.steps.branch_delete_step import BranchDeleteStep
from repo_smith.steps.branch_rename_step import BranchRenameStep


def test_branch_rename_step_parse_missing_branch_name():
    with pytest.raises(
        ValueError, match='Missing "branch-name" field in branch-rename step.'
    ):
        BranchRenameStep.parse("n", "d", "id", {})


def test_branch_rename_step_parse_empty_branch_name():
    with pytest.raises(
        ValueError, match='Empty "branch-name" field in branch-rename step.'
    ):
        BranchRenameStep.parse("n", "d", "id", {"branch-name": ""})


def test_branch_rename_step_parse_missing_new_name():
    with pytest.raises(
        ValueError, match='Missing "new-name" field in branch-rename step.'
    ):
        BranchRenameStep.parse("n", "d", "id", {"branch-name": "test"})


def test_branch_rename_step_parse_empty_new_name():
    with pytest.raises(
        ValueError, match='Empty "new-name" field in branch-rename step.'
    ):
        BranchRenameStep.parse("n", "d", "id", {"branch-name": "test", "new-name": ""})


def test_branch_rename_step_parse():
    step = BranchRenameStep.parse(
        "n", "d", "id", {"branch-name": "test", "new-name": "other"}
    )
    assert isinstance(step, BranchRenameStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.original_branch_name == "test"
    assert step.target_branch_name == "other"
