import os

import pytest
from git import Repo

from src.repo_smith.initialize_repo import initialize_repo


def test_edit_file_step_unknown_file() -> None:
    with pytest.raises(Exception):
        repo_initializer = initialize_repo(
            "tests/specs/edit_file_step/edit_file_missing.yml"
        )
        with repo_initializer.initialize():
            pass


def test_edit_file_step() -> None:
    def add_hook(r: Repo) -> None:
        dir_list = os.listdir(r.working_dir)
        assert "filea.txt" in dir_list
        filepath = os.path.join(r.working_dir, "filea.txt")
        expected_file_contents = ["Original text"]
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f.readlines()]
            assert len(lines) == len(expected_file_contents)
            for actual, expected in zip(lines, expected_file_contents):
                assert actual == expected

    def edit_hook(r: Repo) -> None:
        dir_list = os.listdir(r.working_dir)
        assert "filea.txt" in dir_list
        filepath = os.path.join(r.working_dir, "filea.txt")
        expected_file_contents = ["Edited text"]
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f.readlines()]
            assert len(lines) == len(expected_file_contents)
            for actual, expected in zip(lines, expected_file_contents):
                assert actual == expected

    repo_initializer = initialize_repo("tests/specs/edit_file_step/edit_file.yml")
    repo_initializer.add_post_hook("add", add_hook)
    repo_initializer.add_post_hook("edit", edit_hook)
    with repo_initializer.initialize():
        pass
