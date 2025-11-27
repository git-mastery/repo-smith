from repo_smith.initialize_repo import initialize_repo


def test_remote_step_valid():
    ir = initialize_repo("tests/specs/remote_step/remote_step_valid.yml")
    with ir.initialize() as r:
        assert len(r.remotes) == 1
        assert r.remotes[0].name == "upstream"
        assert r.remotes[0].url == "https://github.com/git-mastery/repo-smith.git"
