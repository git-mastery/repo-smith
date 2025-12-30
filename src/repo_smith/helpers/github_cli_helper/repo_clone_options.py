from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class RepoCloneOptions(TypedDict, total=False):
    upstream_remote_name: str


REPO_CLONE_SPEC = CommandSpec().opt(
    "upstream_remote_name", "--upstream-remote-name", default="upstream"
)
