"""The red/green proof: every test the change adds or edits fails before it and passes after it.

"Start with a test that fails on the current code" is a sentence in a prompt,
and a green suite cannot tell a test that reproduces the bug from one that
would have passed all along. This can: each changed test file's HEAD version is
copied into a checkout of the baseline commit and run there (it must FAIL),
then run in the repo (it must PASS). Both outputs are kept as artifacts — they
are the before/after pair the PR shows.

Binding only for a bug. A feature's new test usually fails on the baseline for a
trivial reason (the module it imports does not exist yet), so for every other
kind the proof is recorded and never fails the run.

The granularity is the file, not the test case: a file with one new failing
test among old passing ones is red on the baseline, which is the claim.
"""

from __future__ import annotations

import fnmatch
import shlex
import shutil
import subprocess
from pathlib import Path

from . import baseline, git_helper
from .data_types import ProofCheck, ProofParams, ProofResult, ProofRunner, VerifyOutput
from .utils import operator_env

TAIL_CHARS = 2_000  # per side; the full output is in the artifact


def runner_for(path: str, runners: list[ProofRunner]) -> ProofRunner | None:
    return next((r for r in runners if fnmatch.fnmatchcase(path, r.pattern)), None)


def changed_tests(params: ProofParams) -> list[str]:
    """Test files that exist now and differ from the baseline: edited, or new and untracked."""
    paths = set(git_helper.diff_files(params.baseline)) | set(git_helper.untracked_files())
    return sorted(p for p in paths if Path(p).is_file() and runner_for(p, params.runners))


def execute(argv: list[str], cwd: Path, timeout: int) -> tuple[int, str]:
    """Run `argv` in `cwd` as the operator would; a timeout exits 124, a missing binary 127."""
    try:
        done = subprocess.run(argv, cwd=cwd, env=operator_env(), capture_output=True, text=True, timeout=timeout)
        return done.returncode, done.stdout + done.stderr
    except subprocess.TimeoutExpired as error:
        return 124, f"{error.stdout or ''}{error.stderr or ''}\nTimed out after {timeout}s."
    except OSError as error:
        return 127, str(error)


def _check(run, tree: Path, path: str, runner: ProofRunner) -> ProofCheck:
    repo = Path(run.repo_root)
    (tree / path).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(repo / path, tree / path)  # the test as the change has it, against the code before it
    argv = [arg.replace("{file}", path) for arg in runner.argv]
    base_rc, base_out = execute(argv, tree, runner.timeout_seconds)
    head_rc, head_out = execute(argv, repo, runner.timeout_seconds)

    seq = run.phases[-1].seq if run.phases else 0
    artifact = Path(run.context_handoff_dir) / "proof" / f"{seq:02d}" / (path.replace("/", "__") + ".log")
    artifact.parent.mkdir(parents=True, exist_ok=True)
    command = shlex.join(argv)
    artifact.write_text(
        f"$ {command}\n\n--- baseline: exit {base_rc} ---\n{base_out}\n--- HEAD: exit {head_rc} ---\n{head_out}\n"
    )
    return ProofCheck(
        file=path,
        command=command,
        base_returncode=base_rc,
        head_returncode=head_rc,
        base_tail=base_out[-TAIL_CHARS:],
        head_tail=head_out[-TAIL_CHARS:],
        output_artifact=str(artifact),
    )


def prove(run, params: ProofParams) -> ProofResult:
    """Run every changed test on the baseline and on HEAD, and judge the pair."""
    required = params.kind == "bug"
    files = changed_tests(params)
    checks: list[ProofCheck] = []
    if files:
        with baseline.checkout(run, params.baseline) as tree:
            checks = [_check(run, tree, f, runner_for(f, params.runners)) for f in files]

    failures: list[str] = []
    if required and not checks:
        patterns = ", ".join(r.pattern for r in params.runners)
        failures.append(
            f"no test reproduces the bug: the change adds or edits no test file ({patterns}). "
            "Add a test that fails on the code as it was and passes with the fix."
        )
    if required:
        short = params.baseline[:7]
        for c in checks:
            if not c.red:
                failures.append(
                    f"{c.file}: passes on the baseline {short} too (`{c.command}` exited 0), so it does not "
                    f"reproduce the bug. Baseline output:\n{c.base_tail}".rstrip()
                )
            if not c.green:
                failures.append(
                    f"{c.file}: fails on HEAD (`{c.command}` exited {c.head_returncode}):\n{c.head_tail}".rstrip()
                )
    return ProofResult(
        required=required,
        passed=not failures,
        baseline=params.baseline,
        checks=checks,
        failures=failures,
        artifacts=[c.output_artifact for c in checks],
    )


def as_envelope(result: ProofResult) -> VerifyOutput:
    """Hand a failed proof back to the builder through the same door a red suite uses."""
    return VerifyOutput(
        status="success" if result.passed else "fail",
        summary=(
            f"red/green proof: {sum(c.red for c in result.checks)} of {len(result.checks)} changed test file(s) "
            f"fail on the baseline, {sum(c.green for c in result.checks)} pass on HEAD"
        ),
        artifacts=result.artifacts,
        notes_for_next_agent=(
            ""
            if result.passed
            else "Each test you add for this bug must fail on the baseline commit and pass with your fix. "
            "Make the test exercise the reported behaviour; keep the fix."
        ),
        passed=result.passed,
        failures=result.failures,
    )
