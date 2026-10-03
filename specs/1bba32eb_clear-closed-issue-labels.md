# Plan: clear stale completion labels from closed issues

## Goal and scope

Implement issue #4 in the issue lane of `scripts/autoqueue.py`: after acquiring the pass lock and successfully fetching origin, but before discovering queued issues, remove `factory:pr-open` from closed issues. Cleanup is best-effort and must never change the queue's exit status. Do not change game behavior, feedback processing, cron generation, author filtering, claim/finalization behavior, or other labels. No GitHub Action, PR-label cleanup, or handling of unmerged closed PRs.

## Existing implementation

- `DONE` already holds `factory:pr-open`; reuse it everywhere in new production code, including messages.
- `listing()` appends `--limit 10000`, decodes JSON, requires an array of objects, and rejects results at the limit.
- `mutation()` returns a boolean and diagnoses command failures on stderr. Do not duplicate its failure diagnostic.
- `main()` acquires `pass_lock()`, fetches origin, runs and returns from the feedback branch if selected, then invokes `candidates()` and processes issues. The cleanup belongs immediately before the issue `candidates()` loop, after the feedback branch has returned.
- `tests/test_autoqueue.py` supplies real local Git and configurable executable shims. Its issue-list shim currently conflates all issue queries; split closed and open responses without altering existing open-query configuration.

## Files to change

1. `scripts/autoqueue.py`: one focused cleanup helper and one issue-lane invocation.
2. `tests/test_autoqueue.py`: closed-query shim support, behavioral tests, and precise call-expectation updates.
3. `docs/factory-labels.md`: lifecycle documentation.
4. `AGENTS.md`: rule 12 lifecycle clause.
5. `README.md`: brief operator-facing note/link, without changing player commands.

## Behavior and data flow

Add a helper such as `clear_closed_done(root, dry_run)` near the existing GitHub discovery helpers:

1. Call `listing(root, ["gh", "issue", "list", "--state", "closed", "--label", DONE, "--json", "number"])`. Do not add a separate limit or extra GitHub lookups.
2. Validate all returned records before any edit: `number` must be present, an actual positive integer (not a boolean). Then sort numerically ascending. This small validation follows the existing candidate-validation style and ensures malformed records cannot cause partial cleanup or malformed edit targets.
3. Catch discovery/validation failures locally (`OSError`, `RuntimeError`, `ValueError`, `KeyError`, `TypeError`; the JSON decoder's error is a `ValueError`). Emit one contextual stderr line, e.g. `autoqueue: closed-issue cleanup skipped: {exc}`, then return normally. Keep the outer queue exception handler unchanged: normal queue-discovery failures must still fail closed.
4. For each sorted issue number:
   - Dry run: print exactly `would clear {DONE} from closed #{number}` and do not call `mutation()`.
   - Otherwise call `mutation(root, ["gh", "issue", "edit", str(number), "--remove-label", DONE])`. Only on success print exactly `cleared {DONE} from closed #{number}`.
   - On mutation failure, its existing stderr diagnostic is sufficient; continue to remaining cleanup records and then the normal queue. Never print a false success, create failure comments, or set the pass's `failed` flag.
5. Invoke the helper with `ROOT` and `args.dry_run` before `candidates(ROOT, args.max)`, in the issue-only path described above.

Choices: cleanup applies to every closed result, independent of queue `--max`, author, assignment, or worktree state. Use the existing listing ceiling rather than new pagination. No new label constant, dependencies, flags, persistent state, or retries. Dry run retains the existing lock/fetch behavior but makes no new mutations. An individual failed edit does not stop other cleanup attempts. The next issue pass naturally re-queries remaining labels.

## Tests (write first, then implement)

Extend SHIM's `gh issue list` branch to inspect `--state`: closed queries use configurable `closed_issues` (default `[]`) and optional `raw_closed_issues`; open queries retain `issues` and `raw_issues`. Continue using the existing prefix-based `reject` mechanism to fail only the closed query. Do not introduce live GitHub access or a new harness.

Add tests covering:

- **Successful cleanup then normal processing:** configure unsorted closed records (e.g. 20 and 2) plus queued issue 13. Assert the exact closed-list argv including `--limit 10000`; cleanup edits occur once each in order 2, 20 and contain only `--remove-label factory:pr-open`. Assert exact cleared lines, followed by successful ordinary processing of 13 and return code 0. Inspect recorded call order to prove fetch precedes cleanup, cleanup precedes the open candidate query/claim, and cleanup runs under the recorded lock. Having more closed records than the default maximum also proves cleanup is not limited by `--max`. Exact edit argv establishes that no other labels, including `factory:needs-human`, are removed; no PR edits are made by cleanup.
- **Dry run:** configure nonempty unsorted closed records and the ordinary queued issue. Assert sorted exact would-clear lines precede `would pick #13: Issue 13`; there are no GitHub mutations, worker runs, or cleanup success lines.
- **Discovery failure is nonfatal:** reject `["gh", "issue", "list", "--state", "closed"]`. Assert a cleanup diagnostic on stderr, no cleanup edits, and normal queued issue processing with its ordinary successful return code.
- **Malformed cleanup data is nonfatal:** parameterize invalid JSON, non-list JSON, non-object list elements, missing/invalid numbers, and a result reaching the listing limit. Assert one cleanup diagnostic, no cleanup edits, no traceback, and normal queued issue processing. Include a valid record before an invalid one to prove validation happens before mutation.
- **Mutation failure is nonfatal:** fail only one closed issue's edit, assert a stderr diagnostic, no cleared line for that number, successful cleanup of another closed record, and normal processing of the queued issue. Parameterize queued-worker success/failure if convenient to explicitly verify the pass exit code remains determined by normal processing.
- **Lane isolation:** add a focused feedback dry-run assertion/test with closed records configured; there must be no closed-issue query or cleanup and no would-clear lines. Existing cron tests already require no tool calls; preserve those assertions. Existing lock-contention and fetch-failure tests must continue to prevent cleanup.

Update `test_live_nonholding_pid_is_reclaimed`'s exact GitHub call-prefix list to include the additional initial `issue list` (closed list, open list, PR list). Inspect other precise call expectations and update only where the issue-lane query changes them; keep their original intent and all existing safety assertions. The default-empty closed response should leave existing stdout and mutation expectations unchanged.

## Documentation

- In `docs/factory-labels.md` section 3, immediately after the merge lifecycle, state in Chinese that the next `just autoqueue` clears `factory:pr-open` from closed issues; other labels (especially `factory:needs-human`) remain. Briefly mention preview-only `--dry-run` and nonblocking cleanup failures nearby.
- Append a short clause to `AGENTS.md` rule 12 about the next issue pass removing only `factory:pr-open` from closed issues after merge.
- Add a small Chinese factory-queue note to `README.md`, linking `docs/factory-labels.md` and summarizing next-pass cleanup and dry-run preview. Keep the player-facing material untouched.

## Verification and completion

1. Before implementing the helper, run new tests using `uv run --no-project --with pytest pytest tests/test_autoqueue.py -q -k 'closed'` and confirm failure for the missing behavior by exit status.
2. After implementation run `just test-autoqueue`.
3. Run required complete gates: `just test` and `just lint`; both must exit 0. Fix only relevant failures and formatting. Do not run paid `just smoke` or live queue commands.
4. Review the changes against the exact messages, query/edit arguments, numeric ordering, issue-only placement, nonfatal failure behavior, and documentation requirements above.

Planning only: no production code or tests have been changed or executed in this planning phase. GitHub issue details are supplied in the task; do not run `gh` for recon or verification.
