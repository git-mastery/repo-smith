from dataclasses import dataclass

from git import Repo

from repo_smith.steps.step import Step


@dataclass
class MergeStep(Step):
    branch_name: str
    no_fast_forward: bool
    squash: bool

    def execute(self, repo: Repo) -> None:
        merge_args = [self.branch_name, "--no-edit"]

        if self.squash:
            merge_args.append("--squash")
        elif self.no_fast_forward:
            merge_args.append("--no-ff")

        repo.git.merge(*merge_args)

        if self.squash:
            repo.git.commit("-m", f"Squash merge branch '{self.branch_name}'")
