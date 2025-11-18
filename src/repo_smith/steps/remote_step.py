from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class RemoteStep(Step):
    remote_name: str
    remote_url: str

    step_type: StepType = field(init=False, default=StepType.REMOTE)

    def execute(self, repo: Repo) -> None:
        repo.create_remote(self.remote_name, self.remote_url)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "remote-url" not in step:
            raise ValueError('Missing "remote-url" field in remote step.')

        if "remote-name" not in step:
            raise ValueError('Missing "remote-name" field in remote step.')

        return cls(
            name=name,
            description=description,
            id=id,
            remote_name=step["remote-name"],
            remote_url=step["remote-url"],
        )
