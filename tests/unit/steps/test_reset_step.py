import pytest

from repo_smith.steps.reset_step import ResetStep


def test_reset_step_parse_with_ref_and_mode():
    step = ResetStep.parse("n", "d", "id", {"ref": "HEAD~1", "mode": "mixed"})
    assert isinstance(step, ResetStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.ref == "HEAD~1"
    assert step.mode == "mixed"
    assert step.files is None


def test_reset_step_parse_with_files():
    step = ResetStep.parse(
        "n",
        "d",
        "id",
        {"ref": "HEAD", "mode": "mixed", "files": ["file1.txt", "file2.txt"]},
    )
    assert step.ref == "HEAD"
    assert step.mode == "mixed"
    assert step.files == ["file1.txt", "file2.txt"]


def test_reset_step_parse_missing_mode():
    with pytest.raises(ValueError, match='Missing "mode" field in reset step'):
        ResetStep.parse("n", "d", "id", {"ref": "HEAD~1"})


def test_reset_step_parse_missing_ref():
    with pytest.raises(ValueError, match='Missing "ref" field in reset step'):
        ResetStep.parse("n", "d", "id", {"mode": "hard"})


def test_reset_step_parse_empty_ref():
    with pytest.raises(ValueError, match='Empty "ref" field in reset step'):
        ResetStep.parse("n", "d", "id", {"ref": "", "mode": "hard"})


def test_reset_step_parse_invalid_mode():
    with pytest.raises(ValueError, match='Invalid "mode" value'):
        ResetStep.parse("n", "d", "id", {"ref": "HEAD~1", "mode": "invalid"})


def test_reset_step_parse_empty_files_list():
    with pytest.raises(ValueError, match='Empty "files" list in reset step'):
        ResetStep.parse("n", "d", "id", {"ref": "HEAD", "mode": "mixed", "files": []})


def test_reset_step_parse_files_with_soft_mode():
    with pytest.raises(ValueError, match='Cannot use "files" with "soft" mode'):
        ResetStep.parse(
            "n", "d", "id", {"ref": "HEAD", "mode": "soft", "files": ["file.txt"]}
        )


def test_reset_step_parse_files_with_hard_mode():
    with pytest.raises(ValueError, match='Cannot use "files" with "hard" mode'):
        ResetStep.parse(
            "n", "d", "id", {"ref": "HEAD", "mode": "hard", "files": ["file.txt"]}
        )
