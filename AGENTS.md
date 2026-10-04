# AGENTS.md — 成语接龙 · Pi Harness 的工程规则

本文件是给人和工厂 agent（planner / builder / reviewer / documenter）共同遵守的规则。设计背景见 `docs/agentic-engineering-paper.md`（Python 原版的四层工程与两个循环），Pi 文档见 `docs/pi-docs/`。

## 结构

| 路径 | 内容 |
| :-- | :-- |
| `src/engine/` | 纯游戏引擎（TypeScript）：规则、Prompt、Verifier、接龙链、对局状态机。不 import 任何 Pi 包 |
| `src/extension/` | Pi extension：`input` 拦截、`submit_idiom` 工具、`context` 裁剪、命令、仪表盘与卡片 |
| `tests/engine/`、`tests/extension/` | bun 测试；胶水层用 `tests/extension/fake-pi.ts` 的假 `ExtensionAPI` 驱动 |
| `scripts/smoke.ts` | 联网冒烟（RPC 模式真打两回合） |
| `adws/`、`scripts/autoqueue.py` | SSSF 软件工厂（Python），来源与本地补丁见 `.claude/skills/sssf/UPSTREAM.md` |

## 规则

1. **测试**：`just test` = 类型检查 + `bun test` + 工厂测试 + autoqueue 测试，全部离线。`just smoke` 会调用 DeepSeek（按量计费），工厂不跑它。先写失败的测试再实现，行为改动必须带测试。
2. **引擎纯净**：`src/engine/` 只依赖 `pinyin-pro`；凡是 import `@earendil-works/*` 的代码都放在 `src/extension/`。
3. **能用代码判定的不交给模型**：首字、谐音、长度、判重、计分、轮次都由引擎决定；模型只回答「是不是成语」（裁判）和提议候选（Bot）。
4. **模型只提议，代码写账**：Bot 只能经 `submit_idiom` 提交；写账只发生在 `input` 处理器、命令和工具的 `execute()` 里。
5. **Bot 的视野只到本回合**：`context` 事件只保留最后一条 user 消息之后的内容，失败尝试不得进入下一回合。给人看的内容（`/help`、回合卡片）用 `pi.appendEntry()`，不发给模型。例外：`/status` 仅在 `ctx.mode === "tui"` 时用 `ui.custom(..., { overlay: true })` 显示「📊 状态」，沿用 `statusLines()` 内容，按任意键由组件调用 `done()` 关闭，不追加卡片；其它模式仍用 `appendEntry` 卡片。查看和关闭不进模型上下文、不消耗 token。`/hint` 候选仅在 `ctx.mode === "tui"` 时用捕获焦点的 `ui.custom(..., { overlay: true })` 选择框，↑↓/数字选择、回车确认、Esc 取消；其它模式用 `appendEntry` 编号卡片并等待编号或成语输入。选择框不进模型上下文，等待确认后经人类 Verifier 正常计分并开 Bot 回合；提示限额和扣次由引擎负责，取消或无效不扣次数。终局结算是另一例外：只在实际末轮结算结果 `gameOver: true` 时触发一次，TUI 用 `ui.custom(..., { overlay: true })` 显示并按任意键关闭，其它模式用相同文字的 `appendEntry` 卡片；不进模型上下文，不等待关闭才结束 Bot 工具。
6. **斜杠命令**：除 `/hint` 外都不调用模型。新增命令要登记在 `src/extension/view.ts` 的 `COMMANDS`（注册与 `/help` 共用这张表），并在 `tests/extension/extension.test.ts` 里断言它 0 token。避开 Pi 内置命令名（如 `/model`、`/new`、`/quit`）。
7. **工具参数顶层必须是 object**：DeepSeek 会以 400 拒绝顶层为 union 的工具 schema，离线测试发现不了（在移植来源项目里出过事故）。
8. **导入约定**：本地相对导入写 `.ts` 后缀；Pi 包用 `@earendil-works/*`（旧名 `@mariozechner/*` 只出现在移植来的 `subagents.ts`，Pi 1.0.1 仍兼容）。
9. **界面**：文字用中文；涉及终端宽度时用 `@earendil-works/pi-tui` 的 `visibleWidth()` / `truncateToWidth()`，不要用 `string.length`（中文是双宽）。逻辑不能依赖渲染：RPC、JSON、print 模式下没有 widget。
10. **计费**：游戏 Bot 用 `deepseek/*`（按量）；工厂 roster 用 `openai-codex/*`（订阅）和 `deepseek/*`。不得引入 `anthropic/*` 或其它按量 provider。
11. **密钥**：`.env` 不入库（只留 `.env.example`）。`adws/adw_data/harness_engineering/dev_guard.ts` 拦截工厂 agent 读写 `.env*`、`~/.pi/agent/auth.json`、gh 配置，以及 `gh` 和改动 git 历史的命令——提交、推送、开 PR 是代码的事。
12. **工厂接活**：人给**自己开的** issue 打一个类型标签（`bug` / `enhancement` / `chore` / `documentation`）和 `factory:queued`；`just autoqueue` 认领（`factory:running`），在 `.autoqueue/worktrees/issue-N` 里跑 `just issue N`，成功标 `factory:pr-open`，失败标 `factory:needs-human` 并保留 worktree 与分支，从不自动重试。合并 PR 是唯一的人工闸门；合并后下一轮 `just autoqueue` 只清掉已关闭 issue 上的 `factory:pr-open`，其他标签不动。
13. **跨局战绩**：文件 IO 只放 `src/extension/`，统计与格式化保持纯函数。新开局和成功 `/restart` 生成 id，`/undo` 与加轮继续沿用 id；仅完成时按 id 追加或覆盖记录（含降低轮数结束空闲对局），不改变终局浮层触发规则。`/records` 始终用玩家卡片，0 token、不进模型上下文；读写异常只警告，不阻断游戏、不覆盖损坏历史。扩展测试必须用临时目录设置 `IDIOM_RECORDS_FILE` 并恢复环境，不能触碰真实 home 战绩。
14. **工厂改 PR**：工厂以操作者本人的账号开 PR，GitHub 不允许对自己的 PR 点 Request changes，所以触发靠标签：人照常留 review / 行内评论，然后给 PR 打 `factory:revise`；`just autoqueue-feedback` 在该分支的 worktree 里跑 `just pr-feedback N`（builder → `just test` 修复循环 → 提交、推送、在 PR 上回复）。工厂发的每条评论都带 `<!-- factory -->`，不会被当成意见读回；只有工厂上次回复之后的意见才算。合并后 GitHub 自动删远端分支。
