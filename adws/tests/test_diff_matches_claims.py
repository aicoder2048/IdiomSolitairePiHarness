"""Regression tests for the diff_matches_claims gate (upstream issue #6).

The gate reconciles the envelope's `changed_files` against what the agent call
actually changed — measured from the snapshot `agents.execute` takes before the
agent runs — in both directions. Earlier phases' work and the engineer's own
uncommitted edits sit in that baseline, so they are never charged to the agent.

Run with `just test-adws` (the adws need pydantic; the project venv does not).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adw_modules import gates, permissions  # noqa: E402
from adw_modules.data_types import BuildOutput  # noqa: E402


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    git(tmp_path, "init", "-q")
    git(tmp_path, "config", "user.email", "test@example.com")
    git(tmp_path, "config", "user.name", "test")
    (tmp_path / "base.txt").write_text("v1")
    git(tmp_path, "add", "-A")
    git(tmp_path, "commit", "-qm", "base")
    return tmp_path


def start_call(repo: Path) -> SimpleNamespace:
    """A run whose agent call is about to begin: the baseline is taken now."""
    run = SimpleNamespace(repo_root=repo)
    run.tree_before = permissions.snapshot(run)
    return run


def gate(run, changed_files: list[str]):
    return gates.diff_matches_claims(BuildOutput(status="success", changed_files=changed_files), run)


def test_exact_match_passes(repo):
    run = start_call(repo)
    (repo / "base.txt").write_text("v2")
    (repo / "new.txt").write_text("new")
    assert gate(run, ["base.txt", "new.txt"]).passed


def test_unclaimed_change_fails(repo):
    run = start_call(repo)
    (repo / "base.txt").write_text("v2")
    (repo / "sneaky.txt").write_text("new")
    report = gate(run, ["base.txt"])
    assert any("sneaky.txt" in v for v in report.violations)


def test_claimed_but_unchanged_fails(repo):
    run = start_call(repo)
    report = gate(run, ["base.txt"])
    assert any("base.txt" in v for v in report.violations)


def test_files_in_a_new_directory_are_listed_individually(repo):
    run = start_call(repo)
    (repo / "pkg").mkdir()
    (repo / "pkg" / "a.py").write_text("x = 1")
    assert gate(run, ["pkg/a.py"]).passed


def test_dirty_tree_before_the_call_is_not_charged(repo):
    """A plan written by an earlier phase, or the engineer's WIP, is baseline."""
    (repo / "plan.md").write_text("the plan")
    (repo / "base.txt").write_text("engineer wip")
    run = start_call(repo)
    (repo / "impl.py").write_text("done")
    assert gate(run, ["impl.py"]).passed


def test_further_edit_to_an_already_dirty_file_counts(repo):
    (repo / "base.txt").write_text("v1\nwip")
    run = start_call(repo)
    (repo / "base.txt").write_text("v1\nwip\nmore\nlines")
    assert gate(run, ["base.txt"]).passed


def test_gitignored_files_are_not_unclaimed(repo):
    (repo / ".gitignore").write_text("*.log\n")
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", "ignore logs")
    run = start_call(repo)
    (repo / "base.txt").write_text("v2")
    (repo / "noise.log").write_text("x")
    assert gate(run, ["base.txt"]).passed


def test_dot_slash_and_absolute_claims_are_normalised(repo):
    run = start_call(repo)
    (repo / ".env.sample").write_text("KEY=")
    (repo / "base.txt").write_text("v2")
    assert gate(run, ["./.env.sample", str(repo / "base.txt")]).passed


def test_no_baseline_falls_back_to_existence(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "x.txt").write_text("hi")
    run = SimpleNamespace(repo_root=tmp_path, tree_before=None)
    assert gate(run, ["x.txt"]).passed
    assert not gate(run, ["missing.txt"]).passed
