import os

import pytest
from git import Repo

from src.repo_smith.initialize_repo import initialize_repo


def test_append_file_step_missing_filename():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/append_file_step/append_file_missing_filename.yml")


def test_append_file_step_no_filename():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/append_file_step/append_file_no_filename.yml")


def test_append_file_step():
    def pre_hook(r: Repo) -> None:
        filepath = os.path.join(r.working_dir, "file.txt")
        assert os.path.isfile(filepath)
        expected = ["Hello world"]
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f.readlines()]
            assert len(lines) == len(expected)
            for actual, ex in zip(lines, expected):
                assert actual == ex

    def post_hook(r: Repo) -> None:
        filepath = os.path.join(r.working_dir, "file.txt")
        assert os.path.isfile(filepath)
        expected = ["Hello world", "This is a new line!"]
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f.readlines()]
            assert len(lines) == len(expected)
            for actual, ex in zip(lines, expected):
                assert actual == ex

    repo_initializer = initialize_repo("tests/specs/append_file_step/append_file.yml")
    repo_initializer.add_pre_hook("append-file", pre_hook)
    repo_initializer.add_post_hook("append-file", post_hook)
    with repo_initializer.initialize():
        pass
