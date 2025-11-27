from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class BranchStep(Step):
    branch_name: str

    step_type: StepType = field(init=False, default=StepType.BRANCH)

    def execute(self, repo: Repo) -> None:
        # TODO: Handle when attempting to create a branch when no commits exist
        branch = repo.create_head(self.branch_name)
        branch.checkout()

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "branch-name" not in step:
            raise ValueError('Missing "branch-name" field in branch step.')

        if step["branch-name"] is None or step["branch-name"].strip() == "":
            raise ValueError('Empty "branch-name" field in branch step.')

        return cls(
            name=name,
            description=description,
            id=id,
            branch_name=step["branch-name"],
        )
