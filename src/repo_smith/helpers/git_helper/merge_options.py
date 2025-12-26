from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class MergeOptions(TypedDict, total=False):
    commit: bool
    no_commit: bool

    ff: bool
    no_ff: bool
    ff_only: bool

    squash: bool
    no_squash: bool

    message: str


MERGE_SPEC = (
    CommandSpec()
    .flag("commit", "--commit", default=False)
    .flag("no_commit", "--no-commit", default=False)
    .flag("ff", "--f", default=False)
    .flag("no_ff", "--no-ff", default=False)
    .flag("ff_only", "--ff-only", default=False)
    .flag("squash", "--squash", default=False)
    .flag("no_squash", "--no-squash", default=False)
    .opt("message", "-m")
)
