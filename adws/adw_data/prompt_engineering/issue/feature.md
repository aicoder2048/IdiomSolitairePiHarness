Implement GitHub issue #{{number}}: "{{title}}" ({{url}}). The issue is quoted in full at the end of this request; `gh issue view {{number}} --comments` shows the same.

This is a FEATURE — new behaviour, or existing behaviour made better:
- Plan before building: the plan names the files, the data flow and the tests, and the builder follows it.
- New behaviour comes with tests that describe it. Existing tests keep passing unchanged, unless the issue changes what they test.
- Document it in the same change: README.md, and the cookbook under docs/tech-papers/ when the feature has a recipe.
- Where the issue leaves a choice open, take the simplest option that satisfies it and record the choice in the plan.

Where: the files the issue names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point under the issue's own "Done means" holds; tests cover the new behaviour; `uv run pytest`, `just test-extensions` and `just test-adws` pass; README/docs describe what changed.
Out of scope: anything the issue does not ask for; redesigns of neighbouring code.

## Issue #{{number}} as filed

{{body}}

## Comments

{{comments}}
