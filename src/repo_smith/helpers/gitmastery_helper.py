from git import Repo
from repo_smith.helpers.helper import Helper


class GitMasteryHelper(Helper):
    def __init__(self, repo: Repo, verbose: bool) -> None:
        super().__init__(repo, verbose)

    def create_start_tag(self) -> None:
        """Creates the Git-Mastery start tag."""
        all_commits = list(self.repo.iter_commits())
        first_commit = list(reversed(all_commits))[0]
        first_commit_hash = first_commit.hexsha[:7]
        start_tag = f"git-mastery-start-{first_commit_hash}"
        self.repo.create_tag(start_tag)
