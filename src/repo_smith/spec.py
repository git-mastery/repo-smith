from dataclasses import dataclass
from typing import List, Optional

from repo_smith.steps.step import Step


@dataclass
class Spec:
    name: str
    description: Optional[str]
    steps: List[Step]
