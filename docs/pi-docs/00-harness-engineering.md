# Agent Harness 与 Harness Engineering — 概念与 Pi 落地

> 这页是整个 `pi-docs/` 的"哲学开篇"。读完它，你会带着同一个 mental frame 去看后续 3 套教程。

## 名词 vs 动词

| 概念 | 词性 | 含义 |
|---|---|---|
| **Agent Harness** | 名词 | 围绕 AI 模型构建的**编排框架** —— 把模型的通用能力变成可靠的工程系统 |
| **Harness Engineering** | 动词 | 围绕 harness 的**工程实践学科** —— 设计、测试、迭代、维护它 |

**核心论点**（IndyDevDan 反复强调）：

> 模型在 commodify，**harness 才是护城河**。掌握 harness engineering 比追新模型更有持续回报 —— 模型在变，但"如何驾驭模型"的方法论在沉淀。

## Agent Harness 的典型组成

不论 Claude Code / Pi / Codex / 你自己造的 —— 一个 harness 通常包含：

- **确定性代码**：控制流、重试、错误处理
- **Token 缓存与上下文管理**：context window 满了怎么办、compaction、context reset
- **Agent 编排**：分工、通信、协调（subagent / dispatcher / chain / meta）
- **Prompts 和 Skills**：角色指令、按需加载的能力包
- **模型路由**：什么任务用 Sonnet / 什么用 Haiku

## 三方 canonical 视角

读这 4 套教程时，时不时回头扫一眼这张三方对照表：

### Anthropic — Harness design for long-running apps

> 来源：[Anthropic Engineering Blog · Harness Design 2026-03-24](https://www.anthropic.com/engineering/harness-design-long-running-apps)（Prithvi Rajasekaran）

核心结论：

- **Planner / Generator / Evaluator 三角架构** —— 用 GAN 思路解决 "self-evaluation" 问题（agent 自评偏宽松）
- **Harness 每个组件都编码了对模型局限的假设**：模型进步后这些假设会过时（例：Anthropic 在 Opus 4.6 后去掉了 Sprint 和 context reset），因此 harness 需要**定期重审**
- **配 Evals 才不是盲飞** —— 没 evals 的 harness 凭直觉迭代会卡住
- **Solo 20min/$9 vs Full harness 6h/$200**，但功能完整度差距巨大

实战 hooks 模式：

```
┌──────────┐    spec     ┌──────────┐    code     ┌──────────┐
│ Planner  │ ──────────► │Generator │ ──────────► │Evaluator │
└──────────┘             └────▲─────┘             └────┬─────┘
                              │     bug list & rubric  │
                              └────────────────────────┘
```

### OpenAI — Harness engineering with Codex

> 来源：[OpenAI Engineering Blog · Harness Engineering 2026-03-11](https://openai.com/index/harness-engineering/)（Ryan Lopopolo）

核心结论：

- **Agent legibility 是目标** —— "What Codex can't see doesn't exist"。把人脑里的、Slack 里的、Google Docs 里的知识全部 push 到 repo（markdown / schema / plan）
- **AGENTS.md 是 TOC 不是百科** —— ~100 行的目录指向 `docs/` 各处真相来源；progressive disclosure
- **架构不变量靠 linter 编码** —— "由 Codex 自己生成的 lint 规则"，把"严格分层依赖"变成机械检查
- **Garbage collection** —— 用定期跑的 background agent 扫"AI slop"、更新 quality grade、开重构 PR
- 实测：3 名工程师用 Codex 5 个月产出 100 万行代码 / 1500 PR，**Humans steer, Agents execute**

知识布局示例：

```
AGENTS.md           ← 100 行 TOC
ARCHITECTURE.md
docs/
├── design-docs/
├── exec-plans/{active, completed}
├── product-specs/
├── references/    ← *-llms.txt 第三方文档
└── DESIGN.md, RELIABILITY.md, SECURITY.md, ...
```

### IndyDevDan — Harness Engineering 三视频

> 来源：[Bilibili 转录 + V1/V2/V3 YouTube](../study-notes/20260504-211608-pi-philosophy-from-video.md)（已存为 study note）

核心结论（详见 [`indydevdan-extensions-tutorial/99-dan-vocabulary.md`](../tutorials/indydevdan-extensions-tutorial/99-dan-vocabulary.md)）：

- **"Harness engineering is the new high-leverage skill"**
- **Core 4**：context / model / prompt / tools 必须一起调
- **Specialization is the advantage**：通用 agent 给正态分布，专精给长尾
- **Compute is leverage**：多 agent > 单 agent
- **Build the system that builds the system**：用 Claude Code 做 meta-builder 生成 Pi 扩展

## Pi 在这套理念中的位置

**Pi = 你落地 Agent Harness 的具体的、基础的框架**。

| Harness 组成 | Pi 的具体实现 |
|---|---|
| 确定性代码 | Pi 自己（Mario 用 TS 写的 ~10k LOC） |
| Token 缓存 / context 管理 | Pi 内置自动 compaction + 手动 `/compact` |
| Agent 编排 | 你的扩展通过 `pi.on(...)` 挂在 lifecycle 上 |
| Prompts / Skills | `~/.pi/agents/`、`.claude/agents/`、`.pi/agent/skills/`（Pi 接受多厂商目录） |
| 模型路由 | `ctx.setModel(...)`、`createAgentSession({model: ...})`、`pi.registerProvider(...)` |
| 可观测性 | `tool_counter`、`session-replay`、`provider-payload` 等扩展（[`02-ui-toolkit.md`](../tutorials/indydevdan-extensions-tutorial/02-ui-toolkit.md)） |
| 编排拓扑 | Subagent / Team / Chain / Meta（[`05`](../tutorials/indydevdan-extensions-tutorial/05-subagent.md)–[`08`](../tutorials/indydevdan-extensions-tutorial/08-meta-agent.md)） |
| 架构不变量 | `damage-control` YAML rules + `tool_call` 拦截（[`03-discipline.md`](../tutorials/indydevdan-extensions-tutorial/03-discipline.md)） |
| 知识布局 | `.pi/agents/`、`teams.yaml`、`agent-chain.yaml` —— 跟 OpenAI 的 `docs/` 同精神 |
| 三角架构 | Anthropic Planner/Generator/Evaluator 在 Pi 里 = `agent-chain` 的 specialist 配置 |

## 怎么用这页

读后续教程时，**每次遇到新 API 或新模式就在心里问**：

1. 这是 harness 的**哪一个组成**？（控制流 / 上下文 / 编排 / prompt / 路由 / 观测 / 不变量）
2. 它编码了**哪个对模型局限的假设**？（模型进步了它还需要吗？）
3. 它是 **Anthropic / OpenAI / Dan 哪一派**的实践？

带着这套问题读 4 套教程，你学的不是 Pi 的 API，而是 **harness engineering 这门学科** —— Pi 只是它的一个具体载体。

## 4 套教程在 harness eng 上的角色

| 教程 | 角色 |
|---|---|
| [`tutorials/ts-tutorial/`](../tutorials/ts-tutorial/) | **harness 的语言** —— TS 是写 Pi 扩展的母语；type-safe + agent-legible 是 harness 工程的基本功 |
| [`pi-docs/official-docs/`](./official-docs/) | **了解一款生产级 harness 的 surface** —— Pi 的设计选择都是 harness eng 的取舍样本 |
| [`tutorials/pi-extensions-tutorial/`](../tutorials/pi-extensions-tutorial/) | **harness primitives 学习** —— "lifecycle 即挂载点"是 Pi 哲学；学完你能在任何 harness 上想清楚怎么挂 hook |
| [`tutorials/indydevdan-extensions-tutorial/`](../tutorials/indydevdan-extensions-tutorial/) | **harness composition 学习** —— 把 primitives 拼成纪律系统、多 agent 编排、meta agent |

## 进一步阅读

- [pi-extensions-tutorial/00-README.md](../tutorials/pi-extensions-tutorial/00-README.md) —— Pi 哲学三大支柱（与本文章互补）
- [indydevdan-extensions-tutorial/99-dan-vocabulary.md](../tutorials/indydevdan-extensions-tutorial/99-dan-vocabulary.md) —— Dan 的完整词汇 + Lifecycle 桥接词典
- [`study-notes/20260504-211608-pi-philosophy-from-video.md`](../study-notes/20260504-211608-pi-philosophy-from-video.md) —— B 站视频原话精炼笔记
- 顶层 [README.md](../README.md) —— 4 套教程映射到 harness eng 学习层级
