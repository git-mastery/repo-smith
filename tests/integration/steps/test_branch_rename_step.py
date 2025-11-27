import pytest
from repo_smith.initialize_repo import initialize_repo


def test_branch_rename_step_branch_exists():
    repo_initializer = initialize_repo(
        "tests/specs/branch_rename_step/branch_rename_step_branch_exists.yml"
    )
    with repo_initializer.initialize() as r:
        assert {r.name for r in r.refs} == {"main", "primary"}


def test_branch_rename_step_branch_does_not_exist():
    repo_initializer = initialize_repo(
        "tests/specs/branch_rename_step/branch_rename_step_branch_does_not_exist.yml"
    )
    with pytest.raises(
        ValueError,
        match='"branch-name" field provided does not correspond to any existing branches in branch-rename step.',
    ):
        with repo_initializer.initialize() as _:
            pass


def test_branch_rename_step_branch_already_existed():
    repo_initializer = initialize_repo(
        "tests/specs/branch_rename_step/branch_rename_step_branch_already_existed.yml"
    )
    with pytest.raises(
        ValueError,
        match='"new-name" field provided corresponds to an existing branch already in branch-rename step.',
    ):
        with repo_initializer.initialize() as _:
            pass
