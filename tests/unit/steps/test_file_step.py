import pytest
from repo_smith.steps.file_step import (
    AppendFileStep,
    DeleteFileStep,
    EditFileStep,
    FileStep,
    NewFileStep,
)


def test_file_step_get_details_missing_filename():
    with pytest.raises(ValueError, match='Missing "filename" field in file step.'):
        FileStep.get_details({})


def test_file_step_get_details_empty_filename():
    with pytest.raises(ValueError, match='Empty "filename" field in file step.'):
        FileStep.get_details({"filename": ""})


def test_file_step_get_details_missing_contents():
    filename, contents = FileStep.get_details({"filename": "hello.txt"})
    assert filename == "hello.txt"
    assert contents == ""


def test_file_step_get_details():
    filename, contents = FileStep.get_details(
        {"filename": "hello.txt", "contents": "Hello world"}
    )
    assert filename == "hello.txt"
    assert contents == "Hello world"


FILE_STEP_CLASSES = [NewFileStep, EditFileStep, AppendFileStep, DeleteFileStep]


@pytest.mark.parametrize("step_class", FILE_STEP_CLASSES)
def test_new_file_step_parse(step_class):
    step = step_class.parse(
        "n", "d", "id", {"filename": "hello.txt", "contents": "Hello world"}
    )
    assert isinstance(step, step_class)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.filename == "hello.txt"
    assert step.contents == "Hello world"
