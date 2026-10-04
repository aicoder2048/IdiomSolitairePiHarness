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

实测截图：浮层"没有设计"，位置、背景、层次、交互都是原生默认，需要重做。具体问题与要求：

**1. 位置（现在：没传 overlayOptions，浮层从对话中间某一列开始，压在第 3 轮卡片的「+2」上）**
- 显式传 `overlayOptions`：`anchor: "center"`，`width` 取「内容最宽行 + 边框 + 左右各 1 格内边距」，下限 28 列、上限 `"60%"`，`margin: 1`，`maxHeight: "50%"`。
- 不能盖住底部的仪表盘和输入框。

**2. 外观（现在：没有边框，背景只在有字的地方，右侧一大块透明，看起来像漏绘）**
- 圆角边框 `╭─╮ │ ╰─╯`，用主题的 border/accent 色；标题「💡 提示」嵌在上边框里，加粗、accent 色。
- 每一行都铺满整块面板宽度的不透明背景（`theme.bg("customMessageBg", …)`，不足宽度的行用空格补齐），不能出现透明缝隙。
- 内容分三段：候选成语编号列出（`1. 舛讹百出`）；一条分隔线；底部一行用 muted/dim 色写「本轮 0 分 · Bot 接龙中」。
- 颜色全部取自 `theme`，不硬编码，亮色/暗色主题都要能看。
- 宽度一律用 `visibleWidth()` / `truncateToWidth()` 计算（中文与 emoji 是双宽），超长行截断加「…」。

**3. 交互（现在：浮层抢走键盘焦点，玩家下一次按键被吞掉，只用来关浮层）**
- 用 `nonCapturing: true`，不抢焦点，玩家可以照常输入。
- 自动关闭：玩家下一次提交输入或执行任何命令时关闭；最多显示 30 秒。用 `ui.custom` 给的 `done` 关闭，不要用 `OverlayHandle.hide()`。
- 关闭失败或显示失败都不能影响对局。

**4. 复用**
- `panel.ts` 做成通用面板：标题 + 正文行 + 可选的底部说明 + 主题。#11（结算画面）和 #12（`/status`）会直接复用，所以接口要能覆盖这两种用法。

**5. 测试**
- `panel.test.ts`：所有渲染行的 `visibleWidth` 相同，且等于面板宽度；首行、末行是边框；标题在上边框里；候选有编号；有分隔线和底部说明；超长中文行被截断并带「…」；窄终端下宽度不超过上限。
- `extension.test.ts`：tui 模式下 `ui.custom` 收到的 `overlayOptions` 含 `anchor`、`width`、`nonCapturing: true`；下一次 `input` 事件或命令之后面板被关闭。

视觉效果离线测试测不出来，改完我会在 `just play` 里实测截图复验。
