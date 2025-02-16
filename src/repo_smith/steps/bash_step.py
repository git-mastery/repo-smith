import subprocess

from dataclasses import dataclass

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class BashStep(Step):
    body: str

    def execute(self, repo: Repo) -> None:  # type: ignore
        subprocess.check_call(self.body.strip(), shell=True, cwd=repo.working_dir)
