import os

from git import Repo
import pytest

from src.repo_smith.initialize_repo import initialize_repo


def test_branch_step_missing_branch_name():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/branch_step/branch_step_missing_branch_name.yml")


def test_branch_step_empty_branch_name():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/branch_step/branch_step_empty_branch_name.yml")


def test_branch_step():
    repo_initializer = initialize_repo("tests/specs/branch_step/branch_step.yml")
    with repo_initializer.initialize() as r:
        assert len(r.branches) == 2
        assert "test" in r.heads
