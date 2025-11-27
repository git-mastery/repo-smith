from git import Repo
import pytest

from src.repo_smith.initialize_repo import initialize_repo


def test_checkout_step_missing_branch_name():
    with pytest.raises(Exception):
        initialize_repo(
            "tests/specs/checkout_step/checkout_step_missing_branch_name.yml"
        )


def test_checkout_step_empty_branch_name():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/checkout_step/checkout_step_empty_branch_name.yml")


def test_checkout_step_missing_branch():
    with pytest.raises(Exception):
        repo_initialier = initialize_repo(
            "tests/specs/checkout_step/checkout_step_missing_branch.yml"
        )
        with repo_initialier.initialize():
            pass


def test_checkout_step():
    def first_hook(r: Repo) -> None:
        assert r.active_branch.name == "main"

    def second_hook(r: Repo) -> None:
        assert r.active_branch.name == "test"

    repo_initializer = initialize_repo("tests/specs/checkout_step/checkout_step.yml")
    repo_initializer.add_post_hook("first", first_hook)
    repo_initializer.add_post_hook("second", second_hook)
    with repo_initializer.initialize() as r:
        assert len(r.branches) == 2
        assert "test" in r.heads
