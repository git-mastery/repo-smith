from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class AddOptions(TypedDict, total=False):
    force: bool
    update: bool
    all: bool


ADD_SPEC = (
    CommandSpec()
    .flag("force", "-f", default=False)
    .flag("update", "-u", default=False)
    .flag("all", "-A", default=False)
)
