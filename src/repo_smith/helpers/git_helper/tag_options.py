from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class TagOptions(TypedDict, total=False):
    message: str
    force: bool
    delete: bool
    annotate: bool


TAG_SPEC = (
    CommandSpec()
    .opt("message", "-m")
    .flag("force", "-f", default=False)
    .flag("delete", "-d", default=False)
    .flag("annotate", "-a")
)
