import pytest
from src.repo_smith.initialize_repo import initialize_repo


def test_tag_step_missing_tag_name():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/tag_step/tag_step_missing_tag_name.yml")


def test_tag_step_empty_tag_name():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/tag_step/tag_step_empty_tag_name.yml")


def test_tag_step_invalid_tag_name():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/tag_step/tag_step_invalid_tag_name.yml")


def test_tag_step():
    repo_initializer = initialize_repo("tests/specs/tag_step/tag_step.yml")
    with repo_initializer.initialize() as r:
        assert len(r.tags) == 2
        assert r.tags[0].tag is not None
        assert r.tags[0].tag.tag == "with-description"
        assert r.tags[0].tag.message == "Hello world!"
        assert r.tags[1].tag is None
        assert str(r.tags[1]) == "without-description"
