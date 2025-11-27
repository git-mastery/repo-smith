import os
import shutil
from pathlib import Path
from typing import Generator

import pytest
from git import Repo

DUMMY_PATH = Path("tests/dummy")
REMOTE_REPO_PATH = DUMMY_PATH / "remote_repo"


@pytest.fixture
def remote_repo() -> Generator[Repo, None, None]:
    os.makedirs(REMOTE_REPO_PATH)
    repo = Repo.init(REMOTE_REPO_PATH, initial_branch="main")

    yield repo

    shutil.rmtree(REMOTE_REPO_PATH, ignore_errors=True)
    shutil.rmtree(DUMMY_PATH, ignore_errors=True)
