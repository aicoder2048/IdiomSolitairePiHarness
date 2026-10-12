"""The red/green proof: a test the change adds or edits fails on the baseline and passes on HEAD.

A prompt that says "start with a failing test" is a request; this is the check.
Each changed test file's HEAD version is copied into a worktree of the baseline
commit and run there, then run again in the repo. For a bug the proof is binding:
no changed test, or one that already passes on the baseline, sends the builder
back. For every other kind it is recorded and never fails the run.

The runners here are `sh` scripts, so the suite needs neither bun nor pytest-in-pytest.

Run with `just test-adws` (the adws need pydantic; the project venv does not).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adw_modules import baseline, proof, quality  # noqa: E402
from adw_modules.data_types import ProofParams, ProofRunner  # noqa: E402

SH = [ProofRunner(pattern="t/*.sh", argv=["sh", "{file}"])]
# A test that fails until the fix exists: it is red on the baseline, green on the change.
REPRO = "test -f fixed.txt\n"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


@pytest.fixture
def repo(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    monkeypatch.chdir(root)
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "test")
    (root / "t").mkdir()
    (root / "t" / "old.sh").write_text("true\n")
    (root / "t" / "gone.sh").write_text("true\n")
    (root / "base.txt").write_text("v1")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    return root


@pytest.fixture
def run(repo, tmp_path):
    handoff = tmp_path / "handoff"
    handoff.mkdir()
    return SimpleNamespace(repo_root=repo, context_handoff_dir=handoff, phases=[SimpleNamespace(seq=3)])


def params(repo: Path, kind: str | None) -> ProofParams:
    return ProofParams(kind=kind, baseline=git(repo, "rev-parse", "HEAD").strip(), runners=SH)


def fix(repo: Path) -> None:
    (repo / "fixed.txt").write_text("the fix")


# --- the baseline worktree -------------------------------------------------------------------------


def test_baseline_tree_is_outside_the_repo_and_removed_afterwards(repo, run):
    sha = git(repo, "rev-parse", "HEAD").strip()
    (repo / "base.txt").write_text("v2, uncommitted")
    with baseline.checkout(run, sha) as tree:
        assert not tree.resolve().is_relative_to(repo.resolve())
        assert (tree / "base.txt").read_text() == "v1"  # the commit, not the working tree
    assert not tree.exists()
    assert len(git(repo, "worktree", "list").splitlines()) == 1


def test_baseline_tree_is_removed_when_the_body_raises(repo, run):
    sha = git(repo, "rev-parse", "HEAD").strip()
    with pytest.raises(RuntimeError), baseline.checkout(run, sha) as tree:
        raise RuntimeError("boom")
    assert not tree.exists()
    assert len(git(repo, "worktree", "list").splitlines()) == 1


def test_baseline_shares_node_modules_and_cleanup_never_touches_the_original(repo, run):
    (repo / "node_modules" / "pkg").mkdir(parents=True)
    (repo / "node_modules" / "pkg" / "index.js").write_text("x")
    sha = git(repo, "rev-parse", "HEAD").strip()
    with baseline.checkout(run, sha) as tree:
        assert (tree / "node_modules").is_symlink()
        assert (tree / "node_modules" / "pkg" / "index.js").read_text() == "x"
    assert (repo / "node_modules" / "pkg" / "index.js").read_text() == "x"


# --- which tests the change touched ----------------------------------------------------------------


def test_changed_tests_are_new_or_edited_files_a_runner_matches(repo):
    (repo / "t" / "old.sh").write_text(REPRO)  # edited, tracked
    (repo / "t" / "new.sh").write_text(REPRO)  # new, untracked
    (repo / "t" / "gone.sh").unlink()  # deleted: the integrity check's business, not the proof's
    (repo / "base.txt").write_text("v2")  # not a test
    assert proof.changed_tests(params(repo, None)) == ["t/new.sh", "t/old.sh"]


# --- the verdict -----------------------------------------------------------------------------------


def test_bug_with_a_test_red_on_baseline_and_green_on_head_passes(repo, run):
    (repo / "t" / "repro.sh").write_text(REPRO)
    fix(repo)
    result = proof.prove(run, params(repo, "bug"))
    assert result.required and result.passed
    [check] = result.checks
    assert (check.file, check.red, check.green) == ("t/repro.sh", True, True)
    assert Path(check.output_artifact).is_file()


def test_bug_whose_test_already_passes_on_baseline_fails_naming_the_file(repo, run):
    (repo / "t" / "repro.sh").write_text("echo always fine\n")
    result = proof.prove(run, params(repo, "bug"))
    assert not result.passed
    assert "t/repro.sh" in result.failures[0]
    assert "always fine" in result.failures[0]  # the baseline's own output, verbatim


def test_bug_without_any_changed_test_fails(repo, run):
    fix(repo)
    result = proof.prove(run, params(repo, "bug"))
    assert not result.passed and not result.checks
    assert "no test" in result.failures[0]


def test_bug_whose_test_is_red_on_head_fails(repo, run):
    (repo / "t" / "repro.sh").write_text(REPRO)  # and no fix
    result = proof.prove(run, params(repo, "bug"))
    assert not result.passed
    assert "HEAD" in result.failures[0]


def test_an_edited_test_runs_its_new_version_on_the_baseline(repo, run):
    (repo / "t" / "old.sh").write_text(REPRO)
    fix(repo)
    [check] = proof.prove(run, params(repo, "bug")).checks
    assert check.red  # the committed old.sh is `true`; the edited one is what ran


@pytest.mark.parametrize("kind", ["feature", "chore", "docs", None])
def test_other_kinds_record_the_proof_and_never_fail(repo, run, kind):
    (repo / "t" / "repro.sh").write_text("true\n")  # passes on the baseline too
    result = proof.prove(run, params(repo, kind))
    assert not result.required and result.passed and not result.failures
    assert result.checks[0].red is False


def test_other_kinds_without_tests_need_no_baseline(repo, run, monkeypatch):
    monkeypatch.setattr(baseline, "checkout", lambda *a: pytest.fail("no worktree when there is nothing to run"))
    result = proof.prove(run, params(repo, "feature"))
    assert result.passed and not result.checks


def test_file_placeholder_is_substituted_in_the_runner_argv(repo, run):
    (repo / "t" / "repro.sh").write_text(REPRO)
    fix(repo)
    [check] = proof.prove(run, params(repo, "bug")).checks
    assert check.command == "sh t/repro.sh"


def test_failing_proof_reaches_the_builder_as_an_envelope(repo, run):
    (repo / "t" / "repro.sh").write_text("true\n")
    envelope = proof.as_envelope(proof.prove(run, params(repo, "bug")))
    assert envelope.status == "fail" and not envelope.passed
    assert "t/repro.sh" in envelope.failures[0]
    assert envelope.artifacts


# --- the project's runners -------------------------------------------------------------------------


@pytest.mark.parametrize(
    "path, program",
    [
        ("tests/engine/game.test.ts", "bun"),
        ("tests/test_autoqueue.py", "uv"),
        ("adws/tests/test_proof.py", "uv"),
        ("adws/tests/dev_guard.test.ts", "node"),
    ],
)
def test_every_project_test_suite_has_a_proof_runner(path, program):
    runner = proof.runner_for(path, quality.PROOF_RUNNERS)
    assert runner is not None and runner.argv[0] == program


def test_helpers_are_not_tests():
    assert proof.runner_for("tests/extension/fake-pi.ts", quality.PROOF_RUNNERS) is None
    assert proof.runner_for("tests/fakes.ts", quality.PROOF_RUNNERS) is None
