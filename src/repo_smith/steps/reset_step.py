from dataclasses import dataclass, field
from typing import Any, List, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType

VALID_MODES = ("soft", "mixed", "hard")


@dataclass
class ResetStep(Step):
    revision: Optional[str]
    mode: str
    files: Optional[List[str]]

    step_type: StepType = field(init=False, default=StepType.RESET)

    def execute(self, repo: Repo) -> None:
        if self.files:
            repo.git.reset(self.revision, "--", *self.files)
        else:
            repo.git.reset(f"--{self.mode}", self.revision)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "mode" not in step:
            raise ValueError('Missing "mode" field in reset step.')

        if step["mode"] is None or step["mode"].strip().lower() not in VALID_MODES:
            raise ValueError(f'Invalid "mode" value. Must be one of: {VALID_MODES}.')

        if "revision" not in step:
            raise ValueError('Missing "revision" field in reset step.')

        if step["revision"] is None or step["revision"].strip() == "":
            raise ValueError('Empty "revision" field in reset step.')

        if "files" in step and step["files"] is not None:
            if step["files"] == []:
                raise ValueError('Empty "files" list in reset step.')

            if step["mode"] != "mixed":
                raise ValueError(
                    f'Cannot use "files" field with "{step["mode"]}" mode in reset step. Only "mixed" mode is allowed with files.'
                )

        return cls(
            name=name,
            description=description,
            id=id,
            revision=step["revision"],
            mode=step["mode"],
            files=step.get("files", None),
        )
