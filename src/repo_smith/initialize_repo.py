import os
import shutil
import tempfile
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, Optional, Set, TypeAlias

import yaml
from git import Repo

import repo_smith.steps.tag_step
from repo_smith.clone_from import CloneFrom
from repo_smith.spec import Spec
from repo_smith.steps.dispatcher import Dispatcher

Hook: TypeAlias = Callable[[Repo], None]


class RepoInitializer:
    def __init__(self, spec_data: Any) -> None:
        self.__spec_data = spec_data
        self.__pre_hooks: Dict[str, Hook] = {}
        self.__post_hooks: Dict[str, Hook] = {}

        self.__spec = self.__parse_spec(self.__spec_data)
        self.__validate_spec(self.__spec)
        self.__step_ids = self.__get_all_ids(self.__spec)

    @contextmanager
    def initialize(self, existing_path: Optional[str] = None) -> Iterator[Repo]:
        tmp_dir = tempfile.mkdtemp() if existing_path is None else existing_path
        repo: Optional[Repo] = None
        try:
            if self.__spec.clone_from is not None:
                repo = Repo.clone_from(self.__spec.clone_from.repo_url, tmp_dir)
            else:
                repo = Repo.init(tmp_dir, initial_branch="main")

            for step in self.__spec.steps:
                if step.id in self.__pre_hooks:
                    self.__pre_hooks[step.id](repo)

                step.execute(repo=repo)

                if step.id in self.__post_hooks:
                    self.__post_hooks[step.id](repo)
            yield repo
        finally:
            if repo is not None:
                repo.git.clear_cache()
                shutil.rmtree(tmp_dir)

    def add_pre_hook(self, id: str, hook: Hook) -> None:
        if id not in self.__step_ids:
            ids = "\n".join([f"- {id}" for id in self.__step_ids])
            raise ValueError(
                f"ID {id} not found in spec's steps. Available IDs:\n{ids}"
            )

        if id in self.__pre_hooks:
            raise ValueError(
                f"ID {id} already has a pre-hook set. Did you mean to add a post_hook instead?"
            )

        self.__pre_hooks[id] = hook

    def add_post_hook(self, id: str, hook: Hook) -> None:
        if id not in self.__step_ids:
            ids = "\n".join([f"- {id}" for id in self.__step_ids])
            raise ValueError(
                f"ID {id} not found in spec's steps. Available IDs:\n{ids}"
            )

        if id in self.__post_hooks:
            raise ValueError(
                f"ID {id} already has a post-hook set. Did you mean to add a pre_hook instead?"
            )

        self.__post_hooks[id] = hook

    def __validate_spec(self, spec: Spec) -> None:
        ids: Set[str] = set()
        tags: Set[str] = set()
        for step in spec.steps:
            if step.id is not None:
                if step.id in ids:
                    raise ValueError(
                        f"ID {step.id} is duplicated from a previous step. All IDs should be unique."
                    )
                ids.add(step.id)

            if isinstance(step, repo_smith.steps.tag_step.TagStep):
                if step.tag_name in tags:
                    raise ValueError(
                        f"Tag {step.tag_name} is already in use by a previous step. All tag names should be unique."
                    )
                tags.add(step.tag_name)

    def __get_all_ids(self, spec: Spec) -> Set[str]:
        ids = set()
        for step in spec.steps:
            if step.id is not None:
                ids.add(step.id)
        return ids

    def __parse_spec(self, spec: Any) -> Spec:
        steps = []

        for step in spec.get("initialization", {}).get("steps", []) or []:
            steps.append(Dispatcher.dispatch(step))

        clone_from = None
        if spec.get("initialization", {}).get("clone-from", None) is not None:
            clone_from = CloneFrom(
                repo_url=spec.get("initialization", {}).get("clone-from", "")
            )

        return Spec(
            name=spec.get("name", "") or "",
            description=spec.get("description", "") or "",
            steps=steps,
            clone_from=clone_from,
        )


def initialize_repo(spec_path: str) -> RepoInitializer:
    if not os.path.isfile(spec_path):
        raise ValueError("Invalid spec_path provided, not found.")

    with open(spec_path, "rb") as spec_file:
        try:
            spec_data = yaml.safe_load(spec_file)
            if spec_data is None:
                raise ValueError("Incomplete spec file.")
            return RepoInitializer(spec_data)
        except Exception as e:
            raise e
