from dataclasses import dataclass

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class MergeStep(Step):
    branch_name: str
    no_fast_forward: bool

    def execute(self, repo: Repo) -> None:
        if self.no_fast_forward:
            repo.git.merge(self.branch_name, "--no-edit", "--no-ff")
        else:
            repo.git.merge(self.branch_name, "--no-edit")
