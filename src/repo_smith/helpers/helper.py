from typing import Dict, List

from repo_smith.command_result import CommandResult, run


class Helper:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose

    def run(
        self,
        command: List[str],
        env: Dict[str, str] = {},
        exit_on_error: bool = False,
    ) -> CommandResult:
        return run(command, self.verbose, env, exit_on_error)

