import pytest

from repo_smith.steps.merge_step import MergeStep


def test_merge_step_parse_missing_branch_name():
    with pytest.raises(ValueError, match='Missing "branch-name" field in merge step.'):
        MergeStep.parse("n", "d", "id", {})


def test_merge_step_parse_empty_branch_name():
    with pytest.raises(ValueError, match='Empty "branch-name" field in merge step.'):
        MergeStep.parse("n", "d", "id", {"branch-name": ""})


MERGE_STEP_CONFIGURATION = {
    "no-ff not set, squash not set": {"branch-name": "test"},
    "no-ff not set, squash set": {"branch-name": "test", "squash": True},
    "no-ff set, squash not set": {"branch-name": "test", "no-ff": True},
    "no-ff set, squash set": {"branch-name": "test", "squash": True, "no-ff": True},
}


@pytest.mark.parametrize("config_name, config", MERGE_STEP_CONFIGURATION.items())
def test_merge_step_parse(config_name, config):
    step = MergeStep.parse("n", "d", "id", config)
    assert isinstance(step, MergeStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.branch_name == "test"
    assert step.no_fast_forward == config.get("no-ff", False)
    assert step.squash == config.get("squash", False)
