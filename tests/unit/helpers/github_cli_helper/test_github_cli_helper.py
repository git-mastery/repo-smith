from subprocess import CompletedProcess
from unittest.mock import MagicMock, patch

from repo_smith.command_result import CommandResult
from repo_smith.helpers.github_cli_helper.github_cli_helper import GithubCliHelper
from repo_smith.helpers.helper import Helper


def test_fork_without_clone():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(
                [
                    "gh",
                    "repo",
                    "fork",
                    "git-mastery/app",
                    "--clone=false",
                    "--remote=true",
                ],
                returncode=0,
            )
        ),
    ) as mock_helper:
        gh = GithubCliHelper(repo, False)
        gh.repo_fork("git-mastery", "app", clone=False)
        mock_helper.assert_called_with(
            ["gh", "repo", "fork", "git-mastery/app", "--clone=false", "--remote=true"]
        )


def test_fork_with_clone():
    repo = MagicMock()
    with patch.object(
        Helper,
        "run",
        return_value=CommandResult(
            CompletedProcess(
                [
                    "gh",
                    "repo",
                    "fork",
                    "git-mastery/app",
                    "--clone=true",
                    "--remote=true",
                ],
                returncode=0,
            )
        ),
    ) as mock_helper:
        gh = GithubCliHelper(repo, False)
        gh.repo_fork("git-mastery", "app", clone=True)
        mock_helper.assert_called_with(
            ["gh", "repo", "fork", "git-mastery/app", "--clone=true", "--remote=true"]
        )
