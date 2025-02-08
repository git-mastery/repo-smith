import os
import re
import shutil
import tempfile
from contextlib import contextmanager
from typing import Any, Callable, Dict, Iterator, Set, TypeAlias

import yaml
from git import Repo

import repo_smith.steps.add_step
import repo_smith.steps.commit_step
import repo_smith.steps.file_step
import repo_smith.steps.tag_step
from repo_smith.spec import Spec
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType

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
    def initialize(self) -> Iterator[Repo]:
        tmp_dir = tempfile.mkdtemp()
        try:
            repo = Repo.init(tmp_dir)
            for step in self.__spec.steps:
                if step.id in self.__pre_hooks:
                    self.__pre_hooks[step.id](repo)

                step.execute(repo=repo)

                if step.id in self.__post_hooks:
                    self.__post_hooks[step.id](repo)
            yield repo
        finally:
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
        if "name" not in spec:
            raise ValueError('Missing "name" field in spec.')

        steps = []
        for step in spec.get("initialization", {}).get("steps", []):
            steps.append(self.__parse_step(step))

        return Spec(name=spec["name"], description=spec.get("description"), steps=steps)

    def __parse_step(self, step: Any) -> Step:
        if "name" not in step:
            raise ValueError('Missing "name" field in step.')

        if "type" not in step:
            raise ValueError('Missing "type" field in step.')

        name = step["name"]
        description = step.get("description")
        step_type = StepType.from_value(step["type"])
        id = step.get("id")

        if step_type == StepType.COMMIT:
            if "message" not in step:
                raise ValueError('Missing "message" field in commit step.')

            return repo_smith.steps.commit_step.CommitStep(
                name=name,
                description=description,
                step_type=StepType.COMMIT,
                id=id,
                empty=step.get("empty", False),
                message=step["message"],
            )
        elif step_type == StepType.ADD:
            if "files" not in step:
                raise ValueError('Missing "files" field in add step.')

            if step["files"] == []:
                raise ValueError('Empty "files" list in add step.')

            return repo_smith.steps.add_step.AddStep(
                name=name,
                description=description,
                step_type=StepType.ADD,
                id=id,
                files=step["files"],
            )
        elif step_type == StepType.TAG:
            if "tag-name" not in step:
                raise ValueError('Missing "tag-name" field in tag step.')

            if step["tag-name"].strip() == "":
                raise ValueError('Empty "tag-name" field in tag step.')

            tag_name_regex = "^[0-9a-zA-Z-_.]*$"
            if re.search(tag_name_regex, step["tag-name"]) is None:
                raise ValueError(
                    'Field "tag-name" can only contain alphanumeric characters, _, -, .'
                )

            return repo_smith.steps.tag_step.TagStep(
                name=name,
                description=description,
                step_type=StepType.TAG,
                id=id,
                tag_name=step["tag-name"],
                tag_message=step.get("tag-message"),
            )
        elif step_type in {
            StepType.NEW_FILE,
            StepType.APPEND_FILE,
            StepType.EDIT_FILE,
            StepType.DELETE_FILE,
        }:
            if "filename" not in step:
                raise ValueError('Missing "filename" field in file step.')

            filename = step["filename"]
            contents = step.get("contents", "")

            match step_type:
                case StepType.NEW_FILE:
                    return repo_smith.steps.file_step.NewFileStep(
                        name=name,
                        description=description,
                        step_type=step_type,
                        id=id,
                        filename=filename,
                        contents=contents,
                    )
                case StepType.EDIT_FILE:
                    return repo_smith.steps.file_step.EditFileStep(
                        name=name,
                        description=description,
                        step_type=step_type,
                        id=id,
                        filename=filename,
                        contents=contents,
                    )
                case StepType.DELETE_FILE:
                    return repo_smith.steps.file_step.DeleteFileStep(
                        name=name,
                        description=description,
                        step_type=step_type,
                        id=id,
                        filename=filename,
                        contents=contents,
                    )
                case StepType.APPEND_FILE:
                    return repo_smith.steps.file_step.AppendFileStep(
                        name=name,
                        description=description,
                        step_type=step_type,
                        id=id,
                        filename=filename,
                        contents=contents,
                    )
        else:
            raise ValueError('Improper "type" field in spec.')


def initialize_repo(spec_path: str) -> RepoInitializer:
    if not os.path.isfile(spec_path):
        raise ValueError("Invalid spec_path provided, not found.")

    with open(spec_path, "rb") as spec_file:
        try:
            spec_data = yaml.safe_load(spec_file)
            return RepoInitializer(spec_data)
        except Exception as e:
            raise e
