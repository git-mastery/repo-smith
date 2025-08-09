from src.repo_smith.initialize_repo import initialize_repo


def test_clone_from():
    repo_initializer = initialize_repo("tests/specs/clone_from.yml")
    with repo_initializer.initialize() as r:
        commits = list(r.iter_commits("main"))
        # Should be more than 1 (the empty commit we made)
        assert len(commits) > 1
