Implement GitHub issue #1: "新增 /chain 命令：以卡片列出完整接龙链" (https://github.com/aicoder2048/IdiomSolitairePiHarness/issues/1). The issue is quoted in full at the end of this request; `gh issue view 1 --comments` shows the same.

This is a FEATURE — new behaviour, or existing behaviour made better:
- Plan before building: the plan names the files, the data flow and the tests, and the builder follows it.
- New behaviour comes with tests that describe it. Existing tests keep passing unchanged, unless the issue changes what they test.
- Document it in the same change: README.md, and the cookbook under docs/tech-papers/ when the feature has a recipe.
- Where the issue leaves a choice open, take the simplest option that satisfies it and record the choice in the plan.

Where: the files the issue names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point under the issue's own "Done means" holds; tests cover the new behaviour; `uv run pytest`, `just test-extensions` and `just test-adws` pass; README/docs describe what changed.
Out of scope: anything the issue does not ask for; redesigns of neighbouring code.

## Issue #1 as filed

## 背景
仪表盘只显示接龙链的最后 6 个成语，`/status` 把链挤在一行里。玩家想回看整局时没有好用的入口。

## 要做的
新增斜杠命令 `/chain`：在对话流里写一张卡片（`pi.appendEntry`，与 `/status` 同一种卡片），按顺序逐行列出本局完整接龙链，每行包含：序号、谁出的（你 / Bot）、成语、这一步的得分（带正负号）。链为空时卡片写「还没有成语」。

## 验收标准
- `/chain` 登记在 `src/extension/view.ts` 的 `COMMANDS` 里，`/help` 自动列出它
- 不调用模型（0 token），不发消息给模型（`sendUserMessage` 不被调用）
- 展示逻辑是 `view.ts` 里的纯函数，有单元测试；`tests/extension/extension.test.ts` 有 `/chain` 的测试，并加入「确定性命令 0 token」那条测试的命令列表
- `just test` 全部通过

## 不做的
不改仪表盘、不改 `/status`。

## Comments

(no comments)
