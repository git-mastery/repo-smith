from dataclasses import dataclass

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class MergeStep(Step):
    branch_name: str

    def execute(self, repo: Repo) -> None:
        repo.git.merge(self.branch_name, "--no-edit")
