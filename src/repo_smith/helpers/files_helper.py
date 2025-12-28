import os
import shutil
import stat
import textwrap
from io import TextIOWrapper
from typing import Optional

from git import Repo
from repo_smith.helpers.helper import Helper
from repo_smith.types import FilePath


class FilesHelper(Helper):
    def __init__(self, repo: Optional[Repo], verbose: bool) -> None:
        super().__init__(repo, verbose)

    def create_or_update(
        self, filepath: FilePath, contents: Optional[str] = None
    ) -> None:
        """Creates or updates a file with the given content."""
        dirname = os.path.dirname(filepath)
        if dirname != "":
            os.makedirs(dirname, exist_ok=True)

        if contents is None:
            with open(filepath, "a"):
                pass
        else:
            with open(filepath, "w") as file:
                self.__write_to_file__(file, contents)

    def append(self, filepath: FilePath, contents: str) -> None:
        """Appends contents to a given file."""
        with open(filepath, "a") as file:
            self.__write_to_file__(file, contents)

    def delete(self, filepath: FilePath) -> None:
        """Deletes a given file."""
        if os.path.isdir(filepath):

            def force_remove_readonly(func, path, _):
                os.chmod(path, stat.S_IWRITE)
                func(path)

            shutil.rmtree(filepath, onerror=force_remove_readonly)
        else:
            os.remove(filepath)

    def mkdir(self, dir: FilePath) -> None:
        os.makedirs(dir, exist_ok=True)

    def cd(self, dir: FilePath) -> None:
        os.chdir(dir)

    def chmod(self, filepath: FilePath, mode: int) -> None:
        os.chmod(filepath, mode)

    def __write_to_file__(self, file: TextIOWrapper, contents: str) -> None:
        file.write(textwrap.dedent(contents).lstrip())
