Do GitHub issue #{{number}}: "{{title}}" ({{url}}). The issue and its comments are quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a CHORE — no user-visible behaviour changes:
- Refactors, dependency and tooling changes, scripts, CI, comments and naming are in. Features and fixes are out, however small.
- Test files change only when the chore moves what they import; every assertion keeps its meaning.
- Every command, recipe and entry point that worked before works the same after.

Where: the files the issue names; otherwise the module that owns the code, found before editing. AGENTS.md rules apply.
Done means: the issue's own "Done means" holds; `just test` passes with the same tests as before (count and names); the write-up lists what moved and states that behaviour is unchanged.
Out of scope: behaviour changes, and anything the issue does not ask for.

## Issue #{{number}} as filed

{{body}}

## Comments

{{comments}}
