from repo_smith.initialize_repo import initialize_repo

# TODO: more corner case testing


def test_merge_step_squash():
    ir = initialize_repo("tests/specs/merge_step/merge_step_squash.yml")
    with ir.initialize() as r:
        commits = list(r.iter_commits())
        commit_messages = [c.message.strip() for c in commits][::-1]
        assert commit_messages == ["Before", "Squash merge branch 'incoming'", "After"]


def test_merge_step_no_fast_forward():
    ir = initialize_repo("tests/specs/merge_step/merge_step_no_fast_forward.yml")
    with ir.initialize() as r:
        commits = list(r.iter_commits())
        commit_messages = [c.message.strip() for c in commits][::-1]
        assert "Merge branch 'incoming'" in commit_messages
        assert len(commits[1].parents) == 2


def test_merge_step_with_fast_forward():
    ir = initialize_repo("tests/specs/merge_step/merge_step_with_fast_forward.yml")
    with ir.initialize() as r:
        commits = list(r.iter_commits())
        commit_messages = [c.message.strip() for c in commits][::-1]
        assert "Merge branch 'incoming'" not in commit_messages
        assert not any([len(c.parents) > 1 for c in commits])
