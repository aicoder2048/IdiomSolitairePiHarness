#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pydantic", "python-dotenv", "pyyaml", "rich"]
# ///
"""ADW Simple SDLC — plan, build, test, review, document, committing as it goes.

Usage:
    uv run adws/adw_simple_sdlc.py "<prompt or path/to/prompt.md>" [--config adws/adw_sssf_config/sssf.config.yaml] [--adw-id a1b2c3d4]

Phases: engineer(request) -> planner -> git(commit_plan)
        -> builder -> code(test+lint) -> code(prove: red/green) -> code(integrity)
           [-> builder(fix | reproduce | restore) -> code(test+lint) -> code(prove) -> code(integrity) ... bounded]
        -> reviewer [-> builder(revise) -> reviewer ... bounded]
        -> code(retest: test+lint, then prove and integrity, only if a revision changed code)
        -> git(commit_build) -> code(changes) -> documenter -> git(commit_docs)
        -> code(evidence: context_handoff/evidence.md, accepted or not)

Three commits, three work products, three authors. The plan, the code, and the
write-up each land in their own commit, and each commit message is the words of
the agent that produced it — `commit_message` on PlanOutput describes the spec,
on BuildOutput the code, on DocumentOutput the write-up. No agent's sentence is
ever reused for another agent's diff.

Testing and lint are CODE, not an agent. `bun test` is a command, not a judgement call:
an agent rediscovering it every run costs a million tokens to learn what a
subprocess already knows. Failures travel back to the builder as an envelope,
so the repair loop is unchanged — only the runner became free and repeatable.

Two different questions still get asked, in order. The suite asks "does it
run"; the reviewer asks "is this what was asked for", against `plan.md` — and
neither can answer the other's. A revision that closes a review finding
re-enters the suite, so the tree that gets committed is the tree that was both
tested and approved.

A green suite cannot say whether a new test would have caught the bug, so a
green run is followed by the red/green proof (adw_modules/proof.py): every test
the change added or edited is run on the baseline commit, where it must fail,
and on HEAD, where it must pass. For `--kind bug` that is binding and a failed
proof sends the builder back to write a test that reproduces the bug; for any
other kind it is recorded as evidence only.

A green suite also cannot say whether it was made green by weakening it, so the
integrity check (adw_modules/integrity.py) follows: a skip/focus marker added to
a test, a deleted test file, or fewer tests or expect() calls than the baseline
sends the builder back to restore them — for every kind — unless the builder
declared that weakening in `weakened_tests`, which passes and is kept for the PR.

The code commit lands after verification, not straight after the build: fixes
and revisions are part of the same work product, and red code has no business
on the branch. A run that fails verification therefore leaves the plan
committed and the working tree dirty — the spec is a real artifact either way,
and the unfinished code stays where the engineer can see it.

Last, code writes what it recorded — commands and their counts, the red/green
pair, the integrity comparison, the reviewer's table, what nobody checked — into
the session's evidence.md (adw_modules/evidence.py). adw_issue makes it the PR
body. It is written for a run that was not accepted too: that is when it is read.

The documenter measures against the commit this run STARTED from, not against
`main`, because by then the run has moved `main` itself. That baseline is
pinned before the first commit phase and printed in the request phase.
"""

import argparse
import sys

from adw_modules import agents, changes, evidence, gates, git_helper, integrity, proof, quality, session, utils
from adw_modules.data_types import (
    AgentCall,
    BuildOutput,
    ChangeCapture,
    DocumentOutput,
    EvidenceInput,
    IntegrityParams,
    PhaseParams,
    PlanOutput,
    ProofParams,
    ReviewOutput,
)

REQUIRED_AGENTS = ["planner", "builder", "reviewer", "documenter"]
MAX_FIX_LOOPS = 3
MAX_REVISION_LOOPS = 2

DOCUMENT_NOTES = (
    "Read diff_path in full before writing. Document only what the "
    "diff shows, then copy the write-up into app_docs/ as your task "
    "describes."
)


KINDS = ("bug", "feature", "chore", "docs")


def main(
    prompt: str,
    config: str = "adws/adw_sssf_config/sssf.config.yaml",
    adw_id: str | None = None,
    kind: str | None = None,
) -> int:
    cfg = agents.load_config(config)
    agents.validate(cfg, REQUIRED_AGENTS)
    run = session.ensure(cfg, adw_id)
    baseline = git_helper.rev("HEAD")  # pinned before this run commits anything

    def commit(ph, envelope) -> None:
        """Commit what the preceding phase produced, in that agent's own words."""
        message = envelope.commit_message or f"sssf({run.adw_id}): {envelope.summary}"
        ph.log(sha=git_helper.commit_all(message), message=message)

    def record(ph, result) -> None:
        """Log a deterministic block's verdict — the same shape every ADW uses."""
        passed = sum(1 for check in result.checks if check.passed)
        ph.log(passed=result.passed, checks=f"{passed}/{len(result.checks)}", artifacts=", ".join(result.artifacts))

    def prove(name: str):
        """The red/green proof of the tests this run changed — binding only for a bug."""
        with run.phase(
            PhaseParams(
                name=name,
                kind="code",
                owner="proof",
                description="Run each changed test on the baseline (must fail) and on HEAD (must pass)",
            )
        ) as ph:
            result = proof.prove(run, ProofParams(kind=kind, baseline=baseline, runners=quality.PROOF_RUNNERS))
            n = len(result.checks)
            ph.log(
                passed=result.passed,
                binding=result.required,
                red=f"{sum(c.red for c in result.checks)}/{n} red on baseline",
                green=f"{sum(c.green for c in result.checks)}/{n} green on HEAD",
                artifacts=", ".join(result.artifacts),
            )
        return result

    def check_integrity(name: str):
        """Whether the change weakened the tests that judge it — undeclared weakening fails, for every kind."""
        with run.phase(
            PhaseParams(
                name=name,
                kind="code",
                owner="integrity",
                description="Compare the tests with the baseline: no undeclared skip, deletion or lost assertions",
            )
        ) as ph:
            declared = [w for b in builds for w in b.weakened_tests]
            params = IntegrityParams(
                baseline=baseline, tests=quality.TEST_FILES, counter=quality.SUITE_COUNTER, declared=declared
            )
            result = integrity.check(run, params)
            counts = (
                f"{result.base_counts.tests}→{result.head_counts.tests} tests, "
                f"{result.base_counts.expects}→{result.head_counts.expects} expect() calls"
                if result.base_counts and result.head_counts
                else "not compared"
            )
            ph.log(
                passed=result.passed,
                findings=f"{len(result.failures)} undeclared, {len(result.findings) - len(result.failures)} declared",
                counts=counts,
                unverified="; ".join(result.unverified),
                artifacts=", ".join(result.artifacts),
            )
        return result

    with run.phase(
        PhaseParams(name="request", kind="engineer", owner=run.engineer, description="Capture the incoming ask")
    ) as ph:
        ph.log(input=prompt, baseline=git_helper.short_sha(baseline))

    with run.phase(
        PhaseParams(
            name="plan", kind="agent", owner="planner", description="Turn the request into an implementable plan"
        )
    ) as ph:
        plan = ph.call(
            AgentCall(output_type=PlanOutput, prompt=prompt, gates=[gates.artifacts_exist, gates.files_non_empty])
        )

    with run.phase(
        PhaseParams(
            name="commit_plan",
            kind="code",
            owner="git",
            description="Put the spec on record before any code exists to blur it",
        )
    ) as ph:
        commit(ph, plan)

    with run.phase(
        PhaseParams(name="build", kind="agent", owner="builder", retries=1, description="Implement the plan exactly")
    ) as ph:
        build = ph.call(
            AgentCall(output_type=BuildOutput, prompt=prompt, previous=plan, gates=[gates.diff_matches_claims])
        )
    builds = [build]  # every builder pass, in order — the first one names the commit

    test = None
    proven = None
    intact = None
    for i in range(1, MAX_FIX_LOOPS + 1):
        with run.phase(
            PhaseParams(
                name=f"test_{i}",
                kind="code",
                owner="quality",
                description="Run the suite and lint — known commands, so code runs them and no agent rediscovers them",
            )
        ) as ph:
            test = quality.run_tests_and_lint(run)
            record(ph, test)

        if test.passed:
            proven = prove(f"prove_{i}")
            if proven.passed:
                intact = check_integrity(f"integrity_{i}")
                if intact.passed:
                    break
                repair = PhaseParams(
                    name=f"restore_{i}",
                    kind="agent",
                    owner="builder",
                    retries=1,
                    description="Restore the tests the change weakened, or declare why weakening them is right",
                )
                previous = integrity.as_envelope(intact)
            else:
                repair = PhaseParams(
                    name=f"reproduce_{i}",
                    kind="agent",
                    owner="builder",
                    retries=1,
                    description="Write the test that fails without the fix — the proof found none on the baseline",
                )
                previous = proof.as_envelope(proven)
        else:
            repair = PhaseParams(
                name=f"fix_{i}",
                kind="agent",
                owner="builder",
                retries=1,
                description="Repair what the suite or lint reported, from its verbatim output",
            )
            previous = quality.as_envelope(test, "tests and lint")

        with run.phase(repair) as ph:
            build = ph.call(
                AgentCall(output_type=BuildOutput, prompt=prompt, previous=previous, gates=[gates.diff_matches_claims])
            )
            builds.append(build)

    review = None
    revised = False
    for i in range(1, MAX_REVISION_LOOPS + 1):
        with run.phase(
            PhaseParams(
                name=f"review_{i}", kind="agent", owner="reviewer", description="Confirm the build matches the plan"
            )
        ) as ph:
            review = ph.call(
                AgentCall(
                    output_type=ReviewOutput,
                    prompt=prompt,
                    previous=build,
                    gates=[gates.artifacts_exist, gates.verdict_consistent],
                )
            )

        if review.approved or i == MAX_REVISION_LOOPS:
            break

        with run.phase(
            PhaseParams(
                name=f"revise_{i}",
                kind="agent",
                owner="builder",
                retries=1,
                description="Close the reviewer's blocking findings",
            )
        ) as ph:
            build = ph.call(
                AgentCall(output_type=BuildOutput, prompt=prompt, previous=review, gates=[gates.diff_matches_claims])
            )
            builds.append(build)
            revised = True

    # A revision edited code after the suite last ran, so the green light is
    # stale. Re-run it rather than commit on a result that predates the change.
    if revised and review is not None and review.approved:
        with run.phase(
            PhaseParams(
                name="retest",
                kind="code",
                owner="quality",
                description="Re-run the suite and lint — the revision changed code after the last green result",
            )
        ) as ph:
            test = quality.run_tests_and_lint(run)
            record(ph, test)
        if test.passed:
            proven = prove("reprove")
            intact = check_integrity("reintegrity")

    # Red tests, a failed proof, weakened tests or a rejected review stop the chain here: the code stays
    # uncommitted and nothing is documented, because there is nothing worth
    # describing yet. The plan commit stands — it is a record of what was asked.
    verified = (
        test is not None
        and test.passed
        and proven is not None
        and proven.passed
        and intact is not None
        and intact.passed
        and review is not None
        and review.approved
    )
    if verified:
        with run.phase(
            PhaseParams(
                name="commit_build",
                kind="code",
                owner="git",
                description="Land the code only now: green suite and lint, proof and integrity hold, approved review",
            )
        ) as ph:
            message = git_helper.build_commit_message(builds, run.adw_id)
            ph.log(sha=git_helper.commit_all(message), message=message)

        with run.phase(
            PhaseParams(
                name="changes",
                kind="code",
                owner="git",
                description="Diff the whole run against its pinned baseline, for the documenter",
            )
        ) as ph:
            changeset = changes.capture(run, ChangeCapture(base=baseline))
            ph.log(
                base=f"{changeset.base.label} @ {changeset.base.commit[:7]}",
                reason=changeset.base.reason,
                files=len(changeset.files) + len(changeset.untracked),
                lines=f"+{changeset.insertions} -{changeset.deletions}",
                diff=changeset.diff_path,
            )
            if changeset.empty:
                raise RuntimeError(
                    f"nothing changed since {changeset.base.label} "
                    f"({changeset.base.reason}) — there is nothing to document."
                )

        with run.phase(
            PhaseParams(
                name="document",
                kind="agent",
                owner="documenter",
                retries=1,
                description="Write up the completed change",
            )
        ) as ph:
            document = ph.call(
                AgentCall(
                    output_type=DocumentOutput,
                    prompt=prompt,
                    previous=changes.as_envelope(changeset, DOCUMENT_NOTES),
                    gates=[gates.artifacts_exist, gates.files_non_empty],
                )
            )

        with run.phase(
            PhaseParams(
                name="commit_docs",
                kind="code",
                owner="git",
                description="Ship the write-up in its own commit, beside the code it describes",
            )
        ) as ph:
            commit(ph, document)

    reason = "the suite, lint, the red/green proof, the test-integrity check or the review never came back clean"
    with run.phase(
        PhaseParams(
            name="evidence",
            kind="code",
            owner="evidence",
            description="Write down what the run's code recorded, and what nobody checked — the PR body",
        )
    ) as ph:
        path = evidence.write(
            run,
            EvidenceInput(
                adw_id=run.adw_id,
                workflow="adw_simple_sdlc",
                kind=kind,
                accepted=verified,
                reason="" if verified else reason,
                branch=git_helper.current_branch(),
                baseline=baseline,
                head=git_helper.rev("HEAD") if verified else "",
                diff_stat=git_helper.diff_stat(baseline),
                changed_files=git_helper.diff_files(baseline) + git_helper.untracked_files(),
                quality=test,
                proof=proven,
                integrity=intact,
                new_tests=evidence.new_tests(baseline, quality.TEST_FILES),
                review=review,
                unverified=cfg.evidence.unverified,
                tokens=run.tokens,
                cost=run.cost,
            ),
        )
        ph.log(path=str(path))

    return run.finish(accepted=verified, reason=reason)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", help="inline text or a path to a prompt file")
    parser.add_argument("--config", default="adws/adw_sssf_config/sssf.config.yaml")
    parser.add_argument("--adw-id", default=None, help="join or pin an existing session")
    parser.add_argument("--kind", choices=KINDS, default=None, help="kind of work; a bug must prove its test red/green")
    args = parser.parse_args()
    sys.exit(main(utils.resolve_prompt(args.prompt), args.config, args.adw_id, args.kind))
