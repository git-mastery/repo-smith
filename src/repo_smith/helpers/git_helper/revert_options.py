from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class RevertOptions(TypedDict, total=False):
    no_commit: bool


REVERT_SPEC = CommandSpec().flag("no_commit", "--no-commit", default=False)
