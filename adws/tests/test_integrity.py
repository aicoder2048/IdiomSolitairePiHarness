"""The test-integrity check: a change may not weaken the tests it is judged by, unless it says so.

A builder that cannot make a test pass can make it stop asking: skip it, focus
another one with `.only`, delete the file, drop an assertion. The suite then
goes green and nothing in the run notices. This check compares the change with
the baseline commit — markers in added lines of test files, deleted test files,
and the suite's own test and expect() counts — and sends any weakening the
builder did not declare in `weakened_tests` back to it. A declared one passes,
and is carried forward so the PR can show it first.

The counter here is `sh` printing bun's summary lines, so the suite needs no bun.

This file is itself a test file full of marker strings, so a change that ADDS
more of them here is flagged like any other; declare it in `weakened_tests`
("fixtures for the marker detector") — the check is meant to be that blunt.

Run with `just test-adws` (the adws need pydantic; the project venv does not).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adw_modules import baseline, integrity, quality  # noqa: E402
from adw_modules.data_types import BuildOutput, IntegrityParams, SuiteCounter, WeakenedTest  # noqa: E402

PROMPTS = Path(__file__).resolve().parents[1] / "adw_data" / "prompt_engineering"

# Prints bun's two summary lines: one test per `it ` line, one expect() per `expect` line.
COUNTER = SuiteCounter(
    argv=[
        "sh",
        "-c",
        'echo " $(cat t/*.sh | grep -c expect) expect() calls"; '
        "echo \"Ran $(cat t/*.sh | grep -c '^it ') tests across 2 files.\"",
    ],
    covers=["t/*.sh"],
)
OLD = "it a\nexpect 1\nexpect 2\n"


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
    (root / "t" / "old.sh").write_text(OLD)
    (root / "t" / "gone.sh").write_text("it b\nexpect 3\n")
    (root / "py").mkdir()
    (root / "py" / "test_x.py").write_text("def test_x():\n    assert True\n")
    (root / "src.txt").write_text("v1\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    return root


@pytest.fixture
def run(repo, tmp_path):
    handoff = tmp_path / "handoff"
    handoff.mkdir()
    return SimpleNamespace(repo_root=repo, context_handoff_dir=handoff, phases=[SimpleNamespace(seq=4)])


def check(run, declared: list[WeakenedTest] | None = None):
    params = IntegrityParams(
        baseline=git(run.repo_root, "rev-parse", "HEAD").strip(),
        tests=["t/*.sh", "py/test_*.py"],
        counter=COUNTER,
        declared=declared or [],
    )
    return integrity.check(run, params)


def append(repo: Path, path: str, line: str) -> None:
    with (repo / path).open("a") as f:
        f.write(line + "\n")


# --- markers in added lines ------------------------------------------------------------------------


@pytest.mark.parametrize(
    "line",
    [
        'test.skip("plays a round", () => {})',
        'it.only("plays a round", () => {})',
        'test.todo("plays a round")',
        'test.if(false)("plays a round", () => {})',
        "@pytest.mark.skip(reason='flaky')",
        "@pytest.mark.xfail",
        "    pytest.skip('later')",
    ],
)
def test_a_skip_marker_added_to_a_test_fails(repo, run, line):
    append(repo, "t/old.sh", line)
    result = check(run)
    assert not result.passed
    assert [f.file for f in result.findings] == ["t/old.sh"]
    assert line.strip() in result.failures[0]


def test_a_marker_in_a_new_untracked_test_file_fails(repo, run):
    (repo / "t" / "new.sh").write_text('it c\nexpect 4\ntest.skip("x", () => {})\n')
    assert [f.file for f in check(run).findings] == ["t/new.sh"]


def test_removing_a_marker_is_not_a_weakening(repo, run):
    (repo / "t" / "old.sh").write_text(OLD + 'test.skip("x")\n')
    git(repo, "commit", "-qam", "skipped")
    (repo / "t" / "old.sh").write_text(OLD)
    assert check(run).passed


def test_a_marker_outside_a_test_file_is_not_checked(repo, run):
    append(repo, "src.txt", 'const skip = list.skip("x")')
    assert check(run).passed


# --- deleted test files ----------------------------------------------------------------------------


def test_deleting_a_test_file_fails(repo, run):
    (repo / "py" / "test_x.py").unlink()
    result = check(run)
    assert not result.passed
    assert [f.file for f in result.findings] == ["py/test_x.py"]
    assert "deletes" in result.failures[0]


# --- the suite's own counts ------------------------------------------------------------------------


def test_fewer_expect_calls_than_the_baseline_fails(repo, run):
    (repo / "t" / "old.sh").write_text("it a\nexpect 1\n")
    result = check(run)
    assert not result.passed
    assert (result.base_counts.expects, result.head_counts.expects) == (3, 2)
    assert "expect()" in result.failures[0]


def test_fewer_tests_than_the_baseline_fails(repo, run):
    (repo / "t" / "old.sh").write_text("expect 1\nexpect 2\n")
    result = check(run)
    assert not result.passed
    assert (result.base_counts.tests, result.head_counts.tests) == (2, 1)


def test_more_tests_pass_and_record_both_counts(repo, run):
    append(repo, "t/old.sh", "it c")
    append(repo, "t/old.sh", "expect 4")
    result = check(run)
    assert result.passed
    assert (result.base_counts.tests, result.head_counts.tests) == (2, 3)
    assert len(result.artifacts) == 2 and all(Path(a).is_file() for a in result.artifacts)


def test_an_unparseable_count_is_unverified_not_a_failure(repo, run):
    append(repo, "t/old.sh", "it c")
    params = IntegrityParams(
        baseline=git(repo, "rev-parse", "HEAD").strip(),
        tests=["t/*.sh"],
        counter=SuiteCounter(argv=["echo", "no summary here"], covers=["t/*.sh"]),
    )
    result = integrity.check(run, params)
    assert result.passed
    assert result.base_counts is None
    assert any("could not" in u or "无法" in u for u in result.unverified)


def test_a_changed_test_the_counter_does_not_cover_is_listed_as_unverified(repo, run):
    append(repo, "py/test_x.py", "def test_y():\n    assert True")
    result = check(run)
    assert result.passed
    assert any("py/test_x.py" in u for u in result.unverified)


@pytest.mark.parametrize(
    ("text", "tests", "expects"),
    [
        (" 210 pass\n 0 fail\n 1091 expect() calls\nRan 210 tests across 9 files. [1.20s]\n", 210, 1091),
        (" 1 pass\n 0 fail\n 1 expect() call\nRan 1 test across 1 file. [5.00ms]\n", 1, 1),
    ],
)
def test_parses_bun_summary_lines(text, tests, expects):
    counts = integrity.parse_bun_summary(text)
    assert (counts.tests, counts.expects) == (tests, expects)


def test_a_summary_without_counts_parses_to_none():
    assert integrity.parse_bun_summary("error: something broke") is None


# --- declared weakening ----------------------------------------------------------------------------


def test_a_declared_skip_passes_and_is_kept_as_a_warning(repo, run):
    append(repo, "t/old.sh", 'test.skip("x")')
    declared = [WeakenedTest(file="t/old.sh", reason="the feature it covers was removed")]
    result = check(run, declared)
    assert result.passed
    assert [f.declared for f in result.findings] == [True]
    assert result.declared == declared


def test_a_declaration_for_another_file_does_not_excuse_this_one(repo, run):
    append(repo, "t/old.sh", 'test.skip("x")')
    result = check(run, [WeakenedTest(file="t/gone.sh", reason="unrelated")])
    assert not result.passed


def test_any_declaration_excuses_a_suite_wide_count_drop(repo, run):
    (repo / "t" / "old.sh").write_text("it a\nexpect 1\n")
    result = check(run, [WeakenedTest(file="t/old.sh", reason="the second assertion duplicated the first")])
    assert result.passed
    assert all(f.declared for f in result.findings)


# --- nothing to check ------------------------------------------------------------------------------


def test_unchanged_tests_pass_without_a_baseline_checkout(repo, run, monkeypatch):
    def no_checkout(*_):
        raise AssertionError("no test changed, so the baseline must not be checked out")

    monkeypatch.setattr(baseline, "checkout", no_checkout)
    append(repo, "src.txt", "v2")
    result = check(run)
    assert result.passed
    assert result.findings == [] and result.base_counts is None


# --- the envelope and the builder's side of the contract -------------------------------------------


def test_a_failed_check_reaches_the_builder_as_a_failing_envelope(repo, run):
    append(repo, "t/old.sh", 'it.only("x")')
    envelope = integrity.as_envelope(check(run))
    assert envelope.status == "fail" and not envelope.passed
    assert "weakened_tests" in envelope.notes_for_next_agent
    assert envelope.failures


def test_weakened_tests_defaults_to_empty():
    assert BuildOutput(status="success", summary="x").weakened_tests == []


def test_weakened_tests_parse_from_a_builder_report():
    report = {"status": "success", "summary": "x", "weakened_tests": [{"file": "t/a.sh", "reason": "obsolete"}]}
    assert BuildOutput.model_validate(report).weakened_tests == [WeakenedTest(file="t/a.sh", reason="obsolete")]


def test_the_builder_report_example_declares_weakened_tests():
    text = (PROMPTS / "builder" / "user.md").read_text()
    example = json.loads(re.search(r"```json\n(.*?)\n```", text, re.S).group(1))
    assert "weakened_tests" in example
    BuildOutput.model_validate(example)
    assert "weakened_tests" in (PROMPTS / "builder" / "system.md").read_text()


def test_the_project_counter_covers_only_the_bun_tests():
    assert quality.SUITE_COUNTER.argv == ["bun", "test"]
    assert quality.SUITE_COUNTER.covers == ["tests/*.test.ts"]
    assert quality.TEST_FILES == [r.pattern for r in quality.PROOF_RUNNERS]
