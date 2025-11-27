import re
from dataclasses import dataclass, field
from typing import Any, Optional, Self, Type

from git import Repo
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType


@dataclass
class TagStep(Step):
    tag_name: str
    tag_message: Optional[str]

    step_type: StepType = field(init=False, default=StepType.TAG)

    def execute(self, repo: Repo) -> None:
        repo.create_tag(self.tag_name, message=self.tag_message)

    @classmethod
    def parse(
        cls: Type[Self],
        name: Optional[str],
        description: Optional[str],
        id: Optional[str],
        step: Any,
    ) -> Self:
        if "tag-name" not in step:
            raise ValueError('Missing "tag-name" field in tag step.')

        if step["tag-name"] is None or step["tag-name"].strip() == "":
            raise ValueError('Empty "tag-name" field in tag step.')

        tag_name_regex = "^[0-9a-zA-Z-_.]*$"
        if re.search(tag_name_regex, step["tag-name"]) is None:
            raise ValueError(
                'Field "tag-name" can only contain alphanumeric characters, _, -, .'
            )

        return cls(
            name=name,
            description=description,
            id=id,
            tag_name=step["tag-name"],
            tag_message=step.get("tag-message"),
        )
