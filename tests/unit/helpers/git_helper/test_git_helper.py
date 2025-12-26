from subprocess import CompletedProcess
from unittest.mock import patch, MagicMock

import pytest
from repo_smith.command_result import CommandResult
from repo_smith.helpers.git_helper.git_helper import GitHelper
from repo_smith.helpers.helper import Helper


def test_tag_with_annotate():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(["git", "tag", "v0.1.0", "-a"], returncode=0)
        ),
    ) as mock_helper:
        gh = GitHelper(repo, False)
        gh.tag("v0.1.0", annotate=True)
        mock_helper.assert_called_with(["git", "tag", "v0.1.0", "-a"])


def test_tag_with_force():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(["git", "tag", "v0.1.0", "-f"], returncode=0)
        ),
    ) as mock_helper:
        gh = GitHelper(repo, False)
        gh.tag("v0.1.0", force=True)
        mock_helper.assert_called_with(["git", "tag", "v0.1.0", "-f"])


def test_tag_with_message():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(
                ["git", "tag", "v0.1.0", "-m", "This is a message."], returncode=0
            )
        ),
    ) as mock_helper:
        gh = GitHelper(repo, False)
        gh.tag("v0.1.0", message="This is a message.")
        mock_helper.assert_called_with(
            ["git", "tag", "v0.1.0", "-m", "This is a message."]
        )


def test_tag_with_multiple_flags():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(
                ["git", "tag", "v0.1.0", "-m", "This is a message.", "-f", "-a"],
                returncode=0,
            )
        ),
    ) as mock_helper:
        gh = GitHelper(repo, False)
        gh.tag("v0.1.0", message="This is a message.", force=True, annotate=True)
        mock_helper.assert_called_with(
            ["git", "tag", "v0.1.0", "-f", "-m", "This is a message.", "-a"]
        )


def test_add_all():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(["git", "add", "-A"], returncode=0),
        ),
    ) as mock_helper:
        gh = GitHelper(repo, False)
        gh.add(all=True)
        mock_helper.assert_called_with(["git", "add", "-A"])


def test_commit_all():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(
                ["git", "commit", "-a", "-m", "Test commit"],
                returncode=0,
            )
        ),
    ) as mock_helper:
        gh = GitHelper(repo, False)
        gh.commit(all=True, message="Test commit")
        mock_helper.assert_called_with(["git", "commit", "-a", "-m", "Test commit"])


def test_commit_with_pathspec():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(
                ["git", "commit", "-a", "-m", "Test commit", "file*"],
                returncode=0,
            )
        ),
    ) as mock_helper:
        gh = GitHelper(repo, False)
        gh.commit(pathspec="file*", all=True, message="Test commit")
        mock_helper.assert_called_with(
            ["git", "commit", "-a", "-m", "Test commit", "file*"]
        )


def test_checkout_with_branch_and_start_point():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(
                ["git", "checkout", "-b", "test", "HEAD"],
                returncode=0,
            )
        ),
    ) as mock_helper:
        gh = GitHelper(repo, False)
        gh.checkout(
            branch_name="test",
            start_point="HEAD",
            branch=True,
        )
        mock_helper.assert_called_with(["git", "checkout", "-b", "test", "HEAD"])


def test_checkout_with_files():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(
                ["git", "checkout", "test", "--", "filea.txt", "fileb.txt"],
                returncode=0,
            )
        ),
    ) as mock_helper:
        gh = GitHelper(repo, False)
        gh.checkout(
            branch_name="test",
            paths=["filea.txt", "fileb.txt"],
        )
        mock_helper.assert_called_with(
            ["git", "checkout", "test", "--", "filea.txt", "fileb.txt"]
        )


def test_restore_staged_worktree():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(
                ["git", "restore", "-S", "-W", "."],
                returncode=0,
            )
        ),
    ) as mock_helper:
        gh = GitHelper(repo, False)
        gh.restore(pathspec=".", staged=True, worktree=True)
        mock_helper.assert_called_with(["git", "restore", "-W", "-S", "."])


def test_restore_ours():
    repo = MagicMock()
    with (
        patch.object(
            Helper,
            "run",
            return_value=CommandResult(
                CompletedProcess(
                    ["git", "restore", "-S", "-W", "."],
                    returncode=0,
                )
            ),
        ),
        pytest.raises(ValueError),
    ):
        gh = GitHelper(repo, False)
        gh.restore(pathspec=".", ours=True, source=".", staged=True, worktree=True)
