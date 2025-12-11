from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class RevertStep(Step):
    commit: str

    step_type: StepType = field(init=False, default=StepType.REVERT)

    def execute(self, repo: Repo) -> None:
        revert_args = [self.commit, "--no-edit"]

        repo.git.revert(*revert_args)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "commit" not in step:
            raise ValueError('Missing "commit" field in revert step.')

        if step["commit"] is None or step["commit"].strip() == "":
            raise ValueError('Empty "commit" field in revert step.')

        return cls(
            name=name,
            description=description,
            id=id,
            commit=step["commit"],
        )
