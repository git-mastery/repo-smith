import pytest

from repo_smith.steps.reset_step import ResetStep


def test_reset_step_parse_with_revision_and_mode():
    step = ResetStep.parse("n", "d", "id", {"revision": "HEAD~1", "mode": "mixed"})
    assert isinstance(step, ResetStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.revision == "HEAD~1"
    assert step.mode == "mixed"
    assert step.files is None


def test_reset_step_parse_with_files():
    step = ResetStep.parse(
        "n",
        "d",
        "id",
        {"revision": "HEAD", "mode": "mixed", "files": ["file1.txt", "file2.txt"]},
    )
    assert step.revision == "HEAD"
    assert step.mode == "mixed"
    assert step.files == ["file1.txt", "file2.txt"]


def test_reset_step_parse_missing_mode():
    with pytest.raises(ValueError, match='Missing "mode" field in reset step.'):
        ResetStep.parse("n", "d", "id", {"revision": "HEAD~1"})


def test_reset_step_parse_missing_revision():
    with pytest.raises(ValueError, match='Missing "revision" field in reset step.'):
        ResetStep.parse("n", "d", "id", {"mode": "hard"})


def test_reset_step_parse_empty_revision():
    with pytest.raises(ValueError, match='Empty "revision" field in reset step.'):
        ResetStep.parse("n", "d", "id", {"revision": "", "mode": "hard"})


def test_reset_step_parse_invalid_mode():
    with pytest.raises(
        ValueError,
        match="Invalid \"mode\" value. Must be one of: \\('soft', 'mixed', 'hard'\\).",
    ):
        ResetStep.parse("n", "d", "id", {"revision": "HEAD~1", "mode": "invalid"})


def test_reset_step_parse_empty_files_list():
    with pytest.raises(ValueError, match='Empty "files" list in reset step.'):
        ResetStep.parse(
            "n", "d", "id", {"revision": "HEAD", "mode": "mixed", "files": []}
        )


def test_reset_step_parse_files_with_soft_mode():
    with pytest.raises(
        ValueError,
        match='Cannot use "files" field with "soft" mode in reset step. Only "mixed" mode is allowed with files.',
    ):
        ResetStep.parse(
            "n", "d", "id", {"revision": "HEAD", "mode": "soft", "files": ["file.txt"]}
        )


def test_reset_step_parse_files_with_hard_mode():
    with pytest.raises(
        ValueError,
        match='Cannot use "files" field with "hard" mode in reset step. Only "mixed" mode is allowed with files.',
    ):
        ResetStep.parse(
            "n", "d", "id", {"revision": "HEAD", "mode": "hard", "files": ["file.txt"]}
        )
