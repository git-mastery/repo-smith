from unittest.mock import patch

import pytest
from repo_smith.steps.add_step import AddStep
from repo_smith.steps.bash_step import BashStep
from repo_smith.steps.branch_delete_step import BranchDeleteStep
from repo_smith.steps.branch_rename_step import BranchRenameStep
from repo_smith.steps.branch_step import BranchStep
from repo_smith.steps.checkout_step import CheckoutStep
from repo_smith.steps.commit_step import CommitStep
from repo_smith.steps.dispatcher import Dispatcher
from repo_smith.steps.fetch_step import FetchStep
from repo_smith.steps.file_step import (
    AppendFileStep,
    DeleteFileStep,
    EditFileStep,
    NewFileStep,
)
from repo_smith.steps.merge_step import MergeStep
from repo_smith.steps.remote_step import RemoteStep
from repo_smith.steps.step_type import StepType
from repo_smith.steps.tag_step import TagStep


def test_dispatch_calls_correct_step_parse():
    step_dict = {
        "type": "commit",
        "name": "my commit",
        "description": "desc",
        "id": "123",
    }

    # Patch CommitStep.parse so we don't run real logic
    with patch(
        "repo_smith.steps.commit_step.CommitStep.parse", return_value="parsed"
    ) as mock_parse:
        result = Dispatcher.dispatch(step_dict)

    # parse should have been called once with correct arguments
    mock_parse.assert_called_once_with("my commit", "desc", "123", step_dict)

    # The dispatcher should return whatever parse returned
    assert result == "parsed"


def test_dispatch_missing_type_raises():
    step_dict = {"name": "no type"}
    with pytest.raises(ValueError, match='Missing "type" field in step.'):
        Dispatcher.dispatch(step_dict)


STEP_TYPES_TO_CLASSES = {
    StepType.COMMIT: CommitStep,
    StepType.ADD: AddStep,
    StepType.TAG: TagStep,
    StepType.NEW_FILE: NewFileStep,
    StepType.EDIT_FILE: EditFileStep,
    StepType.DELETE_FILE: DeleteFileStep,
    StepType.APPEND_FILE: AppendFileStep,
    StepType.BASH: BashStep,
    StepType.BRANCH: BranchStep,
    StepType.BRANCH_RENAME: BranchRenameStep,
    StepType.BRANCH_DELETE: BranchDeleteStep,
    StepType.CHECKOUT: CheckoutStep,
    StepType.REMOTE: RemoteStep,
    StepType.MERGE: MergeStep,
    StepType.FETCH: FetchStep,
}


@pytest.mark.parametrize("step_type, step_path", STEP_TYPES_TO_CLASSES.items())
def test_get_type_returns_correct_class(step_type, step_path):
    # Uses mangled name: https://stackoverflow.com/questions/2064202/private-members-in-python
    assert Dispatcher._Dispatcher__get_type(step_type) is step_path  # type: ignore
