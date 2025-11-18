import pytest

from src.repo_smith.initialize_repo import initialize_repo


def test_step_missing_type():
    with pytest.raises(Exception):
        initialize_repo("tests/specs/step_missing_type.yml")
