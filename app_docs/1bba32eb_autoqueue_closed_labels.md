# Closed-issue label cleanup in autoqueue

`just autoqueue` now removes the stale `factory:pr-open` label from closed issues on its issue-processing path. The cleanup runs after the pass lock is acquired and `git fetch` completes, before queued issues are discovered. This keeps merged work from appearing to remain under review without hiding other status labels, particularly `factory:needs-human`.

## Behavior and implementation

In `scripts/autoqueue.py`, `clear_closed_done()` uses the existing `listing()` helper to query closed issues carrying the existing `DONE` label, validates the returned issue numbers, and processes them in ascending order using `mutation()`. Successful edits print `cleared factory:pr-open from closed #N`. With `--dry-run`, it prints `would clear factory:pr-open from closed #N` without editing labels.

Cleanup is best-effort: query or response-validation failures produce a diagnostic on stderr and do not prevent normal queue processing. Failed individual edits use the mutation helper's diagnostic and do not prevent later cleanup or affect the queue's exit status. The helper is called only in the issue lane; feedback and cron do not perform this cleanup.

## Documentation and verification

`docs/factory-labels.md` describes the lifecycle, dry-run preview, and nonblocking failures; `AGENTS.md` rule 12 records that only the closed issue's `factory:pr-open` label is cleared on a later issue pass. `README.md` gives a brief operator-facing summary and links to the lifecycle details.

`tests/test_autoqueue.py` covers sorted cleanup before queue processing, dry-run preview without mutations, nonfatal query and malformed-data failures, nonfatal edit failures, and feedback-lane isolation. To verify the change, run `just test-autoqueue`, then the project gates `just test` and `just lint`.