import pytest
from repo_smith.steps.tag_step import TagStep


def test_tag_step_parse_missing_tag_name():
    with pytest.raises(ValueError, match='Missing "tag-name" field in tag step.'):
        TagStep.parse("n", "d", "id", {})


def test_tag_step_parse_empty_tag_name():
    with pytest.raises(ValueError, match='Empty "tag-name" field in tag step.'):
        TagStep.parse("n", "d", "id", {"tag-name": ""})


def test_tag_step_parse_invalid_tag_name():
    with pytest.raises(
        ValueError,
        match='Field "tag-name" can only contain alphanumeric characters, _, -, .',
    ):
        TagStep.parse("n", "d", "id", {"tag-name": "(open)"})


def test_tag_step_parse_missing_tag_message():
    step = TagStep.parse("n", "d", "id", {"tag-name": "start"})
    assert isinstance(step, TagStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.tag_name == "start"
    assert step.tag_message is None


def test_tag_step_parse_with_tag_message():
    step = TagStep.parse(
        "n", "d", "id", {"tag-name": "start", "tag-message": "this is a message"}
    )
    assert isinstance(step, TagStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.tag_name == "start"
    assert step.tag_message == "this is a message"
