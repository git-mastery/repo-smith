from typing import Any, Type

from repo_smith.steps.add_step import AddStep
from repo_smith.steps.bash_step import BashStep
from repo_smith.steps.branch_delete_step import BranchDeleteStep
from repo_smith.steps.branch_rename_step import BranchRenameStep
from repo_smith.steps.branch_step import BranchStep
from repo_smith.steps.checkout_step import CheckoutStep
from repo_smith.steps.commit_step import CommitStep
from repo_smith.steps.fetch_step import FetchStep
from repo_smith.steps.file_step import (
    AppendFileStep,
    DeleteFileStep,
    EditFileStep,
    NewFileStep,
)
from repo_smith.steps.merge_step import MergeStep
from repo_smith.steps.remote_step import RemoteStep
from repo_smith.steps.reset_step import ResetStep
from repo_smith.steps.revert_step import RevertStep
from repo_smith.steps.step import Step
from repo_smith.steps.step_type import StepType
from repo_smith.steps.tag_step import TagStep


class Dispatcher:
    @staticmethod
    def dispatch(step: Any) -> Step:
        if "type" not in step:
            raise ValueError('Missing "type" field in step.')

        name = step.get("name")
        description = step.get("description")
        step_type = StepType.from_value(step["type"])
        id = step.get("id")
        retrieved_step_type = Dispatcher.__get_type(step_type)
        return retrieved_step_type.parse(name, description, id, step)

    @staticmethod
    def __get_type(step_type: StepType) -> Type[Step]:
        match step_type:
            case StepType.COMMIT:
                return CommitStep
            case StepType.ADD:
                return AddStep
            case StepType.TAG:
                return TagStep
            case StepType.BASH:
                return BashStep
            case StepType.BRANCH:
                return BranchStep
            case StepType.BRANCH_RENAME:
                return BranchRenameStep
            case StepType.BRANCH_DELETE:
                return BranchDeleteStep
            case StepType.CHECKOUT:
                return CheckoutStep
            case StepType.MERGE:
                return MergeStep
            case StepType.REMOTE:
                return RemoteStep
            case StepType.RESET:
                return ResetStep
            case StepType.REVERT:
                return RevertStep
            case StepType.FETCH:
                return FetchStep
            case StepType.NEW_FILE:
                return NewFileStep
            case StepType.EDIT_FILE:
                return EditFileStep
            case StepType.DELETE_FILE:
                return DeleteFileStep
            case StepType.APPEND_FILE:
                return AppendFileStep
