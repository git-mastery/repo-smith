from enum import Enum


class StepType(Enum):
    COMMIT = "commit"
    ADD = "add"
    TAG = "tag"
    NEW_FILE = "new-file"
    EDIT_FILE = "edit-file"
    DELETE_FILE = "delete-file"
    APPEND_FILE = "append-file"
    BASH = "bash"
    BRANCH = "branch"
    BRANCH_RENAME = "branch-rename"
    BRANCH_DELETE = "branch-delete"
    CHECKOUT = "checkout"
    REMOTE = "remote"
    RESET = "reset"
    REVERT = "revert"
    MERGE = "merge"
    FETCH = "fetch"

    @staticmethod
    def from_value(value: str) -> "StepType":
        match value:
            case "commit":
                return StepType.COMMIT
            case "add":
                return StepType.ADD
            case "tag":
                return StepType.TAG
            case "new-file":
                return StepType.NEW_FILE
            case "edit-file":
                return StepType.EDIT_FILE
            case "delete-file":
                return StepType.DELETE_FILE
            case "append-file":
                return StepType.APPEND_FILE
            case "bash":
                return StepType.BASH
            case "branch":
                return StepType.BRANCH
            case "branch-rename":
                return StepType.BRANCH_RENAME
            case "branch-delete":
                return StepType.BRANCH_DELETE
            case "checkout":
                return StepType.CHECKOUT
            case "remote":
                return StepType.REMOTE
            case "reset":
                return StepType.RESET
            case "revert":
                return StepType.REVERT
            case "merge":
                return StepType.MERGE
            case "fetch":
                return StepType.FETCH
            case _:
                raise ValueError(f"Invalid value {value} given. Not supported.")
