# repo-smith

YAML-based configuration for Git repository initialization for unit testing

## Installation

```bash
pip install -U repo-smith
```

## Usage

Create a new configuration file (following the [specification](/specification.md)).

```yml
# File path: tests/specs/basic_spec.yml
name: Basic spec
description: Starting basic spec
initialization:
  steps:
    - name: Create filea.txt
      type: new-file
      filename: filea.txt
      contents: |
        Hello world
    - name: Add filea.txt
      type: add
      files:
        - filea.txt
    - name: Initial commit
      type: commit
      message: Initial commit
      id: initial-commit
    - name: v0 tag
      type: tag
      tag-name: v0
```

Create a unit test accordingly.

```py
from repo_smith.initialize_repo import initialize_repo
from git import Repo

def test_dummy():
  repo_initializer = initialize_repo("test/specs/basic_spec.yml")
  with repo_initializer.initialize() as repo:
    # All unit testing code for the dummy repository goes here
    print(repo)
```

For more use cases of `repo-smith`, refer to:

- [Official specification](/specification.md)
- [Unit tests](./tests/)
