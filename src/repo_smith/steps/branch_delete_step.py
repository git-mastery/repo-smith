from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class BranchDeleteStep(Step):
    branch_name: str

    step_type: StepType = field(init=False, default=StepType.BRANCH_DELETE)

    def execute(self, repo: Repo) -> None:
        current_local_refs = [ref.name for ref in repo.refs]
        if self.branch_name not in current_local_refs:
            raise ValueError(
                '"branch-name" field provided does not correspond to any existing branches in branch-delete step.'
            )
        repo.delete_head(self.branch_name, force=True)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "branch-name" not in step:
            raise ValueError('Missing "branch-name" field in branch-delete step.')

        if step["branch-name"] is None or step["branch-name"].strip() == "":
            raise ValueError('Empty "branch-name" field in branch-delete step.')

        return cls(
            name=name,
            description=description,
            id=id,
            branch_name=step["branch-name"],
        )
