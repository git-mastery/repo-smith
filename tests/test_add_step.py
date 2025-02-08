import os

from git import Repo
import pytest

from src.repo_smith.initialize_repo import initialize_repo


def test_add_step_missing_files():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/add_step/add_step_missing_files.yml")


def test_add_step_empty_files():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/add_step/add_step_empty_files.yml")


def test_add_step():
    def pre_hook(r: Repo) -> None:
        filename = os.path.join(r.working_dir, "file.txt")
        assert os.path.isfile(filename)

    repo_initializer = initialize_repo("tests/specs/add_step/add_step.yml")
    repo_initializer.add_pre_hook("add", pre_hook)
    with repo_initializer.initialize() as r:
        assert len(r.index.entries) == 1
        assert ("file.txt", 0) in r.index.entries
