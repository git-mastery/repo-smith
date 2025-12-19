from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import BadName, Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class CheckoutStep(Step):
    branch_name: Optional[str]
    commit_hash: Optional[str]
    start_point: Optional[str]

    step_type: StepType = field(init=False, default=StepType.CHECKOUT)

    def execute(self, repo: Repo) -> None:
        if self.branch_name is not None:
            if self.start_point is not None:
                if self.branch_name in repo.heads:
                    raise ValueError(
                        f'Branch "{self.branch_name}" already exists. Cannot use "start-point" with an existing branch in checkout step.'
                    )
                repo.git.checkout("-b", self.branch_name, self.start_point)
            elif self.branch_name not in repo.heads:
                raise ValueError("Invalid branch name")
            else:
                repo.heads[self.branch_name].checkout()

        if self.commit_hash:
            try:
                commit = repo.commit(self.commit_hash)
                repo.git.checkout(commit)
            except (ValueError, BadName):
                raise ValueError("Commit not found")

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if step.get("branch-name") is None and step.get("commit-hash") is None:
            raise ValueError(
                'Provide either "branch-name" or "commit-hash" in checkout step.'
            )

        if step.get("branch-name") is not None and step.get("commit-hash") is not None:
            raise ValueError(
                'Provide either "branch-name" or "commit-hash", not both, in checkout step.'
            )

        if step.get("branch-name") is not None and step["branch-name"].strip() == "":
            raise ValueError('Empty "branch-name" field in checkout step.')

        if step.get("branch-name") is None and step.get("start-point") is not None:
            raise ValueError(
                '"start-point" field requires "branch-name" field to be provided in checkout step.'
            )

        if step.get("commit-hash") is not None and step["commit-hash"].strip() == "":
            raise ValueError('Empty "commit-hash" field in checkout step.')

        if step.get("start-point") is not None and step["start-point"].strip() == "":
            raise ValueError('Empty "start-point" field in checkout step.')

        return cls(
            name=name,
            description=description,
            id=id,
            branch_name=step.get("branch-name"),
            commit_hash=step.get("commit-hash"),
            start_point=step.get("start-point"),
        )
