from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class RepoForkOptions(TypedDict, total=False):
    clone: bool
    default_branch_only: bool
    fork_name: str
    org: str
    remote: bool
    remote_name: str


REPO_FORK_SPEC = (
    CommandSpec()
    .bool_opt("clone", "--clone", default=False, transform=lambda v: str(v).lower())
    .bool_opt("remote", "--remote", default=True, transform=lambda v: str(v).lower())
    .flag("default_branch_only", "--default-branch-only", default=False)
    .opt("org", "--org")
    .opt("fork_name", "--fork-name")
    .opt("remote_name", "--remote-name")
)
