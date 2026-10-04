# Issue #12 — `/status` TUI overlay

## Goal and acceptance

Change only the presentation of `/status`: TUI opens a dismissible overlay titled `📊 状态`, using the unchanged `view.statusLines(game, piLLM?.totals)` body. Every non-TUI mode retains the existing `idiom-card` entry with that title and body. Opening/closing status must invoke no model and send no model message. `/help`, `/chain`, game rules, status content, and settlement behavior are outside scope. Deliver tests, README and engineering-rule updates, and a passing `just test`.

## Recon and files

- `src/extension/index.ts`: owns command registration, `card()`, and mode-specific UI. Currently registers status as a direct `card(view.statusLines(...), "📊 状态")` call. `presentFinal()` demonstrates the existing overlay sizing/factory pattern.
- `src/extension/panel.ts`: already exports `createDismissiblePanel`, `panelWidth`, and `PanelContent`. The component calls its completion callback on any key and guards against double completion. Width/rendering already use `visibleWidth()` / `truncateToWidth()`. Reuse these exports; no new panel module or component implementation is necessary.
- `src/extension/view.ts`: owns `statusLines()` and the existing status command metadata; leave unchanged.
- `tests/extension/fake-pi.ts`: already accepts `mode` (defaults to `rpc`), records `customCalls`, and supplies pending promises with `done`/`reject`. No fake changes needed.
- `tests/extension/extension.test.ts`: add status coverage and update the settlement regression that assumes `/status` cannot open an overlay. Existing `hintPanel(index, columns)`, `hintOptions()`, and `flush()` can drive custom factories despite their hint-specific names. Avoid unrelated helper renaming.
- `tests/extension/panel.test.ts`: existing tests cover arbitrary-key dismissal, once-only completion, narrow widths and Chinese text. Keep passing unchanged; test the status wiring at extension level.
- `README.md` and `AGENTS.md`: update player instructions and rule 5 respectively.

## Implementation and choices

1. Add a small async `presentStatus(lines: string[], ctx: ExtensionContext): Promise<void>` beside the display helpers in `index.ts`, and register status as `command("status", (_args, ctx) => presentStatus(view.statusLines(game, piLLM?.totals), ctx))`.
2. Branch strictly on `ctx.mode === "tui"`, not on `hasUI` or method availability. Otherwise immediately call `card(lines, "📊 状态")` and return. This includes rpc/json/print and the default fake, including non-TUI contexts without UI.
3. For TUI, await `ctx.ui.custom<void>(factory, { overlay: true, overlayOptions })`. Reuse `createDismissiblePanel` with title `📊 状态`, all supplied lines unchanged, the factory theme, and `() => done()`. Add the UI-only footer `按任意键关闭`; do not add it to `statusLines()` or non-TUI cards. No terminal-input listener, user message, appendEntry, model call, or game mutation belongs on this path.
4. Use the existing centered panel convention: `OverlayOptions` with `anchor: "center"`, `margin: 1`; compute width via `panelWidth(content, tui.terminal.columns)` and update width in `overlayOptions.visible(columns)` returning true, as `presentFinal()` does. This reuses Chinese-width-safe rendering and existing resizing behavior without modifying shared components. No scrolling/new layout behavior is requested.
5. The command promise resolves when the user dismisses the panel. Unlike final settlement, this command does not need fire-and-forget behavior to release a Bot tool. Keep settlement and hint lifecycle unchanged and retain the command wrapper's existing behavior.
6. On a synchronous throw or rejected custom promise, notify `状态面板显示失败，请重新 /status。` with severity `error` using existing `notify()`, then return. Do not append a TUI fallback card: the issue explicitly asks that TUI status stop adding transcript entries. This is a small local failure policy, not a change to settlement's fallback behavior.

Data flow: command → snapshot from unchanged `statusLines(game, piLLM?.totals)` → mode dispatch → existing card OR themed dismissible component → `done()` resolves UI/command only. No new state or engine dependency is needed.

## Tests first

Write/adjust tests before implementation and run the extension suite to observe failures by exit status.

### New status integration tests

- Parameterize non-TUI coverage over default fake, rpc, json and print. Assert exactly one appended `idiom-card` with title `📊 状态` and existing body, zero `customCalls`, zero fake LLM calls and zero user messages. Cover `hasUI: false` as well as the default `hasUI: true` so the routing cannot accidentally use that flag.
- TUI: start `const pending = pi.command("status")` without immediately awaiting it; flush, inspect the recorded custom call, instantiate its factory using the existing helper, send a key via `handleInput`, then await `pending`. Assert one custom call with `overlay: true`, no entries before or after dismissal, `completed` changes to true, and no LLM calls or user messages. Verify the rendered title and status body at a sufficiently wide render width to avoid truncation. Compare body lines against a non-TUI snapshot of the same deterministic game state, or `statusLines()` of an equivalently configured game; do not duplicate formatter logic.
- Assert centered width options and resize width bounded by terminal width, using existing panel conventions. The shared panel unit tests already establish detailed Unicode rendering behavior; do not rewrite those tests.
- Exercise a repeated open/dismiss cycle to prove status remains callable without accumulating cards. Include a configured/non-empty game state (e.g. one completed round), capture LLM/message counts before inspection, and assert they do not increase while status displays the current score/chain/round detail.
- Test custom display failure (throw and rejection) produces only the error notification, no card or model effects, and the command settles.
- Keep `/status` in the existing `确定性命令 0 token` test. Existing default-fake `/status 与 /help 写成卡片，不发给模型` remains valid and should keep its assertions. Add a TUI regression proving `/help` and `/chain` still append their normal cards and do not call custom.

### Required existing-test adaptation

The parameterized settlement test named `${mode} 末轮 ${route} 只结算一次，后续生命周期/提交/状态/输入不重复` currently awaits `/status` and expects only one total TUI custom call. Under the new behavior this would hang and the count would be wrong. Preserve its purpose:

- After the original settlement panel has been dismissed, start status without awaiting it in TUI, assert a second custom call, instantiate index 1, assert its title is `📊 状态` (not another settlement), dismiss it, and await the status command.
- Non-TUI continues awaiting status normally.
- Final assertions expect two total TUI custom calls (one settlement, one status), but still only one settlement presentation, zero extra model calls/messages, and the same non-TUI final-card count. Keep the route matrix and all lifecycle checks.

Do not weaken other tests or change game/settlement behavior to accommodate status.

## Documentation

- Add a short Chinese README section for viewing status: `/status` shows `📊 状态` in a TUI overlay, any key closes it, repeated checks no longer add cards; rpc/json/print still show a card; viewing/closing is 0 token and does not message the model. Explain that the detailed status content is unchanged. Do not change `/help` or `/chain` instructions except any strictly necessary clarification.
- Amend AGENTS.md rule 5: remove `/status` from the unconditional appendEntry examples and explicitly document its strict TUI-only `ui.custom(..., { overlay: true })` exception, arbitrary-key `done()` dismissal, non-TUI card fallback, and no model context/token effects. Preserve the hint and settlement rules and settlement's non-blocking requirement.

## Verification and delivery

1. Red/green targeted loop: `bun test tests/extension/extension.test.ts tests/extension/panel.test.ts tests/extension/view.test.ts`.
2. Run `just test` for TypeScript checking, all Bun tests, factory tests, and autoqueue tests. Judge commands by exit status. No paid `just smoke`, GitHub commands, secret reads, or dependency/toolchain changes.
3. Review changes for scope: implementation only in extension presentation; formatter, engine, hints, help, chain, and final-settlement runtime untouched; tests cover both mode paths and documentation matches them.
4. Builder reports the actual verification results. This planning phase only writes this plan and its spec copy; it does not implement or claim tests have run.
