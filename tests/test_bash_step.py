import os
import subprocess

import pytest

from src.repo_smith.initialize_repo import initialize_repo


def test_bash_step_missing_runs():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/bash_step/bash_step_missing_runs.yml")


def test_bash_step_invalid_runs():
    with pytest.raises(subprocess.CalledProcessError):
        repo_initializer = initialize_repo(
            "tests/specs/bash_step/bash_step_invalid_runs.yml"
        )
        with repo_initializer.initialize():
            pass


def test_bash_step():
    repo_initializer = initialize_repo("tests/specs/bash_step/bash_step.yml")
    with repo_initializer.initialize() as r:
        dirs = os.listdir(r.working_dir)
        assert (
            len(
                set(dirs)
                & {"file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"}
            )
            == 5
        )
        with open(os.path.join(r.working_dir, "file4.txt"), "r") as file:
            assert file.readlines() == ["Hello world\n"]
