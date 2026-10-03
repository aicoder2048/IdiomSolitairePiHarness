Write GitHub issue #{{number}}: "{{title}}" ({{url}}). The issue is quoted in full at the end of this request; `gh issue view {{number}} --comments` shows the same.

This is DOCUMENTATION only:
- Only Markdown changes: README.md, docs/, app_docs/, and *.md next to code. No code, config, tests or justfile edits.
- Describe what the code does today — read it before writing, and never describe behaviour that does not exist.
- Keep each file's language and conventions (README.md is Chinese with English technical terms; BTC means Buy to Close).

Where: the files the issue names; otherwise the document that already covers the topic.
Done means: the issue's own "Done means" holds; `git diff --stat` against the baseline touches documentation files only; the suites still pass because nothing else changed.
Out of scope: code changes, even to fix something the writing reveals — note those in the report for a separate issue.

## Issue #{{number}} as filed

{{body}}

## Comments

{{comments}}
