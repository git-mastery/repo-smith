from dataclasses import dataclass

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class BranchStep(Step):
    branch_name: str

    def execute(self, repo: Repo) -> None:
        branch = repo.create_head(self.branch_name)
        branch.checkout()
