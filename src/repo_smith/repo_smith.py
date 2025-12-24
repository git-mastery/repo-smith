from repo_smith.helpers.files_helper import FilesHelper
from repo_smith.helpers.git_helper.git_helper import GitHelper


class RepoSmith:
    def __init__(self, verbose: bool) -> None:
        self.verbose = verbose
        self.files = FilesHelper(verbose)
        self.git = GitHelper(verbose)
