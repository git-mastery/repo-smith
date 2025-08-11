from dataclasses import dataclass

from git import Repo
from repo_smith.steps.step import Step


@dataclass
class BranchDeleteStep(Step):
    branch_name: str

    def execute(self, repo: Repo) -> None:
        repo.delete_head(self.branch_name, force=True)
