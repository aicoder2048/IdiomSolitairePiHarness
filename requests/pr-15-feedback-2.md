Address review feedback on pull request #15: "/hint 的候选改为 overlay 显示" (https://github.com/aicoder2048/IdiomSolitairePiHarness/pull/15). The factory opened it; you are on its branch, and its earlier commits are the factory's own plan (under specs/), code and write-up. The feedback is quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a REVISION of work under review:
- Address every point below. Where a point is a question, or you think the change would be wrong, change nothing for it and answer it in your report's summary: the reply to the reviewer is built from that summary.
- Change only what the feedback asks for. Existing tests keep passing; feedback that changes behaviour comes with tests that describe it.
- An inline point names its file and line; read the code around it before editing.

Where: the files the feedback names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point below is either handled in code or answered in the report; `just test` passes.
Out of scope: anything the feedback does not ask for, including cleanups the reviewer did not mention.

## Pull request description

Closes #10

Built by SSSF run `1e8f421e` (adw_issue, kind: feature) from `requests/issue-10-hint-overlay.md`. Plan, code and write-up are its three commits.

## Feedback since the factory's last reply

### 1. @aicoder2048 · comment

还需要改进:
1. /hint 的overlay 浮窗宽度太窄
2. 浮窗出现后, 应该能够让我用上下键选择用哪个候选成语, 或者输入数字选择用哪个候选成语, 而不是帮我选择. 我选择好了, 就回车关闭当前Overlay浮窗. 这个浮窗应该是blocking的直到用户做了选择. 而不是系统自动帮我选第一个.

### 2. @aicoder2048 · comment

补充说明（对上一条评论的澄清与新规则，以本条为准）

现在的 `/hint` 规则是「给候选参考、我本轮 0 分、由 Bot 自己出词」，并不是系统替我选了第一个，只是 Bot 常常出了同一个词。改成下面的新规则：

**1. 选择框（浮层）**
- 宽度至少 40 列（仍不超过 60% 屏宽），沿用上一轮的圆角边框、标题、居中、主题背景。
- blocking 的选择框：↑↓ 移动高亮，数字键 1–N 直接选中，回车确认；Esc 取消。底部说明行改为「↑↓/数字选择 · 回车确认 · Esc 取消 · 剩余提示 N 次」。
- 选择框需要键盘焦点，不再用 `nonCapturing`；选完或取消即关闭。

**2. 选中的候选 = 我本轮的出词，正常计分**
- 入账前走与手打作答**完全相同**的 Verifier（人类当前难度的规则与词库）：原字 2 分、谐音 1 分，再乘难度倍率；之后照常由 Bot 接这个词的末字。
- 若裁判判它无效：提示原因，回到选择框让我另选或取消，**不消耗**提示次数。
- 倒计时规则不变：超时后作答仍按跳过处理。

**3. 提示次数按难度限制（每局）**

| 难度 | 每局提示次数 |
| :-- | --: |
| extreme（极限） | 0 |
| hard（困难） | 1 |
| normal（普通） | 2 |
| easy（简单） | 3 |

- 只有确认选中并入账才消耗 1 次；Esc 取消、裁判判无效都不消耗。
- 次数用完（或极限模式）时 `/hint` 直接提示「本局提示次数已用完」，**不调用提示模型**（0 token）。
- `/undo` 撤销一整轮时，这一轮用掉的提示次数一并退回（放进快照）；`/restart` 重置次数。
- 中途 `/difficulty` 换难度：剩余次数 = 新难度上限 − 本局已用次数，最少 0。
- 仪表盘和 `/status` 显示剩余提示次数；`/help` 的说明和规则文字同步更新。

**4. 代码位置**
- 规则与计数放在引擎 `src/engine/game.ts`：例如 `hint()` 只负责检查次数并返回候选（不再开回合），新增「用提示词出词」的方法（走 Verifier、计分、扣次数、开 Bot 回合）；次数上限放进 `MODE_CONFIGS` 或旁边的常量表。
- 选择框组件放在 `src/extension/`（可在 `panel.ts` 的通用面板基础上加选择能力），非 tui 模式下退回：写一张带编号的候选卡片，并提示「输入候选编号或直接输入成语」。

**5. 测试**
- 引擎：各难度的次数上限；用完后 `/hint` 不调用模型；选中后计分与手打一致（原字 2、谐音 1、乘倍率）；裁判判无效不扣次数；取消不扣次数；`/undo` 退回次数；`/restart` 重置；中途换难度的剩余次数。
- 扩展：↑↓、数字键、回车、Esc 的处理；选中后 Bot 接的是候选的末字；选择框渲染宽度 ≥ 40 列且每行宽度一致。
