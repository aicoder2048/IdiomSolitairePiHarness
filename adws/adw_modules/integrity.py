"""The test-integrity check: a change may not quietly weaken the tests that judge it.

A builder that cannot make a test pass can make it stop asking — skip it, focus
another test with `.only`, delete the file, drop an assertion — and the suite
goes green. A green suite cannot see that; a comparison with the baseline can.
Three signals, all deterministic:

- a skip/focus marker in a line the change ADDS to a test file (removing one is fine);
- a test file that existed on the baseline and is gone;
- fewer tests or fewer expect() calls than the baseline, counted by running the
  suite in a checkout of the baseline and in the repo (bun's summary lines).

Weakening is sometimes right — the behaviour a test checked was removed on
purpose. So the builder may declare it in `BuildOutput.weakened_tests`: a
declared file passes, and the result keeps it so the PR can show it first. Only
undeclared findings fail. A count drop is suite-wide, so any declaration excuses it.

What it cannot see is said, not hidden: test files the counter does not cover
(pytest here) are checked for markers and deletion only, and listed as unverified.
"""

from __future__ import annotations

import fnmatch
import re
import shlex
from pathlib import Path

from . import baseline, git_helper, proof
from .data_types import IntegrityFinding, IntegrityParams, IntegrityResult, SuiteCounter, SuiteCounts, VerifyOutput

# bun: test.skip( it.only( describe.todo( test.skipIf( test.if(false) — pytest: mark.skip(if) mark.xfail pytest.skip(
MARKER = re.compile(
    r"pytest\.mark\.(?:skip|xfail)|pytest\.skip\(|unittest\.skip|\.(?:skip|only|todo|skipIf|todoIf)\(|\.if\(\s*false"
)
ANSI = re.compile(r"\x1b\[[0-9;]*m")


def is_test(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, p) for p in patterns)


def parse_bun_summary(text: str) -> SuiteCounts | None:
    """`Ran 210 tests across 9 files.` and `1091 expect() calls` → counts; None if either is missing."""
    text = ANSI.sub("", text)
    ran = re.search(r"^Ran (\d+) tests? across", text, re.M)
    expects = re.search(r"^\s*(\d+) expect\(\) calls?\b", text, re.M)
    if not (ran and expects):
        return None
    return SuiteCounts(tests=int(ran[1]), expects=int(expects[1]))


def _markers(path: str, lines: list[str]) -> list[IntegrityFinding]:
    found = []
    for line in lines:
        match = MARKER.search(line)
        if match:
            found.append(IntegrityFinding(file=path, problem=f"adds `{match[0]}`: {line.strip()[:200]}"))
    return found


def _count(run, cwd: Path, counter: SuiteCounter, side: str) -> tuple[SuiteCounts | None, str]:
    returncode, output = proof.execute(counter.argv, cwd, counter.timeout_seconds)
    seq = run.phases[-1].seq if run.phases else 0
    artifact = Path(run.context_handoff_dir) / "integrity" / f"{seq:02d}" / f"count-{side}.log"
    artifact.parent.mkdir(parents=True, exist_ok=True)
    artifact.write_text(f"$ {shlex.join(counter.argv)}\nexit: {returncode}\n\n{output}")
    return parse_bun_summary(output), str(artifact)


def check(run, params: IntegrityParams) -> IntegrityResult:
    """Compare the change's tests with the baseline's; fail on any weakening not declared."""
    untracked = set(git_helper.untracked_files())
    changed = sorted(
        p
        for p in set(git_helper.diff_files(params.baseline)) | untracked
        if Path(p).is_file() and is_test(p, params.tests)
    )
    deleted = sorted(p for p in git_helper.deleted_files(params.baseline) if is_test(p, params.tests))

    findings: list[IntegrityFinding] = []
    for path in changed:
        if path in untracked:
            lines = Path(path).read_text(encoding="utf-8", errors="replace").splitlines()
        else:
            lines = git_helper.added_lines(params.baseline, path)
        findings += _markers(path, lines)
    findings += [IntegrityFinding(file=path, problem="deletes the test file") for path in deleted]

    touched = changed + deleted
    counter = params.counter
    counted = [p for p in touched if counter and is_test(p, counter.covers)]
    base_counts = head_counts = None
    artifacts: list[str] = []
    unverified: list[str] = []
    if counted:
        with baseline.checkout(run, params.baseline) as tree:
            base_counts, base_log = _count(run, tree, counter, "baseline")
        head_counts, head_log = _count(run, Path(run.repo_root), counter, "head")
        artifacts = [base_log, head_log]
        short = params.baseline[:7]
        if base_counts is None or head_counts is None:
            unverified.append(
                f"无法从 `{shlex.join(counter.argv)}` 的输出解析用例数，用例数没有比较（输出见 {', '.join(artifacts)}）"
            )
        else:
            if head_counts.tests < base_counts.tests:
                findings.append(
                    IntegrityFinding(
                        file="",
                        problem=f"the suite runs {head_counts.tests} tests, {base_counts.tests} on the baseline {short}",
                    )
                )
            if head_counts.expects < base_counts.expects:
                findings.append(
                    IntegrityFinding(
                        file="",
                        problem=f"the suite makes {head_counts.expects} expect() calls, "
                        f"{base_counts.expects} on the baseline {short}",
                    )
                )
    uncounted = [p for p in touched if p not in counted]
    if uncounted:
        unverified.append(f"这些测试文件的用例数没有比较，只查了跳过标记和删除：{', '.join(uncounted)}")

    declared_files = {w.file for w in params.declared}
    for finding in findings:
        finding.declared = finding.file in declared_files if finding.file else bool(declared_files)
    failures = [f"{f.file or 'the suite'}: {f.problem}" for f in findings if not f.declared]
    return IntegrityResult(
        passed=not failures,
        baseline=params.baseline,
        base_counts=base_counts,
        head_counts=head_counts,
        findings=findings,
        declared=params.declared,
        failures=failures,
        artifacts=artifacts,
        unverified=unverified,
    )


def as_envelope(result: IntegrityResult) -> VerifyOutput:
    """Hand undeclared weakening back to the builder through the same door a red suite uses."""
    undeclared = sum(1 for f in result.findings if not f.declared)
    return VerifyOutput(
        status="success" if result.passed else "fail",
        summary=(
            f"test integrity: {undeclared} undeclared and {len(result.findings) - undeclared} declared "
            "weakening(s) of the tests"
        ),
        artifacts=result.artifacts,
        notes_for_next_agent=(
            ""
            if result.passed
            else "These changes weaken the tests that judge your work. Restore each one and make the code pass "
            "it instead. Only if weakening a test is genuinely right — the behaviour it checks was removed or "
            "changed on purpose — keep it and declare it in `weakened_tests` with the file and the reason; "
            "the PR will show it."
        ),
        passed=result.passed,
        failures=result.failures,
    )
