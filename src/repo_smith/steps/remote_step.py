from dataclasses import dataclass

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class RemoteStep(Step):
    remote_name: str
    remote_url: str

    def execute(self, repo: Repo) -> None:
        repo.create_remote(self.remote_name, self.remote_url)
