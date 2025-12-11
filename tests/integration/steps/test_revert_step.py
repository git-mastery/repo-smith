from repo_smith.initialize_repo import initialize_repo


def test_revert_step_hash():
    ir = initialize_repo("tests/specs/revert_step/revert_step_hash.yml")
    with ir.initialize() as r:
        commits = list(r.iter_commits("master"))
        commit = commits[0]
        assert "Revert" in commit.message


def test_revert_step_relative():
    ir = initialize_repo("tests/specs/revert_step/revert_step_relative.yml")
    with ir.initialize() as r:
        commits = list(r.iter_commits("master"))
        commit = commits[0]
        assert "Revert" in commit.message
