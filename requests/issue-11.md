Implement GitHub issue #11: "对局结束时显示结算画面" (https://github.com/aicoder2048/IdiomSolitairePiHarness/issues/11). The issue and its comments are quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a FEATURE — new behaviour, or existing behaviour made better:
- Plan before building: the plan names the files, the data flow and the tests, and the builder follows it.
- New behaviour comes with tests that describe it. Existing tests keep passing unchanged, unless the issue changes what they test.
- Document it in the same change: README.md (player-facing: how to play, commands) and AGENTS.md when it adds a rule.
- Where the issue leaves a choice open, take the simplest option that satisfies it and record the choice in the plan.

Where: the files the issue names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point under the issue's own "Done means" holds; tests cover the new behaviour; `just test` passes; README/docs describe what changed.
Out of scope: anything the issue does not ask for; redesigns of neighbouring code.

## Issue #11 as filed

## 背景
最后一轮结算后，现在只在对话流里追加一张「🏁 对局结束」卡片，信息少。

## 要做的
对局结束（`submitBot` / `forfeitBot` 返回 `gameOver: true`）时，在 TUI 里弹出 overlay 结算画面：
- 标题「🏁 对局结束」；
- 比分与胜负（沿用 `view.finalLines()` 的措辞）；
- 每一轮一行：轮次、你这一步、Bot 这一步、双方得分（可复用 `view.describeHumanMove()` / `describeBot()`）；
- 末行提示「/restart 再来一局，或 /rounds 加轮数继续」。

结算画面的文字由 `view.ts` 里的纯函数生成并有单元测试。非 tui 模式保持现在的终局卡片，但内容换成同一组文字行。

Overlay 用 `ctx.ui.custom(factory, { overlay: true })`，按任意键关闭（组件调用 `done()`）。只在 `ctx.mode === "tui"` 时用 overlay；其它模式（rpc/json/print，以及测试里的假 `ExtensionAPI`）退回现有的卡片（`pi.appendEntry`），所以离线测试测的是"tui 模式调用了 `ui.custom` 且 `overlay: true`，非 tui 模式写卡片"。`tests/extension/fake-pi.ts` 需要时可以加 `mode` 参数和 `ui.custom` 记录。如果 `src/extension/` 里已有通用的 overlay 面板助手，复用它；没有就新建一个（例如 `src/extension/panel.ts`：给定标题和文字行，返回可关闭的面板组件），文字宽度用 `@earendil-works/pi-tui` 的 `visibleWidth()` / `truncateToWidth()`。

## 验收标准
- 纯函数有单元测试（含 Bot 放弃的轮次、跳过和提示的轮次）；
- tui 模式弹 overlay，非 tui 模式写卡片；
- 只在对局结束那一刻触发一次；
- `just test` 通过。

## 不做的
不改计分、轮次和终止条件。

## Comments

(no comments)
