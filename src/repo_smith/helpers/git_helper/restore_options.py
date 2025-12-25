from typing import Literal, TypedDict, Union

from repo_smith.helpers.command_spec import CommandSpec


class RestoreOptions(TypedDict, total=False):
    source: str

    worktree: bool
    staged: bool

    ours: bool
    theirs: bool

    merge: bool
    conflict: Union[Literal["merge"], Literal["diff3"], Literal["zdiff3"]]

    ignore_unmerged: bool
    ignore_skip_worktree_bits: bool

    recurse_submodules: bool
    no_recurse_submodules: bool

    overlay: bool
    no_overlay: bool


RESTORE_SPEC = (
    CommandSpec()
    .opt("source", "--source")
    .flag("worktree", "-W", default=False)
    .flag("staged", "-S", default=False)
    .flag("ours", "--ours", default=False)
    .flag("theirs", "--theirs", default=False)
    .flag("merge", "--merge", default=False)
    .opt("conflict", "--conflict")
    .flag("ignore_unmerged", "--ignore-unmerged", default=False)
    .flag("ignore_skip_worktree_bits", "--ignore-skip-worktree-bits", default=False)
    .flag("recurse_submodules", "--recurse-submodules", default=False)
    .flag("no_recurse_submodules", "--no-recurse-submodules", default=False)
    .flag("overlay", "--overlay", default=False)
    .flag("no_overlay", "--no-overlay", default=False)
)
