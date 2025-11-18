import os
import os.path
import pathlib
from dataclasses import dataclass, field
from typing import Any, Optional, Self, Tuple, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class FileStep(Step):
    filename: str
    contents: str

    @staticmethod
    def get_details(step: Any) -> Tuple[str, str]:
        if "filename" not in step:
            raise ValueError('Missing "filename" field in file step.')

        if step["filename"] is None or step["filename"].strip() == "":
            raise ValueError('Empty "filename" field in file step.')

        filename = step["filename"]
        contents = step.get("contents", "") or ""
        return filename, contents


@dataclass
class NewFileStep(FileStep):
    step_type: StepType = field(init=False, default=StepType.NEW_FILE)

    def execute(self, repo: Repo) -> None:
        rw_dir = repo.working_dir
        filepath = os.path.join(rw_dir, self.filename)
        filepath_dir_only = os.path.dirname(filepath)
        pathlib.Path(filepath_dir_only).mkdir(parents=True, exist_ok=True)
        with open(filepath, "w+") as fs:
            fs.write(self.contents)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        filename, contents = FileStep.get_details(step)
        return cls(
            name=name,
            description=description,
            id=id,
            filename=filename,
            contents=contents,
        )


@dataclass
class EditFileStep(FileStep):
    step_type: StepType = field(init=False, default=StepType.EDIT_FILE)

    def execute(self, repo: Repo) -> None:
        rw_dir = repo.working_dir
        filepath = os.path.join(rw_dir, self.filename)
        if not os.path.isfile(filepath):
            raise ValueError("Invalid filename for editing")
        with open(filepath, "w") as fs:
            fs.write(self.contents)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        filename, contents = FileStep.get_details(step)
        return cls(
            name=name,
            description=description,
            id=id,
            filename=filename,
            contents=contents,
        )


@dataclass
class DeleteFileStep(FileStep):
    step_type: StepType = field(init=False, default=StepType.DELETE_FILE)

    def execute(self, repo: Repo) -> None:
        rw_dir = repo.working_dir
        filepath = os.path.join(rw_dir, self.filename)
        if not os.path.isfile(filepath):
            raise ValueError("Invalid filename for deleting")
        os.remove(filepath)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        filename, contents = FileStep.get_details(step)
        return cls(
            name=name,
            description=description,
            id=id,
            filename=filename,
            contents=contents,
        )


@dataclass
class AppendFileStep(FileStep):
    step_type: StepType = field(init=False, default=StepType.APPEND_FILE)

    def execute(self, repo: Repo) -> None:
        rw_dir = repo.working_dir
        filepath = os.path.join(rw_dir, self.filename)
        if not os.path.isfile(filepath):
            raise ValueError("Invalid filename for appending")
        with open(filepath, "a") as fs:
            fs.write(self.contents)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        filename, contents = FileStep.get_details(step)
        return cls(
            name=name,
            description=description,
            id=id,
            filename=filename,
            contents=contents,
        )
