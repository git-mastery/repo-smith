from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class FetchStep(Step):
    remote_name: str

    step_type: StepType = field(init=False, default=StepType.FETCH)

    def execute(self, repo: Repo) -> None:
        try:
            remote = repo.remote(self.remote_name)
        except Exception:
            raise ValueError(f"Missing remote '{self.remote_name}' in fetch step.")

        remote.fetch()

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "remote-name" not in step:
            raise ValueError('Missing "remote-name" field in fetch step.')

        if step["remote-name"] is None or step["remote-name"].strip() == "":
            raise ValueError('Empty "remote-name" field in fetch step.')

        return cls(
            name=name,
            description=description,
            id=id,
            remote_name=step["remote-name"],
        )
