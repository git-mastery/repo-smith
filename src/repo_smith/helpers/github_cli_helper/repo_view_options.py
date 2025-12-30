from typing import List, TypedDict, Union

from repo_smith.helpers.command_spec import CommandSpec
from repo_smith.helpers.github_cli_helper.fields import JSON_FIELDS


class RepoViewOptions(TypedDict, total=False):
    branch: str
    jq: str
    json: Union[JSON_FIELDS, List[JSON_FIELDS]]


REPO_VIEW_SPEC = (
    CommandSpec()
    .opt("branch", "--branch")
    .opt("jq", "--jq")
    .opt(
        "json", "--json", transform=lambda v: ",".join(v) if isinstance(v, list) else v
    )
)
