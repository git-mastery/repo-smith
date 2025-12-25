import tempfile
from contextlib import contextmanager
from typing import Iterator, TypedDict, Unpack

from git.repo import Repo

from repo_smith.helpers.files_helper import FilesHelper
from repo_smith.helpers.git_helper.git_helper import GitHelper
from repo_smith.helpers.gitmastery_helper import GitMasteryHelper


class RepoSmith:
    def __init__(self, repo: Repo, verbose: bool) -> None:
        self.verbose = verbose
        self.repo = repo
        self.files = FilesHelper(repo, verbose)
        self.git = GitHelper(repo, verbose)
        self.git_mastery = GitMasteryHelper(repo, verbose)


class CreateRepoOptions(TypedDict, total=False):
    clone_from: str
    existing_path: str


@contextmanager
def create_repo_smith(
    verbose: bool, **options: Unpack[CreateRepoOptions]
) -> Iterator[RepoSmith]:
    """Creates a RepoSmith instance over a given repository."""
    clone_from = options.get("clone_from")
    existing_path = options.get("existing_path")

    dir = tempfile.mkdtemp() if existing_path is None else existing_path

    if clone_from:
        repo = Repo.clone_from(clone_from, dir)
    else:
        repo = Repo.init(dir, initial_branch="main")

    yield RepoSmith(repo, verbose)
