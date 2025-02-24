from dataclasses import dataclass

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class CheckoutStep(Step):
    branch_name: str

    def execute(self, repo: Repo) -> None:
        if self.branch_name not in repo.heads:
            raise ValueError("Invalid branch name")
        repo.heads[self.branch_name].checkout()
