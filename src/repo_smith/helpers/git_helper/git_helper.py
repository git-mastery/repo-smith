from typing import List, Optional, Union, Unpack

from repo_smith.helpers.git_helper.add_options import ADD_SPEC, AddOptions
from repo_smith.helpers.git_helper.checkout_options import (
    CHECKOUT_SPEC,
    CheckoutOptions,
)
from repo_smith.helpers.git_helper.commit_options import COMMIT_SPEC, CommitOptions
from repo_smith.helpers.git_helper.remote_options import (
    REMOTE_ADD_SPEC,
    RemoteAddOptions,
)
from repo_smith.helpers.git_helper.tag_options import TAG_SPEC, TagOptions
from repo_smith.helpers.helper import Helper


class GitHelper(Helper):
    def __init__(self, verbose: bool) -> None:
        super().__init__(verbose)

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
        elif isinstance(files, "str"):
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
