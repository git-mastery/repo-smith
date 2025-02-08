from dataclasses import dataclass
from typing import List

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class AddStep(Step):
    files: List[str]

    def execute(self, repo: Repo) -> None:
        repo.index.add(self.files)
