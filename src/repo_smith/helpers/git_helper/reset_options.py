from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class ResetOptions(TypedDict, total=False):
    soft: bool
    mixed: bool
    hard: bool
    merge: bool
    keep: bool


RESET_SPEC = (
    CommandSpec()
    .flag("soft", "--soft", default=False)
    .flag("mixed", "--mixed", default=False)
    .flag("hard", "--hard", default=False)
    .flag("merge", "--merge", default=False)
    .flag("keep", "--keep", default=False)
)
