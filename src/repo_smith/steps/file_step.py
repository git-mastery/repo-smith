import os
import os.path
from dataclasses import dataclass
import pathlib

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class FileStep(Step):
    filename: str
    contents: str


class NewFileStep(FileStep):
    def execute(self, repo: Repo) -> None:
        rw_dir = repo.working_dir
        filepath = os.path.join(rw_dir, self.filename)
        filepath_dir_only = os.path.dirname(filepath)
        pathlib.Path(filepath_dir_only).mkdir(parents=True, exist_ok=True)
        with open(filepath, "w+") as fs:
            fs.write(self.contents)


class EditFileStep(FileStep):
    def execute(self, repo: Repo) -> None:
        rw_dir = repo.working_dir
        filepath = os.path.join(rw_dir, self.filename)
        if not os.path.isfile(filepath):
            raise ValueError("Invalid filename for editing")
        with open(filepath, "w") as fs:
            fs.write(self.contents)


class DeleteFileStep(FileStep):
    def execute(self, repo: Repo) -> None:
        rw_dir = repo.working_dir
        filepath = os.path.join(rw_dir, self.filename)
        if not os.path.isfile(filepath):
            raise ValueError("Invalid filename for deleting")
        os.remove(filepath)


class AppendFileStep(FileStep):
    def execute(self, repo: Repo) -> None:
        rw_dir = repo.working_dir
        filepath = os.path.join(rw_dir, self.filename)
        if not os.path.isfile(filepath):
            raise ValueError("Invalid filename for appending")
        with open(filepath, "a") as fs:
            fs.write(self.contents)
