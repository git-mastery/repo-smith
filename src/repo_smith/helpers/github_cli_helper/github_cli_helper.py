from typing import Optional, Unpack

from git import Repo
from repo_smith.command_result import CommandResult
from repo_smith.helpers.github_cli_helper.api_options import API_SPEC, ApiOptions
from repo_smith.helpers.github_cli_helper.repo_clone_options import (
    REPO_CLONE_SPEC,
    RepoCloneOptions,
)
from repo_smith.helpers.github_cli_helper.repo_create_options import (
    REPO_CREATE_SPEC,
    RepoCreateOptions,
)
from repo_smith.helpers.github_cli_helper.repo_fork_options import (
    REPO_FORK_SPEC,
    RepoForkOptions,
)
from repo_smith.helpers.github_cli_helper.repo_view_options import (
    REPO_VIEW_SPEC,
    RepoViewOptions,
)
from repo_smith.helpers.helper import Helper
from repo_smith.types import FilePath


class GithubCliHelper(Helper):
    def __init__(self, repo: Optional[Repo], verbose: bool) -> None:
        super().__init__(repo, verbose)

    def repo_view(
        self,
        owner: Optional[str] = None,
        repo: Optional[str] = None,
        **options: Unpack[RepoViewOptions],
    ) -> CommandResult:
        """Calls gh repo view."""
        if owner is None and repo is None:
            return self.run(["gh", "repo", "view"] + REPO_VIEW_SPEC.build(options))
        elif owner is None or repo is None:
            raise ValueError("You need both the owner and repo.")
        else:
            repository = f"{owner}/{repo}"
            return self.run(
                ["gh", "repo", "view", repository] + REPO_VIEW_SPEC.build(options)
            )

    def repo_create(
        self,
        owner: Optional[str],
        repo: str,
        **options: Unpack[RepoCreateOptions],
    ) -> None:
        """Calls gh repo create."""
        if owner is None:
            repository = repo
        else:
            repository = f"{owner}/{repo}"
        self.run(["gh", "repo", "create", repository] + REPO_CREATE_SPEC.build(options))

    def repo_delete(
        self,
        owner: Optional[str],
        repo: Optional[str],
    ) -> None:
        """Calls gh repo delete."""
        if owner is None and repo is None:
            self.run(["gh", "repo", "delete", "--yes"])
        elif owner is None or repo is None:
            raise ValueError("You need both the owner and repo.")
        else:
            repository = f"{owner}/{repo}"
            self.run(["gh", "repo", "delete", repository, "--yes"])

    def repo_clone(
        self,
        owner: Optional[str],
        repo: str,
        directory: Optional[FilePath] = None,
        gitflags: Optional[str] = None,
        **options: Unpack[RepoCloneOptions],
    ) -> None:
        """Calls gh repo clone."""
        if owner is None:
            repository = repo
        else:
            repository = f"{owner}/{repo}"
        trailing = [str(directory)] if directory is not None else []
        args = (
            ["gh", "repo", "clone", repository]
            + trailing
            + REPO_CLONE_SPEC.build(options)
        )
        if gitflags is not None:
            args += "--"
            args += gitflags
        self.run(args)

    def repo_fork(
        self,
        owner: Optional[str],
        repo: str,
        gitflags: Optional[str] = None,
        **options: Unpack[RepoForkOptions],
    ) -> None:
        """Calls gh repo fork."""
        if owner is None:
            repository = repo
        else:
            repository = f"{owner}/{repo}"
        args = ["gh", "repo", "fork", repository] + REPO_FORK_SPEC.build(options)
        if gitflags is not None:
            args += "--"
            args += gitflags
        self.run(args)

    def api(self, endpoint: str, **options: Unpack[ApiOptions]) -> CommandResult:
        """Calls gh api."""
        return self.run(["gh", "api", endpoint] + API_SPEC.build(options))
