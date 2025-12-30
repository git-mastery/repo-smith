from typing import TypedDict

from repo_smith.helpers.command_spec import CommandSpec
from repo_smith.helpers.github_cli_helper.fields import (
    GITIGNORE_TEMPLATE,
    LICENSE,
)


class RepoCreateOptions(TypedDict, total=False):
    add_readme: bool
    clone: bool
    description: str
    disable_issues: bool
    disable_wiki: bool
    gitignore: GITIGNORE_TEMPLATE
    homepage: str
    include_all_branches: bool
    license: LICENSE

    internal: bool
    public: bool
    private: bool

    push: bool
    remote: str
    source: str
    team: str
    template: str


REPO_CREATE_SPEC = (
    CommandSpec()
    .flag("add_readme", "--add-readme", default=False)
    .flag("clone", "--clone", default=False)
    .opt("description", "--description")
    .flag("disable_issues", "--disable-issues", default=False)
    .flag("disable_wiki", "--disable-wiki", default=False)
    .opt("gitignore", "--gitignore")
    .opt("homepage", "--homepage")
    .flag("include_all_branches", "--include-all-branches", default=False)
    .opt("license", "--license")
    .flag("internal", "--internal", default=False)
    .flag("public", "--public", default=False)
    .flag("private", "--private", default=False)
    .flag("push", "--push", default=False)
    .opt("remote", "--remote")
    .opt("source", "--source")
    .opt("team", "--team")
    .opt("template", "--template")
)
