import pytest

from repo_smith.steps.add_step import AddStep


def test_add_step_parse_missing_files():
    with pytest.raises(ValueError, match='Missing "files" field in add step.'):
        AddStep.parse("a", "d", "id", {})


def test_add_step_parse_empty_files():
    with pytest.raises(ValueError, match='Empty "files" list in add step.'):
        AddStep.parse("a", "d", "id", {"files": []})


def test_add_step_parse():
    step = AddStep.parse("a", "d", "id", {"files": ["hello.txt"]})
    assert isinstance(step, AddStep)
    assert step.name == "a"
    assert step.description == "d"
    assert step.id == "id"
    assert step.files == ["hello.txt"]
