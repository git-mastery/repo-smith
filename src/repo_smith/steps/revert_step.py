from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class RevertStep(Step):
    revision: str

    step_type: StepType = field(init=False, default=StepType.REVERT)

    def execute(self, repo: Repo) -> None:
        revert_args = [self.revision, "--no-edit"]

        repo.git.revert(*revert_args)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "revision" not in step:
            raise ValueError('Missing "revision" field in revert step.')

        if step["revision"] is None or step["revision"].strip() == "":
            raise ValueError('Empty "revision" field in revert step.')

        return cls(
            name=name,
            description=description,
            id=id,
            revision=step["revision"],
        )
