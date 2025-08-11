from dataclasses import dataclass

from git import Repo
from repo_smith.steps.step import Step


@dataclass
class BranchRenameStep(Step):
    original_branch_name: str
    target_branch_name: str

    def execute(self, repo: Repo) -> None:
        branch = repo.heads[self.original_branch_name]
        branch.rename(self.target_branch_name)
