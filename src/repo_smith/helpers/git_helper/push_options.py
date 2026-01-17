from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class PushOptions(TypedDict, total=False):
    set_upstream: bool
    force: bool
    all: bool
    tags: bool


PUSH_SPEC = (
    CommandSpec()
    .flag("set_upstream", "--set-upstream", default=False)
    .flag("force", "--force", default=False)
    .flag("all", "--all", default=False)
    .flag("tags", "--tags", default=False)
)
