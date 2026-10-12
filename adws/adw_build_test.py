#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pydantic", "python-dotenv", "pyyaml", "rich"]
# ///
"""ADW Build Test — implement, then verify; failures flow back into the builder.

Usage:
    uv run adws/adw_build_test.py "<prompt or path/to/prompt.md>" [--config adws/adw_sssf_config/sssf.config.yaml] [--adw-id a1b2c3d4]

Phases: engineer(request) -> builder -> code(test+lint) -> code(prove) -> code(integrity)
        [-> builder(fix | restore) -> code(test+lint) -> code(prove) -> code(integrity) ... bounded]
        -> code(evidence: context_handoff/evidence.md, accepted or not)

Testing and lint are CODE. Their commands are written down in adw_modules/quality.py,
so running it needs no judgement — only repairing it does. Failures reach the
builder as an envelope through `quality.as_envelope`, which is the same door an
agent's report came through, so the repair loop is unchanged.

A failing suite or lint does NOT fail its phase: the runner did its job, the code is
what failed. It fails the run, checked at the end, after the bounded fix loop
has had its chances.

A green suite is followed by two comparisons with the commit the run started
from. The red/green proof (adw_modules/proof.py) is recorded only: this chain
does not know what kind of work it was given. The integrity check
(adw_modules/integrity.py) is binding: a skip marker added to a test, a deleted
test file, or fewer tests or expect() calls than the baseline sends the builder
back, unless it declared that weakening in `weakened_tests`.

The run ends by writing what its code recorded into the session's evidence.md
(adw_modules/evidence.py); adw_pr_feedback appends it to its reply on the PR.
This chain does not commit, so the bundle names HEAD as the uncommitted tree.
"""

import argparse
import sys

from adw_modules import agents, evidence, gates, git_helper, integrity, proof, quality, session, utils
from adw_modules.data_types import AgentCall, BuildOutput, EvidenceInput, IntegrityParams, PhaseParams, ProofParams

REQUIRED_AGENTS = ["builder"]
MAX_FIX_LOOPS = 3


def main(prompt: str, config: str = "adws/adw_sssf_config/sssf.config.yaml", adw_id: str | None = None) -> int:
    cfg = agents.load_config(config)
    agents.validate(cfg, REQUIRED_AGENTS)
    run = session.ensure(cfg, adw_id)
    baseline = git_helper.rev("HEAD")  # what the tests are compared with

    def record(ph, result) -> None:
        passed = sum(1 for check in result.checks if check.passed)
        ph.log(passed=result.passed, checks=f"{passed}/{len(result.checks)}", artifacts=", ".join(result.artifacts))

    def prove(name: str):
        """The red/green record of the tests this run changed — evidence only in this chain."""
        with run.phase(
            PhaseParams(
                name=name,
                kind="code",
                owner="proof",
                description="Record each changed test on the baseline and on HEAD — evidence, never binding here",
            )
        ) as ph:
            result = proof.prove(run, ProofParams(baseline=baseline, runners=quality.PROOF_RUNNERS))
            n = len(result.checks)
            ph.log(
                red=f"{sum(c.red for c in result.checks)}/{n} red on baseline",
                green=f"{sum(c.green for c in result.checks)}/{n} green on HEAD",
                artifacts=", ".join(result.artifacts),
            )
        return result

    def check_integrity(name: str):
        """Whether the change weakened the tests that judge it — undeclared weakening fails."""
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
            ph.log(
                passed=result.passed,
                findings=f"{len(result.failures)} undeclared, {len(result.findings) - len(result.failures)} declared",
                unverified="; ".join(result.unverified),
                artifacts=", ".join(result.artifacts),
            )
        return result

    with run.phase(
        PhaseParams(name="request", kind="engineer", owner=run.engineer, description="Capture the incoming ask")
    ) as ph:
        ph.log(input=prompt)

    with run.phase(
        PhaseParams(name="build", kind="agent", owner="builder", retries=1, description="Implement the request")
    ) as ph:
        builds = [ph.call(AgentCall(output_type=BuildOutput, prompt=prompt, gates=[gates.diff_matches_claims]))]

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
                name=f"fix_{i}",
                kind="agent",
                owner="builder",
                retries=1,
                description="Repair what the suite or lint reported, from its verbatim output",
            )
            previous = quality.as_envelope(test, "tests and lint")

        with run.phase(repair) as ph:
            builds.append(
                ph.call(
                    AgentCall(
                        output_type=BuildOutput, prompt=prompt, previous=previous, gates=[gates.diff_matches_claims]
                    )
                )
            )

    accepted = test is not None and test.passed and intact is not None and intact.passed
    reason = f"the suite, lint or the test-integrity check still failed after {MAX_FIX_LOOPS} fix attempt(s)"
    with run.phase(
        PhaseParams(
            name="evidence",
            kind="code",
            owner="evidence",
            description="Write down what the run's code recorded, and what nobody checked — for the PR reply",
        )
    ) as ph:
        path = evidence.write(
            run,
            EvidenceInput(
                adw_id=run.adw_id,
                workflow="adw_build_test",
                accepted=accepted,
                reason="" if accepted else reason,
                branch=git_helper.current_branch(),
                baseline=baseline,
                diff_stat=git_helper.diff_stat(baseline),
                changed_files=git_helper.diff_files(baseline) + git_helper.untracked_files(),
                quality=test,
                proof=proven,
                integrity=intact,
                new_tests=evidence.new_tests(baseline, quality.TEST_FILES),
                unverified=cfg.evidence.unverified,
                tokens=run.tokens,
                cost=run.cost,
            ),
        )
        ph.log(path=str(path))

    return run.finish(accepted=accepted, reason=reason)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("prompt", help="inline text or a path to a prompt file")
    parser.add_argument("--config", default="adws/adw_sssf_config/sssf.config.yaml")
    parser.add_argument("--adw-id", default=None, help="join or pin an existing session")
    args = parser.parse_args()
    sys.exit(main(utils.resolve_prompt(args.prompt), args.config, args.adw_id))
