import os

import pytest
from git import Repo

from src.repo_smith.initialize_repo import initialize_repo


def test_initialize_repo_no_name() -> None:
    with pytest.raises(Exception):
        initialize_repo("tests/specs/no_name.yml")


def test_initialize_repo_step_no_name() -> None:
    with pytest.raises(Exception):
        initialize_repo("tests/specs/step_no_name.yml")


def test_initialize_repo_basic_spec() -> None:
    initialize_repo("tests/specs/basic_spec.yml")


def test_initialize_repo_hooks() -> None:
    initialize_repo("tests/specs/hooks.yml")


def test_initialize_repo_duplicate_ids() -> None:
    with pytest.raises(Exception):
        initialize_repo("tests/specs/duplicate_ids.yml")


def test_initialize_repo_duplicate_tags() -> None:
    with pytest.raises(Exception):
        initialize_repo("tests/specs/duplicate_tags.yml")


def test_initialize_repo_invalid_tag() -> None:
    with pytest.raises(Exception):
        initialize_repo("tests/specs/invalid_tag.yml")


def test_initialize_repo_invalid_pre_hook() -> None:
    with pytest.raises(Exception):
        repo_initializer = initialize_repo("tests/specs/basic_spec.yml")
        repo_initializer.add_pre_hook("hello-world", lambda _: None)


def test_initialize_repo_invalid_post_hook() -> None:
    with pytest.raises(Exception):
        repo_initializer = initialize_repo("tests/specs/basic_spec.yml")
        repo_initializer.add_post_hook("hello-world", lambda _: None)


def test_initialize_repo_pre_hook() -> None:
    def initial_commit_pre_hook(_: Repo) -> None:
        assert True

    repo_initializer = initialize_repo("tests/specs/basic_spec.yml")
    repo_initializer.add_pre_hook("initial-commit", initial_commit_pre_hook)
    with repo_initializer.initialize() as r:
        assert r.commit("start-tag") is not None


def test_initialize_repo_post_hook() -> None:
    def initial_commit_post_hook(_: Repo) -> None:
        assert True

    repo_initializer = initialize_repo("tests/specs/basic_spec.yml")
    repo_initializer.add_post_hook("initial-commit", initial_commit_post_hook)
    with repo_initializer.initialize():
        pass


# TODO move these to separate files for broader unit testing?
def test_initialize_repo_new_file() -> None:
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

    repo_initializer = initialize_repo("tests/specs/new_file.yml")
    repo_initializer.add_post_hook("filea", validate_filea_hook)
    repo_initializer.add_post_hook("nested_file", validate_nested_file_hook)
    with repo_initializer.initialize():
        pass


def test_initialize_repo_edit_file() -> None:
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

    repo_initializer = initialize_repo("tests/specs/new_file.yml")
    repo_initializer.add_post_hook("filea", validate_filea_hook)
    repo_initializer.add_post_hook("nested_file", validate_nested_file_hook)
    with repo_initializer.initialize():
        pass
