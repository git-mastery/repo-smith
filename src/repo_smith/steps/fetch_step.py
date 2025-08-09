from dataclasses import dataclass

from git import Repo

from repo_smith.steps.step import Step

# TODO: This needs a unit test file


@dataclass
class FetchStep(Step):
    remote_name: str

    def execute(self, repo: Repo) -> None:
        try:
            remote = repo.remote(self.remote_name)
        except Exception:
            raise ValueError(f"Missing remote '{self.remote_name}'")

        remote.fetch()
