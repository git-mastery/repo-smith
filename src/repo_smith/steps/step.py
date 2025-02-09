from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

from git import Repo

from repo_smith.steps.step_type import StepType


@dataclass
class Step(ABC):
    name: Optional[str]
    step_type: StepType
    description: Optional[str]
    id: Optional[str]

    @abstractmethod
    def execute(self, repo: Repo) -> None:
        pass
