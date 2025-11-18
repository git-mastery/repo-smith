from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class CommitStep(Step):
    empty: bool
    message: str

    step_type: StepType = field(init=False, default=StepType.COMMIT)

    def execute(self, repo: Repo) -> None:
        if self.empty:
            repo.git.commit("-m", self.message, "--allow-empty")
        else:
            repo.index.commit(message=self.message)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "message" not in step:
            raise ValueError('Missing "message" field in commit step.')

        if step["message"] is None or step["message"].strip() == "":
            raise ValueError('Empty "message" field in commit step.')

        return cls(
            name=name,
            description=description,
            id=id,
            empty=step.get("empty", False),
            message=step["message"],
        )
