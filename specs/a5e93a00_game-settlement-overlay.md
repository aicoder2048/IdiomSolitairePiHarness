# Issue #11 — 对局结束结算画面

## Scope and acceptance

Add a player-only end-of-game summary when a completed Bot round returns `gameOver: true`, through either `submitBot` or `forfeitBot`. TUI gets a dismissible overlay; all other modes keep the final conversation card, now containing the same richer text. Include title, final score/verdict, one line per recorded round with both moves and earned scores, and the restart/extend-rounds instruction. Do not change scoring, round limits, termination, prompts, or engine behavior.

Acceptance: pure text unit tests cover Bot forfeits, passes and hints; TUI uses `ui.custom(..., { overlay: true })`; non-TUI uses `appendEntry`; each actual game-ending settlement presents exactly once; `just test` passes; README and the relevant engineering rule are updated.

## Recon and design decisions

- `src/extension/view.ts` already owns `finalLines`, `describeHumanMove`, and `describeBot`. Expand `finalLines` rather than introduce a second summary formatter.
- `src/extension/index.ts` has a shared `settle(res, ctx)` called by tool execution and the forfeiture helper. It currently appends a round card, optionally a final card, then refreshes the board. This is the only trigger to change; do not trigger from rendering, refresh, input, or checking `game.gameOver` elsewhere.
- Engine `finishRound` records the round, clears pending Bot state, increments the round number, and returns `gameOver`. Later submits are stale and repeated settlement events have no pending round. Reuse these guards; do not add a sticky `finalShown` flag that would suppress summaries after `/restart`, `/undo`, or `/rounds` continuation.
- `src/extension/panel.ts` already provides themed, terminal-width-safe `createPanel`. Reuse it, adding a small dismissible wrapper instead of changing the noninteractive base component or hint selector.
- `tests/extension/fake-pi.ts` already supports a mode constructor (default RPC), records `customCalls`, and exposes their factories and completion callbacks. No fake changes are expected.
- Display the scores already stored in `game.scores`, `record.human.gained`, and `record.botGained`; never recalculate historical points from current difficulty. “双方得分” means per-move earned points on each round line, plus final totals in the header, not additional cumulative columns.
- Keep ordinary round cards in every mode. A successful TUI overlay replaces only the final card; do not append a duplicate final card as well.
- The overlay is informational: open it without awaiting dismissal in the tool/event settlement path, so `terminate: true` and lifecycle processing do not depend on a keypress. Handle custom-UI exceptions/rejections inside the presentation helper and fall back once to the captured summary card on failure. This adds no model calls or messages.
- Use a centered, available-width overlay (`width: "100%"`, `margin: 1`) for the long round rows. Reuse `createPanel`'s clipping and footer wrapping; the hint-specific 60% width policy remains untouched. No scrolling, pagination, or terminal redesign is requested. All historical rounds must be present in the generated text, even when terminal clipping limits visible space.

## Files and implementation steps

### 1. Tests first

Add the tests below before implementation. Run the targeted extension suite to demonstrate failures from missing summary rows, dismissible component, and mode routing. Preserve existing tests unchanged except compatible additions to shared test helpers if genuinely needed.

### 2. `src/extension/view.ts`: shared pure summary

Expand `finalLines(game): string[]` with this order:

1. `🏁 对局结束`
2. Existing score and verdict wording, unchanged: `你 H : B Bot · <你赢了！🎉 / Bot 获胜。 / 平局。>`.
3. Map `game.roundLog` in recorded order, exactly one logical string per round: `第 N 轮：<describeHumanMove(record.human)> / <describeBot(record)>`.
4. Existing final instruction, unchanged: `输入 /restart 再来一局，或 /rounds 加轮数继续。`

Successful Bot descriptions already include their recorded score. For a failed Bot, append `（本轮 0 分）`, using `signed(record.botGained)` rather than a hard-coded score. Example: `第 2 轮：你跳过本轮（-1） / Bot 放弃：回合被中断（本轮 0 分）`. Do this only in the summary composition; do not change `describeBot` globally and thereby change existing status/round cards. Human descriptions already represent idiom, pass, timeout and hint scores correctly. No extra attempt-detail lines in the final summary.

The formatter must be side-effect free, use no Pi runtime APIs, and return a fresh array without altering logs, totals, timers, or hint allowance.

### 3. `src/extension/panel.ts`: dismissible panel wrapper

Export `createDismissiblePanel(content: PanelContent, done: () => void): Component` (or equivalently named wrapper).

- Delegate render/invalidate to `createPanel(content)` to preserve Chinese-width/ANSI-safe layout and existing theme/border styling.
- Add `handleInput` that calls `done()` for any input/key, without passing input through or changing game state.
- Guard closure so repeated input calls `done` at most once.
- Leave `createPanel` noninteractive and leave all hint-selector behavior and sizing intact.

### 4. `src/extension/index.ts`: mode-aware final presentation

Import the dismissible wrapper. Add a small presentation helper beside `card`, taking a captured `string[]` and the context:

- If `ctx.mode !== "tui"`, call `card(lines)` immediately and return. Do not depend on `hasUI`, widgets, or calling a component factory in non-TUI modes.
- Otherwise use `ctx.ui.custom<void>((tui, theme, keybindings, done) => component, { overlay: true, overlayOptions: { anchor: "center", width: "100%", margin: 1 } })` with default focus capture.
- Build `PanelContent` from exactly the supplied lines: title is the first line, body is `slice(1, -1)`, footer is the last line. This places the title once and keeps the continuation instruction at the end with existing footer wrapping. Do not rebuild the text from mutable game state inside the factory.
- Return the dismissible wrapper with a callback invoking `done()`.
- Catch synchronous custom-UI errors and asynchronous rejection so they cannot fail an already-accounted Bot round or produce an unhandled rejection. On failure append the captured final card once; do not retry the overlay.

In `settle`, retain the ordinary round card and board refresh. Replace `if (res.gameOver) card(view.finalLines(game))` with a call to this presenter on `view.finalLines(game)`. Invoke the asynchronous presentation without awaiting dismissal, while catching errors inside it. Do not modify the tool's returned round-end text, usage, `terminate` flag, nudges, or forfeiture routes.

No engine files, tool schemas, commands, or model-context paths need edits. Normal any-key dismissal has no other effect and does not generate a card or model message.

### 5. Documentation

- `README.md`: add a short Chinese “对局结算” section describing the automatic final summary, total score/verdict and all round moves/points (including passes, hints and Bot forfeits), any-key TUI dismissal, RPC/JSON/print final-card fallback, and `/restart` versus `/rounds <N>` to increase total rounds and continue. Clarify that viewing/closing the summary costs no extra model tokens.
- `AGENTS.md` rule 5: add the settlement overlay as another player-only exception to appendEntry-only display. State TUI-only custom overlay, any key closes, other modes use identical-text cards, and it triggers only on an actual final round result. Keep the existing hint rules unchanged.

## Detailed tests

### `tests/extension/view.test.ts`

Import `finalLines` and add:

- Exact ordered output for a completed game: title, totals/verdict, one row per log entry, final instruction. Test human-win, Bot-win, and draw wording (real FakeLLM-driven games or focused fixtures).
- A multi-round history containing an ordinary idiom, a pass, a successfully committed hint, and a Bot forfeit. Assert recorded round numbers, actual moves, “使用提示”, negative pass points, successful Bot points, forfeit reason and explicit zero Bot points. Include timeout formatting as a low-cost additional case.
- Missing forfeit reason uses the existing “没有给出合规成语” fallback when using a fixture without attempts.
- Historic earned points remain unchanged after switching difficulty; assert no recalculation.
- Repeated `finalLines` calls are identical and leave a snapshot of scores, chain, roundLog, round number, hint allowance and awaitingBot unchanged. Assert array length is `roundLog.length + 3`, so each round contributes only one logical line.

Prefer engine methods with FakeLLM/FakeClock to produce representative histories; use narrowly typed fixtures only for otherwise-unreachable presentation boundaries.

### `tests/extension/panel.test.ts`

- New wrapper renders the supplied summary title/body/footer using the existing panel.
- A normal printable key, Enter, Esc and an arrow each dismiss fresh component instances. Repeated input on one instance calls done only once.
- Rendering and invalidation alone do not dismiss; repeated render is stable.
- Long Chinese rows and narrow/zero widths remain safe, with every rendered row within its supplied display width (use `visibleWidth` and `stripTerminalSequences`, not JS string length). Existing passive-panel and hint-selector tests remain unchanged.

### `tests/extension/extension.test.ts`

Use the current FakePi and `/rounds 1` or `/rounds 2` to shorten games; use `setup({ mode })` for routing. Reuse the existing factory-invocation pattern from hint tests (fake terminal, fakeTheme, recorded done callback).

- Default fake RPC, explicit RPC, JSON and print: finishing a one-round game appends exactly the usual round card plus one final card with full shared summary text; no custom call. This must still work with `hasUI: false`.
- TUI success: final Bot submission invokes custom exactly once with `overlay: true`, creates no final card (ordinary round card remains), and still resolves with `terminate: true` before the overlay is dismissed. Invoke the captured factory, inspect render at sufficient width for title, score, round and footer, then press a key and assert recorded completion.
- Finishing a nonfinal round does not present a final overlay/card. Intermediate rejected attempts and the first nudge do not present one either.
- Exercise final forfeiture through retry exhaustion in `submit_idiom`, the no-tool second settle event, aborted/error settlement, and `agent_settled` fallback. Use a concise parameterized matrix across TUI and a non-TUI mode; verify exactly one final presentation and correct forfeit text/points.
- After a final result, repeated `agent_before_settle` and `agent_settled`, an extra stale tool submit, `/status`, and normal input do not show another summary. Count only final presentations, not all cards, since `/status` legitimately appends a card.
- After dismissing, `/rounds 2` permits another round and a second summary on its completion; `/restart` and `/undo` similarly permit a fresh ending. This verifies that “once” means once per final settlement, not once per extension lifetime.
- Summary presentation/dismissal adds no FakeLLM calls, `sendUserMessage` calls, or summary text in the tool result. Snapshot counts after expected gameplay judge calls; do not mistakenly count judging as summary usage.
- Synchronous custom throw and asynchronous rejection yield a single final-card fallback without changing the completed tool result or retrying the overlay.

Keep tests fully offline. No need to enhance `fake-pi.ts` unless a small reusable test helper proves necessary; its mode and custom recording already exist.

## Verification and completion checklist

1. Red phase: `bun test tests/extension/view.test.ts tests/extension/panel.test.ts tests/extension/extension.test.ts` after adding tests.
2. Green phase: rerun that command after implementation, then `just typecheck`.
3. Required final gate: `just test` (type checking, all Bun tests, factory tests, autoqueue tests). Judge every command by exit status; report any environment blocker accurately.
4. Review diff for unchanged engine rules, original hint behavior, no additional model messages, no duplicate final TUI card, no sticky suppression of later endings, and both documentation updates.
5. Do not run paid `just smoke`, access credentials, run `gh`, or change git history. The supplied issue is the complete scope.

Planning only: no implementation or validation commands were run while preparing this document.
