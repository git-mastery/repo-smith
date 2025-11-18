import os

import pytest
from git import Repo

from src.repo_smith.initialize_repo import initialize_repo


def test_new_file_step_missing_filename() -> None:
    with pytest.raises(Exception):
        initialize_repo("tests/specs/new_file_step/new_file_missing_filename.yml")


def test_new_file_step_empty_filename() -> None:
    with pytest.raises(Exception):
        initialize_repo("tests/specs/new_file_step/new_file_empty_filename.yml")


def test_new_file_step_empty_contents() -> None:
    repo_initializer = initialize_repo(
        "tests/specs/new_file_step/new_file_empty_contents.yml"
    )
    with repo_initializer.initialize() as r:
        filea = os.path.join(r.working_dir, "filea.txt")
        fileb = os.path.join(r.working_dir, "fileb.txt")
        assert os.path.isfile(filea)
        assert os.path.isfile(fileb)
        assert os.path.getsize(filea) == 0
        assert os.path.getsize(fileb) == 0


def test_new_file_step() -> None:
    def validate_filea_hook(r: Repo) -> None:
        dir_list = os.listdir(r.working_dir)
        assert "filea.txt" in dir_list
        filepath = os.path.join(r.working_dir, "filea.txt")
        expected_file_contents = ["Hello world!", "", "This is a file"]
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f.readlines()]
            assert len(lines) == len(expected_file_contents)
            for actual, expected in zip(lines, expected_file_contents):
                assert actual == expected

    def validate_nested_file_hook(r: Repo) -> None:
        dir_list = os.listdir(r.working_dir)
        assert "nested" in dir_list
        filepath = os.path.join(r.working_dir, "nested/a/b/c/filed.txt")
        assert os.path.isfile(filepath)
        expected_file_contents = ["This is a nested file"]
        with open(filepath, "r") as f:
            lines = [line.strip() for line in f.readlines()]
            assert len(lines) == len(expected_file_contents)
            for actual, expected in zip(lines, expected_file_contents):
                assert actual == expected

    repo_initializer = initialize_repo("tests/specs/new_file_step/new_file.yml")
    repo_initializer.add_post_hook("filea", validate_filea_hook)
    repo_initializer.add_post_hook("nested_file", validate_nested_file_hook)
    with repo_initializer.initialize():
        pass
