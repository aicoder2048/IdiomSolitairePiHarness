# Isolated TUI text capture

Issue #19 adds a reusable, standard-library-only screen capture runner. A JSON scene file supplies the launch command, terminal dimensions, readiness marker, masks, and ordered interactions, so the engine itself is not tied to a particular TUI. Each scene runs in its own uniquely named tmux server and produces a normalized `<name>.txt`; `manifest.json` records ordered per-scene success or failure without timestamps or durations. A failed scene does not prevent later scenes from running.

## Implementation

- `scripts/tui_capture.py` validates the complete scene document before capture, launches panes with an explicit filtered `env -i` environment and isolated Pi settings, polls for ready/wait markers, executes literal text or key steps, and always attempts server cleanup. It normalizes the repository path, applies ordered masks, and writes deterministic artifacts. Mask replacement is literal; default masking keeps character widths (wide/fullwidth characters become `##`) and preserves newlines.
- `scripts/tui_scenes.example.json` demonstrates model-free `/status` and `/help` scenes.
- `justfile` provides `just tui-capture scenes out repo="."` for manual real runs and `just test-tui-capture` for offline tests; the latter is part of `just test`. `tests/test_tui_capture.py` uses a scripted fake tmux runner and fake clock, not a real terminal or model. `adws/tests/test_quality_gate.py` checks that the new test recipe remains in the quality gate.
- `README.md` documents invocation, output, configuration, limitations, and the human reproducibility check. `AGENTS.md` records the utility and that real capture is not factory testing. `specs/2b935869_tui-capture-engine.md` records the implementation plan; `requests/issue-19-tui-scripts-tui-capture.md` preserves the task.

## Use and verification

Run against a trusted scene file (its `launch` is a shell command):

```sh
uv run scripts/tui_capture.py --repo . --scenes scripts/tui_scenes.example.json --out captures
# or
just tui-capture scripts/tui_scenes.example.json captures .
```

A successful run returns 0; scene/artifact failures return 1; invalid arguments/configuration or missing tmux return 2. The runner requires a local tmux with `extended-keys-format csi-u` support and the launched program (Pi for the example). It is an environment filter, not a security sandbox. Check `just test` for offline coverage. Real tmux output and three-run byte-for-byte reproducibility are a separate human verification gate; the fake-runner tests do not establish that result. This change does not integrate captures into ADW evidence or add before/after diffing.