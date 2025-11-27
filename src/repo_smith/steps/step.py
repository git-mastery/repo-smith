from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional, Self, Type

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

    @classmethod
    @abstractmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        pass
