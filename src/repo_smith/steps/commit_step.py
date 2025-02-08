from dataclasses import dataclass

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class CommitStep(Step):
    empty: bool
    message: str

    def execute(self, repo: Repo) -> None:
        if self.empty:
            repo.git.commit("-m", self.message, "--allow-empty")
        else:
            repo.index.commit(message=self.message)
