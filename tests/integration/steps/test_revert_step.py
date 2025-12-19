import os

from shutil import copyfile
from git import Repo
from repo_smith.initialize_repo import initialize_repo
from tests.fixtures.git_fixtures import REMOTE_REPO_PATH, remote_repo


def test_revert_step_hash(remote_repo: Repo):
    (REMOTE_REPO_PATH / "dummy1.txt").write_text("first")
    remote_repo.index.add(["dummy1.txt"])
    remote_repo.index.commit("first commit")

    (REMOTE_REPO_PATH / "dummy2.txt").write_text("second")
    remote_repo.index.add(["dummy2.txt"])
    remote_repo.index.commit("second commit")

    (REMOTE_REPO_PATH / "dummy3.txt").write_text("third")
    remote_repo.index.add(["dummy3.txt"])
    remote_repo.index.commit("third commit")

    (REMOTE_REPO_PATH / "dummy4.txt").write_text("fourth")
    remote_repo.index.add(["dummy4.txt"])
    remote_repo.index.commit("fourth commit")

    full_hash = remote_repo.commit("HEAD~1").hexsha

    copyfile(
        "tests/specs/revert_step/revert_step_hash.yml",
        "tests/specs/revert_step/temp-1.yml"
        )

    with open("tests/specs/revert_step/temp-1.yml", "a") as f:
        f.write(full_hash)

    ir = initialize_repo("tests/specs/revert_step/temp-1.yml")
    with ir.initialize() as r:
        commits = list(r.iter_commits("main"))
        commit = commits[0]
        assert "Revert" in commit.message

    os.remove("tests/specs/revert_step/temp-1.yml")


def test_revert_step_short_hash(remote_repo: Repo):
    (REMOTE_REPO_PATH / "dummy1.txt").write_text("first")
    remote_repo.index.add(["dummy1.txt"])
    remote_repo.index.commit("first commit")

    (REMOTE_REPO_PATH / "dummy2.txt").write_text("second")
    remote_repo.index.add(["dummy2.txt"])
    remote_repo.index.commit("second commit")

    (REMOTE_REPO_PATH / "dummy3.txt").write_text("third")
    remote_repo.index.add(["dummy3.txt"])
    remote_repo.index.commit("third commit")

    (REMOTE_REPO_PATH / "dummy4.txt").write_text("fourth")
    remote_repo.index.add(["dummy4.txt"])
    remote_repo.index.commit("fourth commit")

    short_hash = remote_repo.commit("HEAD~1").hexsha[:7]

    copyfile(
        "tests/specs/revert_step/revert_step_short_hash.yml",
        "tests/specs/revert_step/temp-2.yml"
        )

    with open("tests/specs/revert_step/temp-2.yml", "a") as f:
        f.write(short_hash)

    ir = initialize_repo("tests/specs/revert_step/temp-2.yml")
    with ir.initialize() as r:
        commits = list(r.iter_commits("main"))
        commit = commits[0]
        assert "Revert" in commit.message

    os.remove("tests/specs/revert_step/temp-2.yml")


def test_revert_step_relative(remote_repo: Repo):
    (REMOTE_REPO_PATH / "dummy1.txt").write_text("first")
    remote_repo.index.add(["dummy1.txt"])
    remote_repo.index.commit("first commit")

    (REMOTE_REPO_PATH / "dummy2.txt").write_text("second")
    remote_repo.index.add(["dummy2.txt"])
    remote_repo.index.commit("second commit")

    (REMOTE_REPO_PATH / "dummy3.txt").write_text("third")
    remote_repo.index.add(["dummy3.txt"])
    remote_repo.index.commit("third commit")

    (REMOTE_REPO_PATH / "dummy4.txt").write_text("fourth")
    remote_repo.index.add(["dummy4.txt"])
    remote_repo.index.commit("fourth commit")

    ir = initialize_repo("tests/specs/revert_step/revert_step_relative.yml")
    with ir.initialize() as r:
        commits = list(r.iter_commits("main"))
        commit = commits[0]
        assert "Revert" in commit.message
