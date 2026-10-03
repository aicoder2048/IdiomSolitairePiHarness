Implement GitHub issue #{{number}}: "{{title}}" ({{url}}). The issue and its comments are quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a FEATURE — new behaviour, or existing behaviour made better:
- Plan before building: the plan names the files, the data flow and the tests, and the builder follows it.
- New behaviour comes with tests that describe it. Existing tests keep passing unchanged, unless the issue changes what they test.
- Document it in the same change: README.md (player-facing: how to play, commands) and AGENTS.md when it adds a rule.
- Where the issue leaves a choice open, take the simplest option that satisfies it and record the choice in the plan.

Where: the files the issue names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point under the issue's own "Done means" holds; tests cover the new behaviour; `just test` passes; README/docs describe what changed.
Out of scope: anything the issue does not ask for; redesigns of neighbouring code.

## Issue #{{number}} as filed

{{body}}

## Comments

{{comments}}
