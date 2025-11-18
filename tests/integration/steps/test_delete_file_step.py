import os

import pytest
from git import Repo

from src.repo_smith.initialize_repo import initialize_repo


def test_delete_file_step_missing_filename() -> None:
    with pytest.raises(Exception):
        initialize_repo("tests/specs/delete_file_step/delete_file_missing_filename.yml")


def test_delete_file_step_unknown_file() -> None:
    with pytest.raises(Exception):
        repo_initializer = initialize_repo(
            "tests/specs/delete_file_step/delete_file_no_file.yml"
        )
        with repo_initializer.initialize():
            pass


def test_delete_file_step() -> None:
    def pre_hook(r: Repo) -> None:
        filepath = os.path.join(r.working_dir, "file.txt")
        assert os.path.isfile(filepath)

    repo_initializer = initialize_repo("tests/specs/delete_file_step/delete_file.yml")
    repo_initializer.add_pre_hook("delete-file", pre_hook)
    with repo_initializer.initialize() as r:
        filepath = os.path.join(r.working_dir, "file.txt")
        assert not os.path.isfile(filepath)
