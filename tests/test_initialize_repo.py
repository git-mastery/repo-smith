import pytest
from git import Repo

from src.repo_smith.initialize_repo import initialize_repo


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
