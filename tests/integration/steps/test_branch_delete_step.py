import pytest
from repo_smith.initialize_repo import initialize_repo


def test_branch_delete_step_branch_exists():
    repo_initializer = initialize_repo(
        "tests/specs/branch_delete_step/branch_delete_step_branch_exists.yml"
    )
    with repo_initializer.initialize() as r:
        assert [r.name for r in r.refs] == ["main"]


def test_branch_delete_step_branch_does_not_exist():
    repo_initializer = initialize_repo(
        "tests/specs/branch_delete_step/branch_delete_step_branch_does_not_exist.yml"
    )

    with pytest.raises(
        ValueError,
        match='"branch-name" field provided does not correspond to any existing branches in branch-delete step.',
    ):
        with repo_initializer.initialize() as _:
            pass
