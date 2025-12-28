from typing import Dict, List, Optional

from git import Repo
from repo_smith.command_result import CommandResult, run


class Helper:
    def __init__(self, repo: Optional[Repo], verbose: bool) -> None:
        self.repo = repo
        self.verbose = verbose

    def run(
        self,
        command: List[str],
        env: Dict[str, str] = {},
        exit_on_error: bool = False,
    ) -> CommandResult:
        return run(command, self.verbose, env, exit_on_error)
