from typing import List, Optional, Union, Unpack

from git import Repo
from repo_smith.helpers.git_helper.add_options import ADD_SPEC, AddOptions
from repo_smith.helpers.git_helper.branch_options import BRANCH_SPEC, BranchOptions
from repo_smith.helpers.git_helper.checkout_options import (
    CHECKOUT_SPEC,
    CheckoutOptions,
)
from repo_smith.helpers.git_helper.commit_options import COMMIT_SPEC, CommitOptions
from repo_smith.helpers.git_helper.fetch_options import FETCH_SPEC, FetchOptions
from repo_smith.helpers.git_helper.init_options import INIT_SPEC, InitOptions
from repo_smith.helpers.git_helper.merge_options import MERGE_SPEC, MergeOptions
from repo_smith.helpers.git_helper.remote_options import (
    REMOTE_ADD_SPEC,
    RemoteAddOptions,
)
from repo_smith.helpers.git_helper.reset_options import RESET_SPEC, ResetOptions
from repo_smith.helpers.git_helper.restore_options import RESTORE_SPEC, RestoreOptions
from repo_smith.helpers.git_helper.revert_options import REVERT_SPEC, RevertOptions
from repo_smith.helpers.git_helper.tag_options import TAG_SPEC, TagOptions
from repo_smith.helpers.helper import Helper


class GitHelper(Helper):
    def __init__(self, repo: Optional[Repo], verbose: bool) -> None:
        super().__init__(repo, verbose)

    def tag(
        self,
        tag_name: str,
        object_id: Optional[str] = None,
        **options: Unpack[TagOptions],
    ) -> None:
        """Calls the underlying git-tag command with the given support options.

        More information about the git-tag command can be found `here <https://git-scm.com/docs/git-tag>`__.
        """
        args = ["git", "tag", tag_name]
        if object_id is not None:
            args.append(object_id)
        args.extend(TAG_SPEC.build(options))
        self.run(args)

    def add(
        self,
        files: Optional[Union[str, List[str]]] = None,
        **options: Unpack[AddOptions],
    ) -> None:
        """Calls the underlying git-add command with the given support options.

        More information about the git-add command can be found `here <https://git-scm.com/docs/git-add>`__.
        """
        if files is None:
            files = []
        elif isinstance(files, str):
            files = [files]
        args = ["git", "add", *files] + ADD_SPEC.build(options)
        self.run(args)

    # TODO: Create a class just for the pathspec format
    def commit(
        self,
        pathspec: Optional[str] = None,
        **options: Unpack[CommitOptions],
    ) -> None:
        """Calls the underlying git-commit command with the given support options.

        More information about the git-commit command can be found `here <https://git-scm.com/docs/git-commit>`__.
        """
        trailing = [] if pathspec is None else [pathspec]
        args = ["git", "commit"] + COMMIT_SPEC.build(options) + trailing
        self.run(args)

    def remote_add(
        self,
        name: str,
        url: str,
        **options: Unpack[RemoteAddOptions],
    ) -> None:
        """Calls the underlying git-remote add command with the given support options.

        More information about the git-remote add command can be found `here <https://git-scm.com/docs/git-remote>`__.
        """
        args = ["git", "remote", "add"] + REMOTE_ADD_SPEC.build(options) + [name, url]
        self.run(args)

    def remote_rename(self, old: str, new: str) -> None:
        """Calls the underlying git-remote rename command with the given support options.

        More information about the git-remote rename command can be found `here <https://git-scm.com/docs/git-remote>`__.
        """
        args = ["git", "remote", "rename", old, new]
        self.run(args)

    def remote_remove(self, name: str) -> None:
        """Calls the underlying git-remote remove command with the given support options.

        More information about the git-remote remove command can be found `here <https://git-scm.com/docs/git-remote>`__.
        """
        args = ["git", "remote", "remove", name]
        self.run(args)

    def checkout(
        self,
        branch_name: Optional[str] = None,
        start_point: Optional[str] = None,
        paths: Optional[Union[str, List[str]]] = None,
        **options: Unpack[CheckoutOptions],
    ) -> None:
        """Calls the underlying git-checkout command with the given support options.

        More information about the git-checkout command can be found `here <https://git-scm.com/docs/git-checkout>`__.
        """
        # git-checkout prioritizes the branch first, so if the branch is provided, we use it first
        if paths is not None and len(paths) > 0:
            if options.get("branch", False):
                # The alternative is to just ignore this field if set
                raise ValueError("Cannot use '-b' when specifying paths.")

        args = ["git", "checkout"] + CHECKOUT_SPEC.build(options)
        if branch_name is not None:
            args.append(branch_name)

        if start_point is not None:
            # So we assume checking out by branch, otherwise we look for files
            args.append(start_point)
        elif paths is not None:
            args.append("--")
            paths = [paths] if isinstance(paths, str) else paths
            args.extend(paths)

        self.run(args)

    def restore(
        self,
        pathspec: Optional[Union[str, List[str]]] = None,
        **options: Unpack[RestoreOptions],
    ) -> None:
        """Calls the underlying git-restore command with the given support options.

        More information about the git-restore command can be found `here <https://git-scm.com/docs/git-restore>`__.
        """
        if (
            options.get("ours", False)
            or options.get("theirs", False)
            or options.get("merge", False)
            or options.get("conflict") is not None
        ) and options.get("source") is not None:
            raise ValueError(
                "Cannot use --ours, --theirs, --merge, or --conflict with --source."
            )

        if (
            options.get("ours", False)
            or options.get("theirs", False)
            or options.get("merge", False)
            or options.get("conflict") is not None
        ) and options.get("ignore_unmerged") is not None:
            raise ValueError(
                "Cannot use --ours, --theirs, --merge, or --conflict with --ignore-unmerged."
            )

        if pathspec is None:
            pathspec = []
        elif isinstance(pathspec, str):
            pathspec = [pathspec]
        args = ["git", "restore"] + RESTORE_SPEC.build(options) + pathspec
        self.run(args)

    def merge(
        self,
        commits: Union[str, List[str]],
        **options: Unpack[MergeOptions],
    ) -> None:
        """Calls the underlying git-merge command with the given support options.

        More information about the git-merge command can be found `here <https://git-scm.com/docs/git-merge>`__.
        """
        if isinstance(commits, str):
            commits = [commits]
        args = ["git", "merge"] + MERGE_SPEC.build(options) + commits
        self.run(args)

    def fetch(
        self,
        repository: Optional[str] = None,
        **options: Unpack[FetchOptions],
    ) -> None:
        """Calls the underlying git-fetch command with the given support options.

        More information about the git-fetch command can be found `here <https://git-scm.com/docs/git-fetch>`__.
        """
        if repository is None and not options.get("all"):
            raise ValueError(
                "Specify the repository as a URL or remote if --all not used."
            )
        trailing = [repository] if repository is not None else []
        args = ["git", "fetch"] + FETCH_SPEC.build(options) + trailing
        self.run(args)

    def branch(
        self,
        branch_name: str,
        start_point: Optional[str] = None,
        old_branch: Optional[str] = None,
        **options: Unpack[BranchOptions],
    ) -> None:
        """Calls the underlying git-branch command with the given support options.

        More information about the git-branch command can be found `here <https://git-scm.com/docs/git-branch>`__.
        """
        if options.get("move", False) or options.get("copy", False):
            if old_branch is None:
                raise ValueError(
                    "You must specify the old_branch when using --move or --copy."
                )
            args = [
                "git",
                "branch",
                "--move" if options.get("move", False) else "--copy",
                old_branch,
                branch_name,
            ]
        elif options.get("delete", False):
            args = ["git", "branch", "--delete", branch_name]
        else:
            args = (
                ["git", "branch"]
                + BRANCH_SPEC.build(options)
                + [branch_name]
                + ([] if start_point is None else [start_point])
            )
        self.run(args)

    def revert(
        self,
        commits: Union[str, List[str]],
        **options: Unpack[RevertOptions],
    ) -> None:
        """Calls the underlying git-revert command with the given support options.

        More information about the git-revert command can be found `here <https://git-scm.com/docs/git-revert>`__.
        """
        if isinstance(commits, str):
            commits = [commits]
        # Hardcode --no-edit since we never allow interaction
        args = ["git", "revert", "--no-edit"] + REVERT_SPEC.build(options) + commits
        self.run(args)

    def reset(
        self,
        commits: Optional[Union[str, List[str]]] = None,
        pathspec: Optional[Union[str, List[str]]] = None,
        **options: Unpack[ResetOptions],
    ) -> None:
        """Calls the underlying git-reset command with the given support options.

        More information about the git-reset command can be found `here <https://git-scm.com/docs/git-reset>`__.
        """
        if isinstance(commits, str):
            commits = [commits]
        elif commits is None:
            commits = []

        args = ["git", "reset"] + RESET_SPEC.build(options)

        args.extend(commits)

        if pathspec is not None:
            args.append("--")
            if isinstance(pathspec, str):
                pathspec = [pathspec]
            args.extend(pathspec)

        self.run(args)

    def init(
        self,
        directory: Optional[str] = None,
        **options: Unpack[InitOptions],
    ) -> None:
        """Calls the underlying git-init command with the given support options.

        More information about the git-init command can be found `here <https://git-scm.com/docs/git-init>`__.
        """
        trailing = [] if directory is None else [directory]
        args = ["git", "init"] + INIT_SPEC.build(options) + trailing
        self.run(args)
