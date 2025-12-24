import os
import textwrap
from io import TextIOWrapper
from typing import Optional

from repo_smith.helpers.helper import Helper
from repo_smith.types import FilePath


class FilesHelper(Helper):
    def __init__(self, verbose: bool) -> None:
        super().__init__(verbose)

    def create_or_update(
        self, filepath: FilePath, contents: Optional[str] = None
    ) -> None:
        """Creates or updates a file with the given content."""
        dirname = os.path.dirname(filepath)
        if dirname != "":
            os.makedirs(dirname, exist_ok=True)

        if contents is None:
            open(filepath, "a").close()
        else:
            with open(filepath, "w") as file:
                self.__write_to_file__(file, contents)

    def append(self, filepath: FilePath, contents: str) -> None:
        """Appends contents to a given file."""
        with open(filepath, "a") as file:
            self.__write_to_file__(file, contents)

    def delete(self, filepath: FilePath) -> None:
        """Deletes a given file."""
        os.remove(filepath)

    def __write_to_file__(self, file: TextIOWrapper, contents: str) -> None:
        file.write(textwrap.dedent(contents).lstrip())
