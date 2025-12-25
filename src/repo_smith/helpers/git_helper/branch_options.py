from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class BranchOptions(TypedDict, total=False):
    delete: bool
    force: bool
    move: bool
    copy: bool

    set_upstream_to: str
    unset_upstream: bool


BRANCH_SPEC = (
    CommandSpec()
    .flag("delete", "--delete", default=False)
    .flag("force", "--force", default=False)
    .flag("move", "--move", default=False)
    .flag("copy", "--copy", default=False)
    .opt("set_upstream_to", "--set-upstream-to")
    .flag("unset_upstream", "--unset-upstream", default=False)
)
