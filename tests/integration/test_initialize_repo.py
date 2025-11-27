import pytest
from git import Repo
from src.repo_smith.initialize_repo import initialize_repo

# TODO: Test to make sure that the YAML parsing is accurate so we avoid individual
# integration test for every corner case covered in unit tests


def test_initialize_repo_missing_spec_path():
    with pytest.raises(ValueError, match="Invalid spec_path provided, not found."):
        initialize_repo("tests/specs/invalid_spec_path_does_not_exist.yml")


def test_initialize_repo_incomplete_spec_file():
    with pytest.raises(ValueError, match="Incomplete spec file."):
        initialize_repo("tests/specs/incomplete_spec_file.yml")


def test_initialize_repo_duplicate_ids():
    with pytest.raises(
        ValueError,
        match="ID commit is duplicated from a previous step. All IDs should be unique.",
    ):
        initialize_repo("tests/specs/duplicate_ids.yml")


def test_initialize_repo_duplicate_tags():
    with pytest.raises(
        ValueError,
        match="Tag tag is already in use by a previous step. All tag names should be unique.",
    ):
        initialize_repo("tests/specs/duplicate_tags.yml")


def test_initialize_repo_invalid_pre_hook():
    with pytest.raises(Exception):
        repo_initializer = initialize_repo("tests/specs/basic_spec.yml")
        repo_initializer.add_pre_hook("hello-world", lambda _: None)


def test_initialize_repo_invalid_post_hook():
    with pytest.raises(Exception):
        repo_initializer = initialize_repo("tests/specs/basic_spec.yml")
        repo_initializer.add_post_hook("hello-world", lambda _: None)


def test_initialize_repo_pre_hook():
    def initial_commit_pre_hook(_: Repo):
        assert True

    repo_initializer = initialize_repo("tests/specs/basic_spec.yml")
    repo_initializer.add_pre_hook("initial-commit", initial_commit_pre_hook)
    with repo_initializer.initialize() as r:
        assert r.commit("start-tag") is not None


def test_initialize_repo_post_hook():
    def initial_commit_post_hook(_: Repo):
        assert True

    repo_initializer = initialize_repo("tests/specs/basic_spec.yml")
    repo_initializer.add_post_hook("initial-commit", initial_commit_post_hook)
    with repo_initializer.initialize():
        pass


def test_initialize_repo_basic_spec():
    initialize_repo("tests/specs/basic_spec.yml")


def test_initialize_repo_hooks():
    initialize_repo("tests/specs/hooks.yml")
