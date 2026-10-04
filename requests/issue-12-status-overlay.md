Implement GitHub issue #12: "/status 改为 overlay 详版面板" (https://github.com/aicoder2048/IdiomSolitairePiHarness/issues/12). The issue and its comments are quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a FEATURE — new behaviour, or existing behaviour made better:
- Plan before building: the plan names the files, the data flow and the tests, and the builder follows it.
- New behaviour comes with tests that describe it. Existing tests keep passing unchanged, unless the issue changes what they test.
- Document it in the same change: README.md (player-facing: how to play, commands) and AGENTS.md when it adds a rule.
- Where the issue leaves a choice open, take the simplest option that satisfies it and record the choice in the plan.

Where: the files the issue names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point under the issue's own "Done means" holds; tests cover the new behaviour; `just test` passes; README/docs describe what changed.
Out of scope: anything the issue does not ask for; redesigns of neighbouring code.

## Issue #12 as filed

## 背景
`/status` 现在把详细状态写成对话流里的卡片，每查一次就多一张，刷屏。

## 要做的
`/status` 在 TUI 里改用 overlay 显示，内容沿用 `view.statusLines()`，标题「📊 状态」。非 tui 模式保持卡片。

Overlay 用 `ctx.ui.custom(factory, { overlay: true })`，按任意键关闭（组件调用 `done()`）。只在 `ctx.mode === "tui"` 时用 overlay；其它模式（rpc/json/print，以及测试里的假 `ExtensionAPI`）退回现有的卡片（`pi.appendEntry`），所以离线测试测的是"tui 模式调用了 `ui.custom` 且 `overlay: true`，非 tui 模式写卡片"。`tests/extension/fake-pi.ts` 需要时可以加 `mode` 参数和 `ui.custom` 记录。如果 `src/extension/` 里已有通用的 overlay 面板助手，复用它；没有就新建一个（例如 `src/extension/panel.ts`：给定标题和文字行，返回可关闭的面板组件），文字宽度用 `@earendil-works/pi-tui` 的 `visibleWidth()` / `truncateToWidth()`。

## 验收标准
- tui 模式：调用 `ui.custom` 且 `overlay: true`，不再追加卡片；非 tui 模式：仍写卡片；
- 仍然 0 token，不发消息给模型（保留在「确定性命令 0 token」测试里）；
- `just test` 通过。

## 不做的
不改 `statusLines()` 的内容；不改 `/help`、`/chain`。

## Comments

(no comments)
