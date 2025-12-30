from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec


class ApiOptions(TypedDict, total=False):
    jq: str
    paginate: bool
    slurp: bool


API_SPEC = (
    CommandSpec()
    .opt("jq", "--jq")
    .flag("paginate", "--paginate")
    .flag("slurp", "--slurp")
)
