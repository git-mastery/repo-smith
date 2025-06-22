# `repo-smith`

## Inspiration

`repo-smith` is a unit testing library built on top of `GitPython` and
inspired by the
[`GitPython` unit testing](https://github.com/gitpython-developers/GitPython/blob/main/test/test_diff.py)
where unit tests for Git repositories are performed by directly creating
temporary directories and initializing them as Git repositories.

The process of writing the necessary code to create the Git repository (before
any unit testing can even be conducted) is too tedious and given that we want
to similarly unit test solution files for Git Mastery, we want a much better
overall developer experience in initializing and creating test Git repositories.

`repo-smith` declares a lightweight YAML-based configuration language,
allowing developers to declare Git repositories to be created using an
intuitive syntax (detailed below) and will serve as the basis for initializing
larger and more complex repositories. Using `repo-smith`, you can streamline
your Git repository unit testing, focusing on validating the behavior of your
solutions.

## Syntax

### `name`

Name of the Git repository unit test. Optional.

Type: `string`

### `description`

Description of the Git repository unit test. Optional.

Type: `string`

### `initialization`

Includes the instructions and components to initialize the repository.

> [!NOTE]  
> All steps are run sequentially, so ensure that you are declaring the
> repository from top to bottom

#### `initialization.steps[*].name`

Name of the initialization step. Optional.

Type: `string`

#### `initialization.steps[*].description`

Description of the initialization step. Optional.

Type: `string`

#### `initialization.steps[*].id`

Provides a unique `id` for the current step. Optional, but if provided, will be
validated to ensure uniqueness across `initialization.steps[*]`.

When a step is provided with an `id`, hooks will be automatically installed and
events for the hook will be pushed. More information about the
[lifecycle hooks here.](#lifecycle-hooks)

Type: `string`

Constraints:

- Only alphanumeric characters, `-`, and `_`
- No spaces allowed

#### `initialization.steps[*].type`

Type of action of the step. Not optional.

Accepted values include:

- `commit`
- `add`
- `tag`
- `new-file`
- `edit-file`
- `delete-file`
- `append-file`
- `bash`
- `branch`
- `checkout`
- `remote`

More action types will be supported in the future:

- `revert`
- `reset`

#### `initialization.steps[*].empty`

Indicates if the commit should be empty. Only read if
`initialization.steps[*].type` is `commit`

Type: `bool`

#### `initialization.steps[*].message`

Commit message to be used. Only read if `initialization.steps[*].type` is `commit`.

Type: `string`

#### `initialization.steps[*].files`

File names to be added to the Git repository. Only read if
`initialization.steps[*].type` is `add`.

Type: `list`

#### `initialization.steps[*].tag-name`

Tag name to be used on the current commit. Only read if
`initialization.steps[*].type` is `tag`.

The tag name cannot be duplicated, otherwise, the framework will throw an
exception during initialization.

Type: `string`

#### `initialization.steps[*].tag-message`

Tag message to be used on the current commit. Only read if
`initialization.steps[*].type` is `tag`. Optional.

Type: `string`

#### `initialization.steps[*].filename`

Target file name. Only read if
`initialization.steps[*].type` is `new-file`, `edit-file`, `delete-file` or
`append-file`.

Specify any new folders in the `filename` and `repo-smith` will initialize them
accordingly.

Type: `string`

#### `initialization.steps[*].contents`

File content for file `initialization.steps[*].filename`. Only read if
`initialization.steps[*].type` is `new-file`, `edit-file`, `delete-file` or
`append-file`.

Type: `string`

#### `initialization.steps[*].runs`

Bash commands to execute. Only read if `initialization.steps[*].type` is `bash`.

Type: `string`

#### `initialization.steps[*].branch-name`

Branch name. Only read if `initialization.steps[*].type` is `branch` or
`checkout`.

Users are expected to manage their own branches themselves.

Type: `string`

#### `initialization.steps[*].commit-hash`

Commit hash. Only read if `initialization.steps[*].type` is `checkout`.

Type: `string`

#### `initialization.steps[*].remote-name`

Remote name. Only read if `initialization.steps[*].type` is `remote`.

Type: `string`

#### `initialization.steps[*].remote-url`

Remote URL. Only read if `initialization.steps[*].type` is `remote`.

Type: `string`

## Lifecycle hooks

When a step `initializations.steps[*].id` is declared, the step can be
identified with a unique step `id` (discussed [here](#initializationstepsid))
and lifecycle hooks will be automatically installed for the step.

Lifecycle hooks are useful when the unit test wants to provide some guarantees
about the Git repository as it is being built (for instance, ensuring that a
commit is present).

There are two primary lifecycle hooks that the unit test can have access to
during the initialization process:

1. Pre-hook: run right before the step is run
2. Post-hook: run right after the step has completed

Take the following file:

```yaml
# File: hooks.yml
name: Testing hooks
description: |
  Lifecycle hooks on each step give visibility into the initialization process
initialization:
  steps:
    - name: First commit
      type: commit
      message: First commit
      empty: true
      id: first-commit
    - name: Creating a new file
      type: new-file
      filename: test.txt
      contents: |
        Hello world!
    - name: Adding test.txt
      type: add
      files:
        - test.txt
      id: add-test-txt
    - name: Second commit
      type: commit
      message: Add test.txt
```

The overall lifecycle of the above initialization would be:

1. Propagate `first-commit::pre-hook` event
2. Execute "First commit"
3. Propagate `first-commit::post-hook` event
4. Execute "Creating a new file"
5. Propagate `add-test-text::pre-hook` event
6. Execute "Adding test.txt"
7. Propagate `add-test-text::post-hook` event
8. Execute "Second commit"

In the unit test, the hooks can be declared as such:

```python
from repo_smith import initialize_repo

def test_hook() -> None:
  def first_commit_pre_hook(r: Repo) -> None:
    print(r)

  spec_path = "hooks.yml"
  repo_initializer = initialize_repo(spec_path)
  repo_initializer.add_pre_hook("first-commit", first_commit_pre_hook)
  with repo_initializer.initialize() as repo:
    print(repo.repo)
```

## FAQ

### What if I want to attach a tag based on metadata of the commit history?

As `repo-smith` is designed to be as generic as possible, it does not have
strong ties with how `git-autograder` works even though both are designed to
work for Git Mastery.

To do so, you can use a `post-hook` on the commit that should receive the tag:

```yml
# dynamic-tag.yml
name: Dynamic tag hook
description: Dynamically attaching a tag based on commit history data
initialization:
  steps:
    - name: Create file
      type: new-file
      filename: filea.txt
      contents: |
        Hello world!
    - name: Add filea.txt
      type: add
      files:
        - filea.txt
    - name: Initial commit
      type: commit
      message: Committing file
      id: initial-commit
```

```py
from repo_smith import initialize_repo

def test_hook() -> None:
  def tag_commit_pre_hook(r: Repo) -> None:
    first_commit = list(r.iter_commits("main", max_count=1))[0]
    hexsha = first_commit.hexsha[:7]
    r.create_tag(f"git-mastery-{hexsha}")

  spec_path = "dynamic-tag.yml"
  repo_initializer = initialize_repo(spec_path)
  repo_initializer.add_post_hook("initial-commit", first_commit_pre_hook)
  with repo_initializer.initialize() as repo:
    print(repo.repo)
```

In this design, we are able to very quickly attach tags to various commits
without much workarounds.
