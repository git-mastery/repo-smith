import os

import pytest
from git import Repo
from repo_smith.initialize_repo import initialize_repo
from tests.fixtures.git_fixtures import REMOTE_REPO_PATH, remote_repo


def test_fetch_step_remote_valid(remote_repo: Repo):
    (REMOTE_REPO_PATH / "dummy.txt").write_text("initial")
    remote_repo.index.add(["dummy.txt"])
    remote_repo.index.commit("initial commit")

    remote_repo_commit_hexsha = remote_repo.commit("main").hexsha
    ir = initialize_repo("tests/specs/fetch_step/fetch_step_remote_valid.yml")
    with ir.initialize() as r:
        latest_commit_hexsha = r.commit("origin/main").hexsha
        assert latest_commit_hexsha == remote_repo_commit_hexsha


def test_fetch_step_missing_remote(remote_repo: Repo):
    (REMOTE_REPO_PATH / "dummy.txt").write_text("initial")
    remote_repo.index.add(["dummy.txt"])
    remote_repo.index.commit("initial commit")

    ir = initialize_repo("tests/specs/fetch_step/fetch_step_missing_remote.yml")
    with pytest.raises(ValueError, match="Missing remote 'upstream' in fetch step."):
        with ir.initialize() as _:
            pass
