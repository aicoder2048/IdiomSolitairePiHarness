# Plan: isolated, deterministic TUI capture engine (issue #19)

## Scope and inspected ownership

Add a standalone, standard-library-only Python capture utility. Its launch command, terminal size, markers, masks, and scenarios come entirely from JSON; it must not import or change `src/`, invoke models, or integrate with ADW/evidence generation. Each scenario gets a fresh tmux server. The example is project-specific; the engine is not.

Inspected `scripts/autoqueue.py`, `tests/test_autoqueue.py`, `justfile`, `README.md`, and `AGENTS.md`. Existing Python utility conventions are argparse, subprocess argument arrays, pathlib, explicit exit codes, and pytest through `uv run --no-project --with pytest`. `justfile` loads `.env` into recipes, making deliberate environment filtering especially important. Do not read credentials or `.env` files.

## Files to add/change

- **Add `scripts/tui_capture.py`**: CLI, full preflight validation, injected tmux runner, polling, isolated per-scene lifecycle, normalization, deterministic artifacts.
- **Add `scripts/tui_scenes.example.json`**: copy the issue's JSON example exactly in content, including launch string, `[100, 30]`, ready marker, timeout, three masks, and ordered `status`/`help` scenes.
- **Add `tests/test_tui_capture.py`**: offline pytest tests with a scripted fake tmux runner and fake clock; never launch tmux or Pi.
- **Change `justfile`**: add manual `tui-capture scenes out repo="."`, add `test-tui-capture`, and invoke only the latter from `test`.
- **Change `README.md`**: Chinese documentation for the manual capture command, outputs/configuration, dependencies, offline restrictions, test recipe, and human reproducibility verification.
- **Change `AGENTS.md`**: document this utility in the structure table and update the testing rule to include fake-runner capture tests; real capture stays outside factory tests and needs human verification.

No changes to existing test expectations, game behavior, ADW modules, dependencies, or unrelated documentation repairs.

## Contract and implementation choices

### CLI and validation

Expose `main(argv=None, ...) -> int`, with test seams for runner, monotonic clock, sleep, environment, and executable lookup (keyword injection or monkeypatchable small helpers are both acceptable). Use `raise SystemExit(main())` at the entry point. The production runner uses `subprocess.run` without Python `shell=True`, UTF-8 text output, and captured stdout/stderr; judge command success exclusively by return code.

Required flags: `--repo`, `--scenes`, `--out`. Resolve/expand the repo path, require an existing directory, and validate input and output path suitability. Use `shutil.which("tmux")` for preflight, but execute the bare `tmux` command. Do not require Pi globally: another scene file may launch a different TUI. Invalid arguments, unreadable/invalid JSON, invalid configuration, invalid output location, and missing tmux return 2 with a useful stderr diagnostic.

Validate the **entire** document and compile all regexes before creating a server or capture artifacts; an invalid later scene must prevent earlier scenes from running. Require:

- Top-level object with `launch`, `size`, `ready`, `timeout_seconds`, `masks`, `scenes` and their correct types. Reject unrecognized object keys to catch typos.
- Nonempty launch/ready strings; size is exactly two positive integers (not booleans); timeout is a finite positive number (not boolean; reject JSON NaN/infinity).
- `masks` is a list of objects containing string `pattern` and optional string `replace`, with valid regex syntax. Empty masks are valid. Use `re.MULTILINE` so the example's `$` can match a footer line within the captured screen.
- `scenes` is a nonempty list, each object having unique full-match `[a-z0-9_-]+` name and a list of steps. Empty steps are valid (capture the ready screen).
- Every step is an object with exactly one of `text`, `key`, `wait_for`, holding a string; key and wait marker must be nonempty. Allow empty literal text as a no-op. Reject unknown or multi-action steps and NUL characters in command/argument values before execution.

Simplest explicit replacement semantics: `replace` is a literal string replacing the whole regex match (not a backreference template). Document this. Do not invent implicit timings, scene dependencies, additional step types, or default project launch commands.

### Data flow and small functions

Keep the code in one module, organized into small helpers such as `load_scenes`, `pane_environment`, `normalize_screen`, `wait_for`, `capture_scene`, `run_scenes`, and `main`. Configuration can use dictionaries or small stdlib dataclasses; no framework is needed.

Data flow:

`CLI -> complete preflight/compiled config -> ordered scenes -> isolated launch -> ready polling -> ordered steps -> 0.3s settling -> final screen -> normalize -> UTF-8 scene file -> ordered manifest -> exit code`.

Pass dependencies into the orchestration rather than mocking away normalization or validation. The fake must see the same complete argv that subprocess would receive.

### tmux isolation and pane environment

For each scene:

1. Allocate a unique socket label (for example `tui-capture-<uuid hex>`) and a `TemporaryDirectory` containing a tmux config and a **separate initially empty** agent directory. Keep config outside the agent directory.
2. Write the config with exactly the required settings, each on its own line: `set -g extended-keys on` and `set -g extended-keys-format csi-u`.
3. Prefix every tmux invocation, including cleanup, with `tmux -L <socket> -u -f <config>`. Never use the default socket. Start a detached session with fixed session name (e.g. `capture`), explicit `-x <columns> -y <rows>` and `-c <absolute repo>`. Target `capture:0.0` explicitly for subsequent commands.
4. Pane command must begin `env -i`, followed by the allowlisted assignments and a non-interactive `sh -c <launch>`. Prefer tmux's multiple-command-argument direct-exec form so there is no user login shell before `env -i`; the launch remains a shell command string, allowing quoted arguments without unsafe interpolation. Do not source shell startup files. Preserve paths/text as individual arguments, including spaces and quotes.
5. Include only `PATH`, `HOME`, `TERM`, caller `LANG`/`LC_ALL`, plus the four required overrides. Supply sensible PATH/HOME/TERM fallbacks if absent (`os.defpath`, home directory, `screen-256color`). If neither locale variable exists, set `LANG=en_US.UTF-8`; otherwise preserve whichever locale variables exist. Always override `PI_CODING_AGENT_DIR` to the empty directory, `PI_OFFLINE=1`, `PI_SKIP_VERSION_CHECK=1`, and `PI_TELEMETRY=0`. Never forward arbitrary caller environment into the pane, including API keys, inherited Pi paths/settings, or `TMUX`.
6. Also give the tmux subprocess a filtered environment rather than inheriting secrets into the new server. tmux itself may manage its internal terminal variables; tests assert the explicit `env -i` assignment whitelist. This is isolation for trusted scene commands, not an OS sandbox against a malicious launch command accessing files under HOME.

### Polling, actions, errors, cleanup

- Capture the visible pane using `capture-pane -p -t capture:0.0`, without ANSI escapes or scrollback flags. Preserve returned whitespace and line endings; do not `.strip()` the screen.
- For startup ready and each wait_for, use a fresh monotonic deadline of `timeout_seconds`. Capture immediately, test for literal substring, then poll every 0.2 seconds until found or deadline reached. Sleep only between unsuccessful polls (bounded by remaining time). Inject clock/sleep so tests take no real time.
- `text`: `send-keys -t capture:0.0 -l -- <text>`; `key`: `send-keys -t capture:0.0 -- <key>`. Do not append Enter to literal text or try to validate tmux's complete key vocabulary in Python.
- After all steps, sleep exactly the requested 0.3 seconds once, then capture again. No other fixed startup/action delays.
- Retain the last successfully captured screen. Timeout errors identify ready versus step/wait marker and include the last screen. A nonzero tmux command result, OSError, or subprocess timeout is a scene failure, not a global abort. Bound subprocess calls so a stuck client cannot bypass polling indefinitely; a reasonable bound is the configured scene timeout, using remaining deadline for poll captures.
- Enclose the complete lifecycle, including launch, in `try/finally`: attempt `kill-server` on that unique socket on success, timeout, launch/send/capture failure, and interruption. Only then remove the temporary directory/config via its context manager. An already-exited server must not prevent local cleanup or erase the original scene error. Report other cleanup failures rather than silently claiming full success; continue subsequent scenes for ordinary scene failures.

### Normalization and reproducible outputs

First replace literal occurrences of the resolved absolute repo path and its `~/...` equivalent (only when actually under HOME) with `<repo>`. Use path-relative computation, not string prefix checks (HOME `/a/b` must not match `/a/bc`). Then apply regex masks in declaration order.

For masks without `replace`, map every matched character to `#`, or `##` for `unicodedata.east_asian_width(ch)` in W/F. Preserve newline separators rather than hashing them, so broad matches do not collapse rows. Preserve all unmatched characters, blank lines, trailing spaces, and the final newline. Explicit replacement and repo normalization are the requested exceptions to width preservation; do not perform extra trimming, filtering, or line removal. Masks should target content, not row separators; document this expectation.

For each configured name write `<name>.txt` in UTF-8. On failure write the normalized last screen (empty if nothing could be captured), so every manifest file reference exists and stale successful captures cannot masquerade as current failures. Do not delete unrelated output files. Capture-file write failures mark that scene failed and do not prevent attempts for remaining scenes; report manifest-write failure as run failure.

Always write `manifest.json` after ordinary scene processing, with deterministic JSON formatting (`ensure_ascii=False`, fixed indentation, final newline), scene order from input, and each entry having exactly `name`, `file`, `ok`, `error`. `file` is the relative `<name>.txt`; successful `error` is null; failed `error` is a string. Return 0 only if all scenes and artifact writes succeed, otherwise 1. Preflight failures return 2 and do no capture work.

Do not put elapsed times, timestamps, random sockets, temporary paths, or absolute output paths in artifacts. Use stable error summaries (operation, return code, marker, normalized last screen); detailed raw subprocess diagnostics may go to stderr rather than embedding random argv/temporary paths in manifest. Timeout last-screen content in errors must use the same normalization as files. Identical scripted inputs, including failures, must produce identical artifact bytes across runs despite unique runtime resources.

## Tests first

Create failing tests before implementation and record the failing command/exit status. Use pytest fixtures for temporary repo/home/output paths, configuration, fake clock, and a scripted callable runner returning subprocess-like results. The fake records argv and subprocess environment; during launch it can read config and check the empty agent directory. Patch executable discovery in all execution tests so tmux installation is irrelevant.

Required test coverage:

1. Normalization: individual digits; W/F characters including Chinese/fullwidth characters; literal explicit replacement; mask ordering; footer `$` matching within a multiline capture; absolute and home-relative repo spellings; paths outside HOME and with spaces/quotes; preserved blank lines/trailing spaces/line count.
2. Launch/argv: two scenes use distinct sockets and independent startup, all invocations carry isolation options, configured dimensions/cwd, both config lines, literal text versus key argv, and env -i with only permitted assignments. Seed a dummy `DEEPSEEK_API_KEY`, other credential variable, `TMUX`, and inherited Pi variables and prove they are not passed through. Test locale fallback and inherited locale cases.
3. Parsing/CLI: malformed JSON, missing fields, wrong types, bad size/timeout/regex, invalid and duplicate names, unknown/multi-action steps, invalid later scene, bad repo/output path, missing tmux, and missing CLI arguments yield 2 with no runner calls or screenshots. Assert the committed example parses and contains the issue's ordered scenes/settings.
4. Waiting: ready and step markers appearing on the Nth capture are accepted; exact text/key/wait ordering; final capture occurs after the 0.3-second settling call; unsuccessful polls use 0.2-second cadence; no unconditional startup delay.
5. Timeout: last screen appears in normalized error, failed scene writes last-screen file, next scene still runs, exit 1. Include ready timeout and step timeout, using fake time only.
6. Cleanup: kill-server uses the correct socket on success, timeout, nonzero launch/send/capture results, and exceptions; temporary config/agent directories are gone afterward; cleanup cannot mask original errors. A passing stdout containing `error` is still a success.
7. Artifacts: exact field set/types/order and relative filenames; successful exit 0; deterministic byte-for-byte screen and manifest output across two runs, including mixed failure/success and changing socket/temp names. Empty-screen failure must overwrite a preexisting same-name screenshot.

Do not weaken existing tests. No tests may run real tmux, Pi, network calls, or models.

## Recipes and documentation

- `tui-capture scenes out repo="."` runs `uv run scripts/tui_capture.py --repo ... --scenes ... --out ...`. Use positional shell arguments/quoted defaults consistently with existing `set positional-arguments` to preserve spaces and quotes. It is a **manual** recipe, not a dependency of `test`.
- `test-tui-capture` runs `uv run --no-project --with pytest pytest tests/test_tui_capture.py -q`; add it to `test` after the current suites.
- README Chinese section: show both the direct CLI and `just tui-capture scripts/tui_scenes.example.json <out> .`; explain per-scene text/manifest files, whitelist/empty Pi directory, configured masks and markers, exit codes 0/1/2, and that scene files are trusted launch commands. Require local tmux with extended-key support and the launched TUI (Pi for this example). No `/hint`, Bot turn, or settlement captures; status/help are model-free. Update offline-test listing with capture tests.
- AGENTS testing rule: fake-runner capture tests join `just test`; real `just tui-capture` remains human-only and is not factory acceptance evidence until actually run.

## Verification and acceptance

Builder should run the new test recipe for red/green evidence, then `uvx ruff check scripts/tui_capture.py tests/test_tui_capture.py`, `uvx ruff format --check scripts/tui_capture.py tests/test_tui_capture.py`, and **`just test`**. Resolve failures based on command exit status. Existing suites must continue passing unchanged. No actual capture or paid smoke command is authorized for the factory.

Document the outstanding human gate explicitly: on a machine with tmux and Pi, run `uv run scripts/tui_capture.py --repo . --scenes scripts/tui_scenes.example.json --out <fresh-dir>` three times to separate output directories, verify exit 0 and `status.txt`, `help.txt`, `manifest.json`, then compare all three sets byte-for-byte (e.g. `diff -r`). Check real status/help content and absence of extended-key warnings. This real-world determinism is not established by fake tests; do not claim it was verified by the builder.
