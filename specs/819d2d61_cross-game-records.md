# Issue #13 — 跨局战绩与 `/records`

## Goal and scope

Persist completed games locally, replace a game's result when it is completed again after undo, and expose a Chinese, player-only `/records` card with lifetime statistics and the latest ten results. File failures must never break gameplay. No leaderboard, multiplayer, upload, model calls, new dependencies, or neighbouring UI redesign.

## Existing ownership and integration points

- `src/extension/index.ts`: owns the live `IdiomGame`, session creation, `/restart`, tool execution, command registration, and player-only `card()` / `notify()` helpers. Its synchronous `settle()` receives every actual completed round, including successful Bot submissions, exhausted retries, and all forfeit lifecycle routes. `res.gameOver` currently triggers nonblocking final presentation.
- `src/engine/game.ts`: owns scores, `mode`, `roundLog`, `winner()`, undo and round limits. `restart()` can fail or return busy; only `kind: "command"` means it succeeded. Undo restores game state, not extension state. `setRounds()` can end an idle game by lowering the limit to the number already played, or reopen a completed game by raising it.
- `src/extension/view.ts`: pure formatting and the shared `COMMANDS` table used by help and registration.
- `tests/extension/extension.test.ts`: the only existing test suite constructing the extension; many existing final-settlement tests will now write records unless their common fixture is isolated. FakePi already records cards, notifications, model messages, and custom UI calls.

## Explicit design choices

1. JSON is an array of records, not JSONL or a versioned database envelope. Each record has:
   ```ts
   interface GameRecord {
     id: string;
     endedAt: string; // new Date().toISOString(): UTC completion time
     mode: Mode;
     rounds: number; // actual completed roundLog.length
     scores: { human: number; bot: number };
     winner: "human" | "bot" | "draw";
   }
   ```
   The winner is from the player's perspective in presentation (胜 / 负 / 平). Store the difficulty in force at completion; do not invent mixed-difficulty history or recompute scores.
2. Maintain a UUID in the extension closure, generated with `randomUUID` from `node:crypto` whenever the game is created and on successful restart. Session-start replacement also gets a fresh UUID. Failed/busy restart, undo, round-limit changes and difficulty changes keep the ID. No engine changes or filesystem imports in the engine are needed.
3. Upsert by ID: replace the full existing row, including completion time, or append a new row. Undo leaves the last completed result on disk until that same game finishes again; abandoning/restarting an incomplete game does not write an unfinished result. Increasing rounds and finishing again replaces the same ID too.
4. Statistics include every stored game, not just the ten displayed. Win rate is human wins / total games, draws included in the denominator; zero games means zero, never NaN. Display percentage with one decimal place. Latest results are ordered by completion timestamp descending using a copied array, then limited to ten. Dates displayed as UTC `YYYY-MM-DD`, Chinese mode labels, `你 H : B Bot`, and 胜/负/平. Equal timestamps may retain stable input order.
5. Missing file (`ENOENT`) means an empty history and no warning. Other read errors, invalid JSON, or invalid record structure are failures, not empty history. Never overwrite malformed history with a fresh array. On a failed `/records` read, notify warning and do not append a misleading empty-history card. On failed saving, notify warning and leave the game settled and playable; no automatic retry subsystem.
6. Use small synchronous Node filesystem functions in a dedicated extension module. This keeps the existing synchronous settlement and lifecycle signatures intact, avoids fire-and-forget writes and same-process read/write races, and ensures a following `/records` sees the result. No cross-process locking or crash-recovery system is requested. Reading the complete array and rewriting it after an upsert is sufficient for this local feature.
7. Record actual final settlements in `settle()` independently of display. Also cover the existing `/rounds` edge: after a successful change that transitions an idle, previously unfinished game to `gameOver`, persist it. Do not record a still-pending Bot round. Leave the existing final-overlay rule unchanged: only actual final-round settlement opens that overlay.

## Files and changes

### 1. New `src/engine/records.ts`: pure data operations

- Export `GameRecord` and a summary type using type-only imports from the existing game module where appropriate.
- Export `summarizeRecords(records)` returning total, wins, losses, draws and a numeric win-rate ratio (0..1).
- Export `upsertRecord(records, record)` returning a new array, with replacement by ID and no mutation of the inputs.
- Keep clock reads, UUID generation, environment access, filesystem IO and Pi imports outside this file. JSON shape validation can live in the extension storage module because it is an IO boundary, while statistics remain pure.

### 2. New `src/extension/records-store.ts`: local storage

- Export a path resolver with injectable arguments/defaults such as `recordsFilePath(env = process.env, home = homedir())`. Use a nonempty `IDIOM_RECORDS_FILE` verbatim; otherwise `join(home, ".pi", "agent", "idiom-solitaire", "records.json")`. Relative override paths are relative to the process working directory. Do not access a file or capture environment values at import time. Shell users can quote an absolute path or use `$HOME`; no custom tilde-expansion feature is necessary.
- Export synchronous `readRecords(path = recordsFilePath())` and `saveRecord(record, path = recordsFilePath())`.
- Reading: UTF-8 parse, return `[]` only for `ENOENT`, and validate the array and each row before returning. Require a nonempty ID, ISO timestamp, known mode/winner, positive integral completed-round count, and finite numeric scores. Reject inconsistent winner/score combinations and duplicate IDs as malformed rather than silently producing incorrect totals. Unknown extra fields need not be rejected.
- Saving: read/validate first, pure upsert, create the parent using recursive `mkdirSync`, and write a pretty-printed JSON array plus newline. Propagate failures to the extension boundary; do not notify or swallow failures inside storage, and never proceed to a write after a read/validation failure.
- Use standard `node:fs`, `node:path`, `node:os` APIs; no new package.

### 3. `src/extension/view.ts`: command table and card formatting

- Add `records: ["", "查看跨局战绩"]` to `COMMANDS`.
- Add pure `recordsLines(records: readonly GameRecord[]): string[]`, using the pure summary helper.
- Empty history returns exactly `["还没有战绩"]`.
- Nonempty history returns a totals line (总场次、胜、负、平), a `胜率：…%` line, a `最近 10 局：` heading, and up to ten rows containing the UTC date, Chinese difficulty label, both scores and verdict. Do not mutate records while sorting. Keep ID and full timestamps out of the player card.
- The card title at registration will be `📚 战绩`; no overlay, including in TUI. The existing card renderer already handles display.

### 4. `src/extension/index.ts`: lifecycle and command wiring

- Add extension-local game ID state beside `game`. Pair every new game creation/session replacement with a new ID.
- Add a small `persistCompletedGame(ctx)` helper that snapshots `{ id, endedAt, mode, rounds: game.roundLog.length, scores: { ...game.scores }, winner: game.winner() }` and calls storage in try/catch. Use wall-clock `new Date()`, **not** `options.clock`, which is a monotonic game timer in seconds. Guard against incomplete/pending/zero-round state if called from commands.
- Catch persistence errors and call the existing `notify(ctx, "战绩保存失败，游戏可继续。…", "warning")`. Preserve existing no-UI notification convention; persistence itself must run in all modes and regardless of `hasUI`.
- In `settle`, when `res.gameOver` is true, save the record as well as calling the existing `void presentFinal(...)`. An IO error cannot bypass refresh, prevent `terminate: true`, or interfere with final UI. Do not wait for a final overlay to close. Ordinary rounds, rejected/stale tool calls, repeated lifecycle callbacks, status and other viewing commands must not write records.
- Change `/restart` from a one-line handler: call `game.restart(args)`, regenerate the ID only for a successful command outcome, then preserve existing report behaviour.
- In `/rounds`, capture prior `gameOver`, call `setRounds`, report as before, and persist only the successful nonterminal-to-terminal idle transition described above. Raising the limit preserves identity and writes nothing until the next finish.
- Register `/records` through the existing command helper: read storage, format, `card(lines, "📚 战绩")`; catch and warn on read failure. Do not call an LLM, sendUserMessage, custom UI or modify game accounting. Existing `appendEntry` keeps records out of model context.

### 5. Tests (write failing tests before production changes)

**New `tests/engine/records.test.ts`**
- Empty summary; mixed human wins, Bot wins, draws including negative scores; denominator includes draws.
- Upsert appends a new ID, replaces the matching ID without increasing count, preserves unrelated rows, and leaves all inputs unchanged.

**New `tests/extension/records-store.test.ts`**
- Every IO test uses `mkdtempSync(join(tmpdir(), ...))` and an explicit path or a temporarily set `IDIOM_RECORDS_FILE`, with teardown restoring environment and recursively removing the temporary directory.
- Resolve default path with an injected fake home (pure string assertion only); assert env override wins. Never read or write the real home, even to test defaults.
- Missing file reads empty without creating it; first save recursively creates nested directories and writes a parseable row; subsequent different ID appends; same ID replaces while retaining other rows.
- Malformed JSON and syntactically valid but invalid schemas throw; failed save preserves the original corrupt bytes. Cover unknown mode/winner and bad timestamp/score fields.
- Deterministic filesystem failure using a regular file as the would-be parent or a directory at the records-file path. If explicitly testing EACCES, use an isolated mock restored in finally rather than platform/root-sensitive chmod-only assertions.

**`tests/extension/view.test.ts`**
- Empty exact text; totals, all outcomes, translated difficulty, negative/positive score values and one-decimal percentage.
- At least 12 deliberately unsorted fixtures: only latest ten display, newest first, but all twelve count toward summary; records are not mutated. Fixed ISO fixtures make date assertions timezone-independent.
- Include `/records` in the existing help command expectation.

**`tests/extension/extension.test.ts`**
- First update the common beforeEach/afterEach fixture to set `IDIOM_RECORDS_FILE` to a fresh temporary nested path **before** `setup()`. Shutdown before removing files, restore the original variable (delete if originally absent), and clean up even after failures. Calls to `setup()` inside a test must reuse that test's directory so persistence across extension instances can be tested. Do not run environment-mutating tests concurrently. Keep all current behaviour assertions intact.
- Add `/records` to the existing deterministic-command 0-token test.
- Complete a one-round draw via FakePi: no file before completion; after submit returns, assert one row with nonempty ID, valid ISO completion timestamp, normal mode, one round, 2:2 and draw. A second setup/session can view that same persisted history.
- Undo the finished round, replay with a different outcome (e.g. Bot forfeit), and assert same ID, one row, updated score/winner. Repeated lifecycle/stale calls do not rewrite its timestamp or add rows.
- Restart and finish another game: second row and different ID, old row preserved. Invalid/busy restart keeps the current ID, verified by subsequent same-game recompletion rather than exposing private state.
- Raise rounds after completion and finish again: same ID with updated total rounds; lower an idle unfinished game's limit to played rounds: record that completion without introducing a final overlay. A pending Bot round must not be prematurely saved by `/rounds`.
- Extend existing final-route coverage with disk assertions for success, retries, no-tool, abort, error and agent_settled fallback. Normal rounds/rejected attempts/nudges do not save. Persistence happens with `hasUI = false` too.
- `/records` with missing history appends the exact empty text and title. Populated history appends expected summary and lines. Test TUI and non-TUI at least once: cards only, no custom panel, unchanged model call/message counts and board state. Repeated view must not modify the file.
- Corrupt file: `/records` resolves with warning, no fabricated empty card, and no model usage. Finishing a game also warns, preserves corrupt content, still returns terminate and final presentation; restart/new round still works. Repeat a representative write-failure case using an invalid temporary parent path; errors never escape lifecycle/tool handlers.

### 6. Documentation

- `README.md`: add a player-facing 跨局战绩 section near 对局结算: `/records` is 0 token and always a card; summary/latest ten, human-perspective rate formula, default path and `IDIOM_RECORDS_FILE` override example, local-only storage, auto-directory creation, successful restart starts a new record identity, undo/replay and continued rounds overwrite the previous result, and read/write failures warn without stopping play. Explain the last completed result remains visible until recompletion and difficulty is captured at completion.
- `AGENTS.md`: add a concise rule for cross-game storage: IO only in extension, pure statistics/formatting, stable ID through undo/continued rounds and fresh ID on new game/successful restart, upsert only on completion, player-only 0-token `/records`, warning isolation, and mandatory temp-file env isolation in tests. Do not change existing final-overlay semantics.
- Do not read/write `.env` files or credential files. Document overrides in README instead.

## Implementation and verification sequence

1. Add isolated fixtures and failing model/storage/view/integration tests.
2. Implement pure record operations, storage, formatting, lifecycle wiring and command registration in that order, making focused tests pass.
3. Update README and AGENTS as part of the same feature.
4. Run `bun test tests/engine/records.test.ts tests/extension/records-store.test.ts tests/extension/view.test.ts tests/extension/extension.test.ts`.
5. Run `just test` (typecheck, all Bun tests, factory tests, autoqueue tests). Judge commands by exit status. Do not run paid `just smoke` or use `gh`.
6. Inspect the change for accidental real-home access, model calls/context messages, altered overlay behaviour, or unrelated changes. All five issue acceptance scenarios—recording, overwrite, statistics, empty history and corrupt file—must have direct tests.

This is a plan only; no implementation or test run has been performed by the planner.
