# Implementation Plan

把 [IdiomSolitaireMiniHarness](docs/agentic-engineering-paper.md)（自写 Python harness）重写为 Pi Agent Harness 上的 extension，并配一个由 GitHub issue/PR 驱动的软件工厂（SSSF）。

已定的设计：

- **方案 B（Pi 原生）**：人类输入在 `input` 事件里校验，合法才放行给 Pi 的 agent loop；Bot 只能通过 `submit_idiom` 工具出词，工具的 `execute()` 是唯一写账入口。
- **Bot 模型**：`deepseek/$DEEPSEEK_MODEL`（`.env`），按量计费；裁判与提示用同一模型做嵌套调用。
- **`/undo`**：快照栈，与 Python 版一致。
- **工厂**：以 `../OptionTradingPiHarness` 打过补丁的 `adws/` 和 `.claude/skills/sssf/` 为基础；串行、在主目录切分支（不用 worktree）；只处理 `aicoder2048` 创建并打标签的 issue；只有 "Request changes" 触发 PR 反馈。

## Stage 1: 仓库引导
**Goal**: git 仓库、`.gitignore`、`.env.example`、公开 GitHub 仓库 `aicoder2048/IdiomSolitairePiHarness`
**Success Criteria**: `.env` 与第三方文章全文不进仓库；首次 push 前用户确认文件清单
**Tests**: `git check-ignore .env docs/pi-docs/reference-articles/INDEX.md`
**Status**: In Progress（本地完成，等待用户确认后建远端仓库并 push）

## Stage 2: 纯游戏引擎（TypeScript，不 import Pi）
**Goal**: `src/engine/`：规则、Prompt、Verifier、Context、对局状态机（快照、计分、倒计时、命令）
**Success Criteria**: 从 Python 版平移的离线测试全部通过；`tsc --noEmit` 无错误
**Tests**: rules / prompts / verifier / context / game（回合两段式：人类入账 → Bot 提交 → 结算）
**Status**: Not Started

## Stage 3: 最小可玩的 Pi extension
**Goal**: `src/extension/`：`input` 拦截、`submit_idiom` 工具、`context` 裁剪、`before_agent_start` 系统提示、斜杠命令、简版 widget；`just play` 启动
**Success Criteria**: 能在 Pi TUI 里完整玩一局；斜杠命令 0 token；Bot 失败尝试不进入下一回合的上下文
**Tests**: 胶水层用假 `ExtensionAPI` 离线测试；一条 live 冒烟（RPC 模式）
**Status**: Not Started

## Stage 4: 移植软件工厂 + Issue 生命周期
**Goal**: 移植 SSSF（roster 按 `sssf.config.yaml.sample`）、本项目的 `dev_guard.ts`、`quality.py` 接 `just test`；`adw_issue` 加标签状态机（`factory:queued → running → pr-open / needs-human`）
**Success Criteria**: 一个打了 `factory:queued` 的 issue 能被处理成 PR，issue 下有进度评论
**Tests**: `adws/tests/` 离线测试；一次真实 issue → PR 演练
**Status**: Not Started

## Stage 5: PR 反馈回流、清理、交给工厂
**Goal**: `adw_pr_feedback`（"Request changes" 触发，`--adw-id` 续跑同一分支）、`adw_cleanup`；剩余功能（`/hint` overlay、详版面板、结算画面、trace、战绩榜）开成 issue
**Success Criteria**: 一次 Request changes → 工厂修订 → push → 回复评论的完整回路
**Tests**: `adws/tests/` 离线测试；一次真实 review 演练
**Status**: Not Started
