from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class RemoteAddOptions(TypedDict, total=False):
    fetch: bool
    tags: bool
    no_tags: bool


REMOTE_ADD_SPEC = (
    CommandSpec()
    .flag("fetch", "-f", default=False)
    .flag("tags", "--tags", default=False)
    .flag("no_tags", "--no-tags", default=False)
)
