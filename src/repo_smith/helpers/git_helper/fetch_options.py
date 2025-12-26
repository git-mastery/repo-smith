from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class FetchOptions(TypedDict, total=False):
    all: bool
    no_all: bool

    atomic: bool
    force: bool

    no_tags: bool
    tags: bool


FETCH_SPEC = (
    CommandSpec()
    .flag("all", "--all", default=False)
    .flag("no_all", "--no-all", default=False)
    .flag("atomic", "--atomic", default=False)
    .flag("force", "--force", default=False)
    .flag("no_tags", "--no-tags", default=False)
    .flag("tags", "--tags", default=False)
)
