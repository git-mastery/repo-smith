import tempfile
from contextlib import contextmanager
from typing import Dict, Iterator, Self, Type, TypedDict, TypeVar, Unpack

from git.repo import Repo

from repo_smith.helpers.files_helper import FilesHelper
from repo_smith.helpers.git_helper.git_helper import GitHelper
from repo_smith.helpers.helper import Helper

T = TypeVar("T", bound="Helper")


class RepoSmith:
    def __init__(self, repo: Repo, verbose: bool) -> None:
        self.verbose = verbose
        self.repo = repo
        self.files = FilesHelper(repo, verbose)
        self.git = GitHelper(repo, verbose)
        self.__additional_helpers: Dict[Type[Helper], Helper] = {}

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
