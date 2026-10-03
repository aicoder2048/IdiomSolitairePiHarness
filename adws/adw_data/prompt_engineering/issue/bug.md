Fix GitHub issue #{{number}}: "{{title}}" ({{url}}). The issue and its comments are quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a BUG fix:
- Start with a test that reproduces the reported behaviour and fails on the current code; the fix makes it pass. That test ships with the fix.
- Change only what the fix needs. No refactors, renames or features alongside it.
- If what the issue expects contradicts README.md, AGENTS.md or docs/agentic-engineering-paper.md, stop and say so in the report instead of guessing which one is right — unless the issue itself asks for that text to change: a bug in documented behaviour is fixed together with the document that describes it.

Where: the files the issue names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: the new test fails before the fix and passes after; `just test` passes; the write-up names the root cause and the test that pins it.
Out of scope: anything the issue does not ask for, including nearby cleanups.

## Issue #{{number}} as filed

{{body}}

## Comments

{{comments}}
