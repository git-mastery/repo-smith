from dataclasses import dataclass


@dataclass
class CloneFrom:
    """Indicates that the first step of the initialization should be to clone the
    indicated repository and then apply commits to it.
    """

    repo_url: str
