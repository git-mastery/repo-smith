import pytest

from repo_smith.steps.step_type import StepType


def test_step_type_uncovered_type():
    with pytest.raises(ValueError):
        StepType.from_value("this should not be implemented")
