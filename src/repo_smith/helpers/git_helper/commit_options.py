from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class CommitOptions(TypedDict, total=False):
    all: bool
    reuse_message: str
    message: str
    allow_empty: bool
    no_edit: bool


COMMIT_SPEC = (
    CommandSpec()
    .flag("all", "-a", default=False)
    .opt("reuse_message", "--reuse-message")
    .opt("message", "-m")
    .flag("allow_empty", "--allow-empty", default=False)
    .flag("no_edit", "--no-edit", default=False)
)
