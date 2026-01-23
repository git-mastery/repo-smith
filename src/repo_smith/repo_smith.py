import os
import shutil
import tempfile
from contextlib import contextmanager
from logging import shutdown
from typing import Dict, Iterator, Optional, Self, Tuple, Type, TypedDict, TypeVar, Unpack

from git.repo import Repo

from repo_smith.helpers.files_helper import FilesHelper
from repo_smith.helpers.git_helper.git_helper import GitHelper
from repo_smith.helpers.github_cli_helper.github_cli_helper import GithubCliHelper
from repo_smith.helpers.helper import Helper

T = TypeVar("T", bound="Helper")


class RepoSmith:
    def __init__(self, repo: Optional[Repo], verbose: bool) -> None:
        self.verbose = verbose
        self.__repo = repo
        self.files = FilesHelper(repo, verbose)
        self.git = GitHelper(repo, verbose)
        self.gh = GithubCliHelper(repo, verbose)
        self.__additional_helpers: Dict[Type[Helper], Helper] = {}

    @property
    def repo(self) -> Repo:
        if self.__repo is None:
            raise ValueError("Repo is None, cannot access")
        return self.__repo

    def add_helper(self, cls: Type[T]) -> Self:
        self.__additional_helpers[cls] = cls(self.repo, self.verbose)
        return self

    def helper(self, cls: Type[T]) -> T:
        if cls not in self.__additional_helpers:
            raise ValueError(f"Additional helper of {cls.__name__} not found.")
        return self.__additional_helpers[cls]


class CreateRepoOptions(TypedDict, total=False):
    clone_from: str
    existing_path: str
    null_repo: bool
    include_remote_repo: bool


@contextmanager
def create_repo_smith(
    verbose: bool, **options: Unpack[CreateRepoOptions]
) -> Iterator[Tuple[RepoSmith, Optional[RepoSmith]]]:
    """Creates a RepoSmith instance over a given repository.
    
    Returns a tuple of (local_repo_smith, remote_repo_smith).
    remote_repo_smith is None unless include_remote_repo=True.
    """
    clone_from = options.get("clone_from")
    existing_path = options.get("existing_path")
    null_repo = options.get("null_repo", False)
    include_remote_repo = options.get("include_remote_repo", False)

    dir = tempfile.mkdtemp() if existing_path is None else existing_path
    local_remote_dir = None
    remote_repo = None

    if null_repo:
        repo = None
    elif clone_from:
        repo = Repo.clone_from(clone_from, dir)
    else:
        repo = Repo.init(dir, initial_branch="main")
  
    if include_remote_repo:
        local_remote_dir = tempfile.mkdtemp()
        remote_path = os.path.join(local_remote_dir, "remote.git")
        remote_repo = Repo.init(remote_path, bare=True)

    yield (
        RepoSmith(repo, verbose),
        RepoSmith(remote_repo, verbose) if remote_repo else None,
    )

    if existing_path is None:
        # Temporary directory created, so delete it
        if repo is not None:
            repo.git.clear_cache()
        shutil.rmtree(dir)
    
    # Clean up bare repository if created
    if local_remote_dir is not None:
        shutil.rmtree(local_remote_dir, ignore_errors=True)