Implement GitHub issue #10: "/hint 的候选改为 overlay 显示" (https://github.com/aicoder2048/IdiomSolitairePiHarness/issues/10). The issue and its comments are quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a FEATURE — new behaviour, or existing behaviour made better:
- Plan before building: the plan names the files, the data flow and the tests, and the builder follows it.
- New behaviour comes with tests that describe it. Existing tests keep passing unchanged, unless the issue changes what they test.
- Document it in the same change: README.md (player-facing: how to play, commands) and AGENTS.md when it adds a rule.
- Where the issue leaves a choice open, take the simplest option that satisfies it and record the choice in the plan.

Where: the files the issue names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point under the issue's own "Done means" holds; tests cover the new behaviour; `just test` passes; README/docs describe what changed.
Out of scope: anything the issue does not ask for; redesigns of neighbouring code.

## Issue #10 as filed

## 背景
`/hint` 现在把候选写成对话流里的一张卡片，和回合卡片混在一起，不够醒目。

## 要做的
`/hint` 拿到候选后，在 TUI 里用 overlay 显示：标题「💡 提示」，逐行列出候选成语，末行写「本轮 0 分，Bot 接龙中…」。其余行为不变：照常开新回合、把回合 prompt 发给 Bot、本轮 0 分。

Overlay 用 `ctx.ui.custom(factory, { overlay: true })`，按任意键关闭（组件调用 `done()`）。只在 `ctx.mode === "tui"` 时用 overlay；其它模式（rpc/json/print，以及测试里的假 `ExtensionAPI`）退回现有的卡片（`pi.appendEntry`），所以离线测试测的是"tui 模式调用了 `ui.custom` 且 `overlay: true`，非 tui 模式写卡片"。`tests/extension/fake-pi.ts` 需要时可以加 `mode` 参数和 `ui.custom` 记录。如果 `src/extension/` 里已有通用的 overlay 面板助手，复用它；没有就新建一个（例如 `src/extension/panel.ts`：给定标题和文字行，返回可关闭的面板组件），文字宽度用 `@earendil-works/pi-tui` 的 `visibleWidth()` / `truncateToWidth()`。

## 验收标准
- tui 模式：调用 `ui.custom` 且 `overlay: true`；非 tui 模式：仍写卡片，内容与现在一致；
- `/hint` 仍然只调用一次提示模型，Bot 回合照常开始（`sendUserMessage` 被调用一次）；
- `just test` 通过。

## 不做的
不改提示的生成和过滤逻辑；不改其它命令。

## Comments

(no comments)
