import pytest

from repo_smith.steps.checkout_step import CheckoutStep


def test_checkout_step_parse_missing_branch_name_and_commit_hash():
    with pytest.raises(
        ValueError,
        match='Provide either "branch-name" or "commit-hash" in checkout step.',
    ):
        CheckoutStep.parse("n", "d", "id", {})


def test_checkout_step_parse_both_branch_name_and_commit_hash():
    with pytest.raises(
        ValueError,
        match='Provide either "branch-name" or "commit-hash", not both, in checkout step.',
    ):
        CheckoutStep.parse(
            "n", "d", "id", {"branch-name": "test", "commit-hash": "abc123"}
        )


def test_checkout_step_parse_start_point_with_commit_hash():
    with pytest.raises(
        ValueError,
        match='"start-point" field requires "branch-name" field to be provided in checkout step.',
    ):
        CheckoutStep.parse(
            "n", "d", "id", {"start-point": "HEAD~1", "commit-hash": "abc123"}
        )


def test_checkout_step_parse_empty_branch_name():
    with pytest.raises(ValueError, match='Empty "branch-name" field in checkout step.'):
        CheckoutStep.parse("n", "d", "id", {"branch-name": ""})


def test_checkout_step_parse_empty_commit_hash():
    with pytest.raises(ValueError, match='Empty "commit-hash" field in checkout step.'):
        CheckoutStep.parse("n", "d", "id", {"commit-hash": ""})


def test_checkout_step_parse_empty_start_point():
    with pytest.raises(ValueError, match='Empty "start-point" field in checkout step.'):
        CheckoutStep.parse("n", "d", "id", {"start-point": "", "branch-name": "test"})


def test_checkout_step_parse_with_branch_name():
    step = CheckoutStep.parse("n", "d", "id", {"branch-name": "test"})
    assert isinstance(step, CheckoutStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.branch_name == "test"
    assert step.commit_hash is None
    assert step.start_point is None


def test_checkout_step_parse_with_commit_hash():
    step = CheckoutStep.parse("n", "d", "id", {"commit-hash": "abc123"})
    assert isinstance(step, CheckoutStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.branch_name is None
    assert step.commit_hash == "abc123"
    assert step.start_point is None


def test_checkout_step_parse_with_start_point():
    step = CheckoutStep.parse(
        "n", "d", "id", {"branch-name": "test", "start-point": "HEAD~1"}
    )
    assert isinstance(step, CheckoutStep)
    assert step.name == "n"
    assert step.description == "d"
    assert step.id == "id"
    assert step.branch_name == "test"
    assert step.commit_hash is None
    assert step.start_point == "HEAD~1"
