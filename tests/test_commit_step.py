from git import Repo
import pytest

from src.repo_smith.initialize_repo import initialize_repo


def test_commit_step_missing_message():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/commit_step/commit_step_missing_message.yml")


def test_commit_step():
    def pre_hook(r: Repo) -> None:
        with pytest.raises(Exception):
            # Ensure there is 0 commits
            # Must cast to list since the Iterator alone will not raise an error
            list(r.iter_commits("main"))

    repo_initializer = initialize_repo("tests/specs/commit_step/commit.yml")
    repo_initializer.add_pre_hook("commit", pre_hook)
    with repo_initializer.initialize() as r:
        commits = list(r.iter_commits("main"))
        assert len(commits) == 1
        commit = commits[0]
        assert len(commit.stats.files) == 1
        assert "file.txt" in commit.stats.files


def test_commit_step_empty_commit():
    def pre_hook(r: Repo) -> None:
        with pytest.raises(Exception):
            # Ensure there is 0 commits
            # Must cast to list since the Iterator alone will not raise an error
            list(r.iter_commits("main"))

    repo_initializer = initialize_repo("tests/specs/commit_step/commit_empty.yml")
    repo_initializer.add_pre_hook("commit", pre_hook)
    with repo_initializer.initialize() as r:
        commits = list(r.iter_commits("main"))
        assert len(commits) == 1
        commit = commits[0]
        assert len(commit.stats.files) == 0
