from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class MergeStep(Step):
    branch_name: str
    no_fast_forward: bool
    squash: bool

    step_type: StepType = field(init=False, default=StepType.MERGE)

    def execute(self, repo: Repo) -> None:
        merge_args = [self.branch_name, "--no-edit"]

        if self.squash:
            merge_args.append("--squash")
        elif self.no_fast_forward:
            merge_args.append("--no-ff")

        repo.git.merge(*merge_args)

        if self.squash:
            repo.git.commit("-m", f"Squash merge branch '{self.branch_name}'")

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if step.get("branch-name") is None:
            raise ValueError('Provide either "branch-name" in merge step.')

        return cls(
            name=name,
            description=description,
            id=id,
            branch_name=step.get("branch-name"),
            no_fast_forward=step.get("no-ff", False),
            squash=step.get("squash", False),
        )
