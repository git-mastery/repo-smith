from dataclasses import dataclass
from typing import Optional

from git import BadName, Repo

from repo_smith.steps.step import Step


@dataclass
class CheckoutStep(Step):
    branch_name: Optional[str]
    commit_hash: Optional[str]

    def execute(self, repo: Repo) -> None:
        if self.branch_name is not None:
            if self.branch_name not in repo.heads:
                raise ValueError("Invalid branch name")
            else:
                repo.heads[self.branch_name].checkout()

        if self.commit_hash:
            try:
                commit = repo.commit(self.commit_hash)
                repo.git.checkout(commit)
            except (ValueError, BadName):
                raise ValueError("Commit not found")
