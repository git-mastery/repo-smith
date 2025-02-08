from dataclasses import dataclass
from typing import Optional

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class TagStep(Step):
    tag_name: str
    tag_message: Optional[str]

    def execute(self, repo: Repo) -> None:
        repo.create_tag(self.tag_name, message=self.tag_message)
