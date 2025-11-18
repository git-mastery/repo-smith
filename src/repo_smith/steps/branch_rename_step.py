from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class BranchRenameStep(Step):
    original_branch_name: str
    target_branch_name: str

    step_type: StepType = field(init=False, default=StepType.BRANCH)

    def execute(self, repo: Repo) -> None:
        branch = repo.heads[self.original_branch_name]
        branch.rename(self.target_branch_name)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "branch-name" not in step:
            raise ValueError('Missing "branch-name" field in branch-rename step.')

        if step["branch-name"] is None or step["branch-name"].strip() == "":
            raise ValueError('Empty "branch-name" field in branch-rename step.')

        if "new-name" not in step:
            raise ValueError('Missing "new-name" field in branch-rename step.')

        if step["new-name"] is None or step["new-name"].strip() == "":
            raise ValueError('Empty "new-name" field in branch-rename step.')

        return cls(
            name=name,
            description=description,
            id=id,
            original_branch_name=step["branch-name"],
            target_branch_name=step["new-name"],
        )
