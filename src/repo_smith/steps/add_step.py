from dataclasses import dataclass, field
from typing import Any, List, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class AddStep(Step):
    files: List[str]

    step_type: StepType = field(init=False, default=StepType.ADD)

    def execute(self, repo: Repo) -> None:
        repo.index.add(self.files)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "files" not in step:
            raise ValueError('Missing "files" field in add step.')

        if step["files"] is None or step["files"] == []:
            raise ValueError('Empty "files" list in add step.')

        return cls(
            name=name,
            description=description,
            id=id,
            files=step["files"],
        )
