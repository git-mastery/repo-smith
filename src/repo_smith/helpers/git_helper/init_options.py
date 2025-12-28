from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class InitOptions(TypedDict, total=False):
    bare: bool
    template: str
    branch: str
    initial_branch: str


INIT_SPEC = (
    CommandSpec()
    .flag("bare", "--bare", default=False)
    .opt("template", "--template")
    .opt("branch", "-b")
    .opt("initial_branch", "--initial-branch", default="main")
)
