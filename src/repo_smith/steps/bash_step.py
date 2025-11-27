import subprocess
from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class BashStep(Step):
    body: str

    step_type: StepType = field(init=False, default=StepType.BASH)

    def execute(self, repo: Repo) -> None:
        subprocess.check_call(
            self.body.strip(), shell=True, executable="/bin/bash", cwd=repo.working_dir
        )

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "runs" not in step:
            raise ValueError('Missing "runs" field in bash step.')

        if step["runs"] is None or step["runs"].strip() == "":
            raise ValueError('Empty "runs" field in bash step.')

        return cls(
            name=name,
            description=description,
            id=id,
            body=step["runs"],
        )
