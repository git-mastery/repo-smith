import os

from repo_smith.initialize_repo import initialize_repo


def test_reset_step():
    # only test hard reset (other valid modes can be assumed to work if hard works)
    repo_initializer = initialize_repo("tests/specs/reset_step/reset_step_hard.yml")
    with repo_initializer.initialize() as r:
        assert r.head.commit.message.strip() == "Initial commit"
        file_path = os.path.join(r.working_dir, "file1.txt")
        with open(file_path, "r") as f:
            content = f.read()
        assert "Initial content" in content
        assert "Modified content" not in content


def test_reset_step_files():
    repo_initializer = initialize_repo("tests/specs/reset_step/reset_step_files.yml")
    with repo_initializer.initialize() as r:
        staged_files = [d.a_path for d in r.index.diff("HEAD")]
        assert "file1.txt" not in staged_files
        assert "file2.txt" in staged_files
