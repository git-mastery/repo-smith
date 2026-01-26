# Agents for repo-smith

This document defines the autonomous **agent roles** used when working on this repository. Each agent has a clear purpose, scope, and set of files or symbols it is allowed to interact with.

Agents are designed to be **minimal, scriptable, and composable**, so they can be safely used by humans or automated tooling.

---

## 1. CI / Test Runner Agent

**Purpose**
Run and report unit and integration tests.

**Responsibilities**

* Install dependencies
* Execute pytest suites
* Surface failures with minimal noise

**Does NOT**

* Modify source code
* Update specs or documentation

**Typical commands**

* `pip install -r requirements.txt`
* `pytest -q`

**Key files**

* Tests: [`tests/`](tests/)
* Integration entry points: [`tests/integration/steps/test_revert_step.py`](tests/integration/steps/test_revert_step.py)
* Config: [`pyproject.toml`](pyproject.toml), [`requirements.txt`](requirements.txt)

---

## 2. Spec Linter Agent

**Purpose**
Validate YAML spec files against repository expectations.

**Responsibilities**

* Validate required fields and accepted values
* Check `initialization.*` fields
* Fail fast on invalid or ambiguous specs

**Source of truth**

* [`specification.md`](specification.md)
* Spec model: [`Spec`](src/repo_smith/spec.py)

**Does NOT**

* Execute steps
* Initialize repositories

**Key references**

* Specification: [`specification.md`](specification.md)
* Parser / entry point: [`initialize_repo`](src/repo_smith/initialize_repo.py)

---

## 3. Repo Initializer / Orchestrator Agent

**Purpose**
Create repositories from spec files and orchestrate step execution.

**Responsibilities**

* Initialize or clone repositories
* Parse specs into models
* Execute steps in declared order
* Manage lifecycle hooks

**Does NOT**

* Implement step-specific logic
* Validate spec schema beyond basic parsing

**Inputs**

* YAML specs (e.g. `tests/specs/`)

**Outputs**

* Initialized git repository on disk
* Exceptions on invalid execution

**Key symbols/files**

* [`initialize_repo`](src/repo_smith/initialize_repo.py)
* [`RepoInitializer`](src/repo_smith/initialize_repo.py)
* Spec model: [`Spec`](src/repo_smith/spec.py)
* Dispatcher: [`Dispatcher`](src/repo_smith/steps/dispatcher.py)

---

## 4. Steps Agent (Execution & Authoring)

**Purpose**
Author, validate, and execute individual step implementations.

**Responsibilities**

* Implement new step types
* Parse step arguments
* Enforce step-level invariants

**Does NOT**

* Control execution order
* Perform repository-wide orchestration

**Key symbols/files**

* Base class: [`Step`](src/repo_smith/steps/step.py)
* Dispatcher: [`Dispatcher`](src/repo_smith/steps/dispatcher.py)
* Example steps:

  * [`commit_step.py`](src/repo_smith/steps/commit_step.py)
  * [`revert_step.py`](src/repo_smith/steps/revert_step.py)
  * [`file_step.py`](src/repo_smith/steps/file_step.py)

---

## 5. Git Helper Agent

**Purpose**
Wrap and validate git / gh command invocations.

**Responsibilities**

* Define command option schemas
* Construct safe, explicit git commands
* Generate tests for command options

**Does NOT**

* Execute high-level steps
* Modify specs directly

**Key files/symbols**

* Git helper: [`GitHelper`](src/repo_smith/helpers/git_helper/git_helper.py)
* Command spec: [`CommandSpec`](src/repo_smith/helpers/command_spec.py)
* Option definitions:

  * [`tag_options.py`](src/repo_smith/helpers/git_helper/tag_options.py)
  * [`commit_options.py`](src/repo_smith/helpers/git_helper/commit_options.py)

---

## 6. Files Helper Agent

**Purpose**
Create and modify filesystem artifacts used by specs and tests.

**Responsibilities**

* Create files and directories
* Modify file contents deterministically

**Does NOT**

* Invoke git commands
* Execute steps

**Key file**

* [`FilesHelper`](src/repo_smith/helpers/files_helper.py)

---

## 7. Docs & Release Agent

**Purpose**
Maintain documentation and assist with releases.

**Responsibilities**

* Update README and specification
* Maintain changelog
* Assist with GitHub Actions-based releases

**Does NOT**

* Modify core execution logic
* Change spec semantics

**Key files**

* [`README.md`](README.md)
* [`specification.md`](specification.md)
* GitHub Actions:

  * [`.github/workflows/publish.yml`](.github/workflows/publish.yml)
  * [`.github/workflows/bump-version.yml`](.github/workflows/bump-version.yml)

---

## Usage Notes

* Agents should be callable from the **repository root**.
* Agents should fail fast and prefer explicit errors.
* Agents must not infer undocumented behavior.

**Common workflows**

* Run tests: `pytest -q`
* Lint specs: validate YAML files in `tests/specs/` against [`specification.md`](specification.md)
* Initialize repo in tests: call [`initialize_repo`](src/repo_smith/initialize_repo.py)

---

## Quick Navigation

* Core orchestrator: [`initialize_repo`](src/repo_smith/initialize_repo.py)
* Main entry point: [`RepoSmith`](src/repo_smith/repo_smith.py)
* Steps & dispatcher: [`src/repo_smith/steps/`](src/repo_smith/steps/)

---

## Non-goals

Agents should **not**:

* Rewrite git history of this repository
* Push tags or releases without CI confirmation
* Invent spec behavior not documented or tested
