# IndyDevDan: pi-vs-claude-code 仓库导读

> Source: https://github.com/disler/pi-vs-claude-code
> Repo: `disler/pi-vs-claude-code` · MIT · TypeScript · 1198 stars / 292 forks (抓取时)
> Pushed: 2026-05-11 · 抓取日期: 2026-05-24
> Watch: [Pi Coding Agent: The Only Claude Code Competitor](https://youtu.be/f8cfH5XX-XU) · [Pi to Pi: Two-Way Agent Orchestration](https://youtu.be/PIdETjcXNIk)

---

## 1. 仓库定位

一个 **Pi Coding Agent 自定义实例的合集**。disler 把 Pi 当作 "Claude Code 的对手 / 备胎"，用一组（16+）TypeScript extension 演示：UI 完全可自绘、agent orchestration 可编程、安全审计可拦截、agent-to-agent 协议可自建。仓库里随附三份重量级对比文档（README + COMPARISON.md + PI_VS_OPEN_CODE.md，合计约 100KB），把 Pi vs Claude Code 和 Pi vs OpenCode 在 12+ 维度上掰开比一遍。结论性立场是 **"Pi = 平台 (platform)，CC/OC = 产品 (product)"**。

`.claude/` 目录极其精简（一个 statusline + 两个 slash command），整个仓库的中心是 `.pi/` 和 `extensions/`——这本身就是 disler 的观点：CC 已经够 polished，没什么可演示的；Pi 才是可改造的画布。

---

## 2. 仓库结构总览

```
pi-vs-claude-code/
├── .claude/                     # CC 侧，故意做得很薄
│   ├── commands/
│   │   ├── plan_w_team.md       # 复杂 multi-agent planning 模板（Task/TaskCreate 全家桶）
│   │   └── prime.md             # 极简 "load context" 命令
│   ├── settings.json            # 唯一内容：把 statusline 接到 uv 脚本
│   └── status_lines/status_line.py  # uv inline-script，Python 渲染 ANSI 进度条
│
├── .pi/                         # Pi 侧，承载全部声明式资产
│   ├── settings.json            # `theme: synthwave`、`prompts: [../.claude/commands]`
│   ├── damage-control-rules.yaml  # ~280 行 bash 黑名单 + 路径白/黑/只读名单
│   ├── agents/                  # markdown frontmatter 风格的 sub-agent persona
│   │   ├── teams.yaml           # 5 个团队组合（full / plan-build / info / frontend / pi-pi）
│   │   ├── agent-chain.yaml     # 5 条 sequential pipeline 定义
│   │   ├── planner.md / builder.md / reviewer.md / scout.md /
│   │   │ documenter.md / bowser.md / red-team.md / plan-reviewer.md
│   │   └── pi-pi/               # meta-agent 用的 9 个 "framework expert"
│   ├── skills/bowser/SKILL.md   # Agent Skills 标准 demo
│   └── themes/*.json            # 11 套配色（synthwave / tokyo-night / dracula / ...）
│
├── extensions/                  # ★ 仓库主体：18 个 .ts，3000~6000 行/大文件
│   ├── pure-focus.ts / minimal.ts                  # UI 减法
│   ├── tool-counter.ts / tool-counter-widget.ts    # footer / widget 富信息
│   ├── purpose-gate.ts                             # input 拦截 + 动态 system prompt + widget
│   ├── tilldone.ts                                 # 任务纪律系统
│   ├── damage-control.ts / damage-control-continue.ts  # 安全审计（block vs soft-block）
│   ├── subagent-widget.ts                          # /sub 派生 background pi 进程 + live widget
│   ├── agent-team.ts                               # dispatcher pattern + grid dashboard
│   ├── agent-chain.ts                              # sequential pipeline (YAML driven)
│   ├── pi-pi.ts                                    # meta-agent，并行 query 多个 framework expert
│   ├── cross-agent.ts                              # 把 .claude/.gemini/.codex 的 commands 注入 Pi
│   ├── system-select.ts                            # /system 切换 agent persona = 切 system prompt
│   ├── coms.ts                                     # Unix socket / named-pipe peer-to-peer
│   ├── coms-net.ts                                 # HTTP+SSE peer-to-peer（跨机）
│   ├── session-replay.ts                           # 全屏 overlay 浏览历史
│   ├── theme-cycler.ts / themeMap.ts               # Ctrl+X/Q 切主题 + 每个 ext 默认主题映射
│
├── scripts/coms-net-server.ts   # Bun HTTP/SSE hub
├── specs/                       # 4 份功能 spec（damage-control / pi-pi / agent-workflow / agent-forge）
├── justfile                     # 30+ 入口，逐个 ext 启动 + `just all` 多窗口
├── README.md (30KB) / COMPARISON.md (39KB) / PI_VS_OPEN_CODE.md (30KB)
├── CLAUDE.md / TOOLS.md / THEME.md / RESERVED_KEYS.md  # extension 作者参考
└── package.json                 # 仅一个 dep：`yaml`（Pi 自己提供其它运行时）
```

---

## 3. Pi 侧实现

### 3.1 三层资产模型

Pi 的"声明式"资产全部落在 `.pi/`，extension 是"命令式"部分。两层各司其职：

| 层      | 资产                          | 谁来消费                                                    |
| ------ | --------------------------- | ------------------------------------------------------- |
| 数据/配置 | `.pi/settings.json`、`.pi/themes/*.json` | Pi runtime                                              |
| 声明式行为 | `.pi/agents/*.md`（frontmatter + body）、`.pi/agents/*.yaml`、`.pi/damage-control-rules.yaml`、`.pi/skills/*/SKILL.md` | extension（每个 ext 自己扫目录、解析 yaml/frontmatter） |
| 命令式行为 | `extensions/*.ts`           | Pi 用 jiti 在主进程内运行                                       |

注意 `prompts: ["../.claude/commands"]` 这一行——Pi 直接复用 `.claude/commands/*.md` 作为 slash-command prompt 模板，这是 disler 偏好的"少做事"做法。

### 3.2 关键 extension 模式速览

下表按"信息密度从低到高"排，方便读源码定位。

| ext                  | 行数   | 用到的 Pi 事件 / API                                                                                                                                  | 一句话精髓                                                                                              |
| -------------------- | ---- | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------- |
| `pure-focus.ts`      | 24   | `session_start` + `ctx.ui.setFooter`                                                                                                             | render 返回 `[]` = footer 直接消失                                                                       |
| `minimal.ts`         | 33   | 同上 + `ctx.getContextUsage()` + `theme.fg()`                                                                                                      | 10 格 `[###-------] 30%` 上下文计                                                                       |
| `purpose-gate.ts`    | 84   | `session_start` + `ctx.ui.input/notify/setWidget` + `before_agent_start`（改 systemPrompt）+ `input`（returns `{action:"handled"}` 拦截）                | 三件套：拦输入、改 system prompt、画 widget                                                                   |
| `damage-control.ts`  | 209  | `session_start`（读 yaml）+ `tool_call` + `isToolCallEventType()` + `ctx.ui.confirm` + `ctx.abort()` + `pi.appendEntry("damage-control-log", ...)` | 返回 `{block:true, reason}`；reason 里硬塞 "DO NOT attempt to work around this restriction"            |
| `cross-agent.ts`     | 292  | 扫 `.claude/.gemini/.codex` → `pi.registerCommand` + slash 命令模板里支持 `$ARGUMENTS / $@ / $1...`                                                       | Pi 一个命令注册器吞下三家生态的 prompt                                                                          |
| `system-select.ts`   | 167  | `pi.registerCommand("system")` + `ctx.ui.select` + `pi.setActiveTools()` + `before_agent_start`（prepend agent body 到 systemPrompt）              | `/system` = 运行时换 persona，且可裁剪 tool set                                                            |
| `agent-team.ts`      | 734  | `spawn("pi", [...])` + 自定义 tool `dispatch_agent`（typebox schema）+ widget grid                                                                    | 主 agent 不带代码工具，**只能 dispatch**；每个 specialist 自留 session 文件以便跨调用记忆                                  |
| `agent-chain.ts`     | 797  | 解析 `agent-chain.yaml` + `$INPUT / $ORIGINAL` 模板替换 + `run_chain` tool + spawn 串行 pi 进程                                                            | 把 sub-agent 流水线编码成 yaml，主 agent 只决定"该不该跑、跑哪条链"                                                    |
| `subagent-widget.ts` | 481  | `/sub`/`/subcont`/`/subrm`/`/subclear` 命令 + spawn pi + persistent session jsonl + 多个 widget 叠加                                                  | `/subcont N` 用 session 文件复活历史 sub-agent                                                            |
| `pi-pi.ts`           | 633  | 自定义 tool `query_experts`（**数组** 入参，内部并行 spawn 多 pi）+ `before_agent_start`（注入 `{{EXPERT_COUNT}}/{{EXPERT_NAMES}}` 模板）                            | 9 个 framework expert（ext/theme/skill/tui/...）并行查 Pi 文档，orchestrator 综合后写文件                         |
| `coms.ts`            | 1597 | Unix socket / named-pipe + `~/.pi/coms/projects/<project>/agents/*.json` 注册表 + 4 个 tool `coms_list/send/get/await` + `agent_end` 捕获回复            | 4 个 tool、0 魔法；msg 信封里带 `hops`，`MAX_HOPS=5` 防 A↔B 死循环                                              |
| `coms-net.ts`        | 1635 | 同上但走 HTTP + SSE，依赖 `scripts/coms-net-server.ts` 的 Bun hub；客户端 auto-discover `server.json`                                                       | 跨机版；localhost 自动生成 token，LAN/远程必须 `PI_COMS_NET_AUTH_TOKEN`                                        |

### 3.3 Agent / Team / Chain 声明文件

`.pi/agents/*.md` 全部走 Claude Code 一样的 frontmatter，例：

```markdown
---
name: planner
description: Architecture and implementation planning
tools: read,grep,find,ls
---
You are a planner agent. Analyze requirements and produce clear, actionable implementation plans...
```

`teams.yaml` 把 persona 组成命名团队（`agent-team.ts` 启动时弹 select 让你挑队）：

```yaml
full:        [scout, planner, builder, reviewer, documenter, red-team]
plan-build:  [planner, builder, reviewer]
frontend:    [planner, builder, bowser]
pi-pi:       [ext-expert, theme-expert, skill-expert, config-expert,
              tui-expert, prompt-expert, agent-expert]
```

`agent-chain.yaml` 把流水线显式化，`$INPUT` 是上一步输出，`$ORIGINAL` 永远是用户原 prompt：

```yaml
plan-build-review:
  description: "Plan, implement, and review — the standard development cycle"
  steps:
    - agent: planner   ; prompt: "Plan the implementation for: $INPUT"
    - agent: builder   ; prompt: "Implement the following plan:\n\n$INPUT"
    - agent: reviewer  ; prompt: "Review this implementation for bugs, style, and correctness:\n\n$INPUT"
```

注意 `plan-review-plan` 这条链用了同一个 `planner` 跑三次（自我修订），`scout-flow` 用了 `scout` 跑三次（triple-scout 验证）——把 agent 当函数用。

### 3.4 damage-control 规则结构

`.pi/damage-control-rules.yaml` 是声明式的安全策略，extension 在 `tool_call` 钩子里消费：

```yaml
bashToolPatterns:
  - { pattern: '\bgit\s+reset\s+--hard\b', reason: "git reset --hard (use --soft or stash)" }
  - { pattern: '\bgit\s+restore\s+\.',     reason: "Discards all uncommitted changes", ask: true }
  - { pattern: 'DELETE\s+FROM\s+\w+\s*;',  reason: "DELETE without WHERE (will delete ALL rows)" }
  ...
zeroAccessPaths: [.env, ~/.ssh/, "*.pem", "*.tfstate", serviceAccountKey.json, ...]
readOnlyPaths:   [/etc/, package-lock.json, "*.min.js", dist/, ...]
noDeletePaths:   [.git/, README.md, Dockerfile, CLAUDE.md, ...]
```

整套规则覆盖 AWS / GCP / Firebase / Vercel / Netlify / Cloudflare 的破坏性命令（terminate-instances、delete-cluster、firebase projects:delete...），是一份现成的 production-grade 黑名单。

---

## 4. Claude Code 侧实现

故意做得极轻量，只有三件东西：

### 4.1 `.claude/settings.json`

```json
{ "statusLine": { "type": "command", "command": "uv run .claude/status_lines/status_line.py", "padding": 0 } }
```

接到一个 **`uv run` 的 PEP-723 inline-script**——这是 disler 自己 status_line 系列工作的延伸（v6.5，最小化版）。Python 从 stdin 拿 CC 的 JSON 事件，渲染 `[Model] [###---] 42.5%` 一行。

### 4.2 `.claude/commands/plan_w_team.md`

一份"团队 planning"模板，要点：

- frontmatter 用了 `disallowed-tools: Task, EnterPlanMode` 来强制 planner **只写计划不动手**
- 介绍 `TaskCreate / TaskUpdate / TaskList / TaskGet` 这套**任务管理工具集**
- 演示 `Task({...})` 部署 sub-agent 和 `resume: "abc123"` 复用 session
- 通过 `addBlockedBy: ["1"]` 声明依赖；`run_in_background: true` + `TaskOutput({block:false})` 跑并行
- 输出格式硬编码：`### N. <Task Name>` 含 Task ID / Depends On / Assigned To / Agent Type / Parallel

这一份很像 disler 在 youtube 上反复演示的 **"orchestrator-as-prompt"** 模式——靠 prompt 把 lead agent 钉死成调度员。

### 4.3 `.claude/commands/prime.md`

```markdown
1. Run `git ls-files --others --cached --exclude-standard` to see the project file tree
2. Read `justfile`, `THEME.md`
3. Read `extensions/*`
4. Read `.pi/agents/*`
5. Read `.pi/settings.json`, `.pi/themes/synthwave.json`
6. Summarize your understanding of the project: ...
```

一个标准 "context-priming" 命令。`justfile` 里 `primecc` 是 `claude --dangerously-skip-permissions --model opus[1m] /prime`，`primepi` 是 `pi /prime`——两边同 prompt 跑一遍是为了"录视频 side-by-side 对比"。

> 注意：**没有 `.claude/agents/` 子目录**，没有 hook 配置，没有 MCP 配置。Claude Code 侧只展示了它**与生俱来的 statusline + slash command** 这两个最常用的 1st-party 入口。

---

## 5. 对比维度（按特性）

下表把 README + COMPARISON.md 里 12 类对比浓缩到一屏。`★` = disler 偏向 Pi，`☆` = 偏向 CC，`=` = 平手。

| 维度                 | Pi                                                                                | Claude Code                                                                        | disler 评价 |
| ------------------ | --------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------- | --------- |
| **System prompt**  | ~200 tokens，信任前沿模型                                                                | ~10000+ tokens（含 guardrail/工具说明）                                                    | ★ Pi 留出更多 context 给真活                              |
| **默认工具数**          | 4 (read/write/edit/bash)，+3 optional (grep/find/ls)                               | 10+ (含 Glob/Grep/WebSearch/WebFetch/NotebookEdit/Task)                              | = "trade-off"，不是输赢                                |
| **Hook 数量 / 模型**   | **25+** typed TS 事件（in-process）                                                   | **14** shell-command hook（外部进程）                                                     | ★ Pi 多出 input、before_agent_start、tool_execution_stream、context、model_select、session_fork 等 8+ 钩子 |
| **能在 user prompt 入 agent 前拦截吗？** | ✅ `input` event                                                                   | ❌                                                                                  | ★ "Pi-only，这是 huge"                                |
| **能动态改 system prompt 吗？**         | ✅ `before_agent_start` 每 turn 可改                                                   | ❌                                                                                  | ★                                                  |
| **Tool 拦截**        | `tool_call` 返回 `{block, reason}`；`isToolCallEventType()` 类型收窄                      | `PreToolUse` allow/deny/ask + `updatedInput`                                       | = 都能拦                                              |
| **Tool 执行流式**      | `tool_execution_start/update/end`                                                 | ❌                                                                                  | ★ live progress widget 必备                          |
| **Subagent / Task** | extension `subagent-widget` spawn 独立 pi 进程；coms 走 peer-to-peer                     | native `Task` tool，7 并行，permission 继承                                               | ☆ CC 开箱即用                                          |
| **Agent teams**    | 仓库内 `agent-team.ts` + `teams.yaml` 自建                                              | native team coordination（lead + workers）                                            | ☆ CC 开箱即用                                          |
| **Permission**     | YOLO by default；`damage-control` ext 自建（YAML rules + `tool_call` block）            | 5 模式 deny-first + filesystem sandbox + Haiku 预筛                                    | ☆ "Pi 是 security theater 立场，但你可以自建"                |
| **Plan mode**      | 无，"让 agent 自己思考、把 plan 写到文件里"                                                      | 内置 Plan/Build Tab 切换                                                                | ☆ CC 开箱即用                                          |
| **MCP**            | 无内置（论点：7-14K token overhead），可走 ext                                                | first-class native，lazy loading                                                    | ☆ CC 开箱即用                                          |
| **Skills**         | 支持，与 `~/.claude/skills` 跨工具兼容（Agent Skills 标准）                                     | 支持                                                                                  | = 都用 SKILL.md 标准                                   |
| **Slash commands** | `.pi/prompts/` + `pi.registerCommand()`；本仓库直接复用 `.claude/commands/`                | `.claude/commands/*.md`                                                            | = Pi 多一条程序化注册路径                                    |
| **Provider 数**     | 20+ native, 324 模型, cross-provider context handoff                                | 4 platform 全是 Claude；其它走 `ANTHROPIC_BASE_URL` gateway                              | ★ Pi 一开始就 multi-model                              |
| **UI 自定义**         | header / footer / status / widget / overlay / dialog / 51 个 color token / hot-reload | 仅 statusline（命令脚本输出一行）                                                              | ★ "Pi TUI 是 canvas，CC TUI 是 closed product"        |
| **Session**        | JSONL **树**（id/parentId，可 fork/branch/switch/tree）                                | 线性                                                                                  | ★ session_fork 等钩子是 Pi-only                        |
| **SDK / RPC**      | `--mode rpc`（26+ 命令，bidir JSON），`createAgentSession`                              | `@anthropic-ai/claude-agent-sdk` + `claude --print`                                | ★ RPC mode 任何语言驱动                                  |
| **Cost**           | $0（MIT, BYOK）                                                                     | $20-200/mo 订阅或独立 API key                                                            | ★                                                  |
| **生态 / 企业**        | 11.5K stars，3.17M monthly npm                                                     | 企业 SSO / audit / IDE 插件 / 桌面 app / GitHub Actions bot                              | ☆ CC 企业级                                           |

> COMPARISON.md 里还有 Sharing & Distribution（marketplace vs `pi install npm:/git:/local`）和 Community & Ecosystem（包括给 Mario Zechner 打的标签——"libGDX 作者 24.8K stars"、"Armin Ronacher 在用"）这两节，但属于背景信息，对 theta 没直接价值。

---

## 6. 作者观点 / 取舍

把 PI_VS_OPEN_CODE.md 的 "thesis" 段落和 README 的语气结合，disler 的立场可总结为：

1. **"Pi = platform, CC/OC = product"**——Pi 给的是**运行时级别**的控制，CC 给的是**配置级别**的控制
2. **"复杂性预算应该在你手里"**——"three similar lines is better than a premature abstraction"（直接照 Karpathy 那套）
3. **"前沿模型已经 RL-trained up the wazoo"**——少塞 guardrail prompt，把 context 留给真活
4. **"YOLO by default"**——安全是工程问题不是 prompt 问题，要安全自己装 `damage-control`
5. **"Hierarchy loses"** (从 `coms` 那一节)——info 最丰富的人在 worker level，让 agent peer-to-peer 直接说话，不要塞回 orchestrator 一层层转
6. **"Heterogeneous teams win"**——同一对话池里塞 `claude-opus-4-7` + `gpt-5.5` + `deepseek` + `glm`，不同 RL 训练互补
7. **Pi 没有的东西，没说它好（诚实）**——MCP、LSP、permission、IDE 插件、Plan mode、桌面 app 这些 CC/OpenCode 赢得明明白白，Pi 的"alternative"列里也都写了"You build it"

但他依然选 Pi 当主力，因为他要的是**可编程的 agent loop**，不是另一个 polished alternative。

---

## 7. 值得抄过来的 pattern（给 theta）

按 ROI 排序，theta（embed Pi SDK 的 wheel-specialized app）能直接借鉴的：

### 7.1 `damage-control` 的"YAML 规则 + `tool_call` 拦截 + `appendEntry` 审计日志"三件套（★★★★★）

theta 的 board.ts 已经有 mini-orchestrator，加一个 `wheel-rules.yaml` 拦截"卖 covered call 时 strike < cost basis"、"roll 时 net debit > threshold"这类 wheel 业务硬规则，比再加 prompt guardrail 干净得多。代码骨架可以 1:1 抄 `extensions/damage-control.ts`，只换 rule schema 和 `isToolCallEventType()` 分支。

注意它 `block: true` 时**塞进 reason 的 anti-circumvention 话术**：

```
DO NOT attempt to work around this restriction. DO NOT retry with alternative
commands, paths, or approaches that achieve the same result. Report this block
to the user exactly as stated and ask how they would like to proceed.
```

这是 production 经验，agent 默认会"换个写法重试"，必须显式禁掉。

### 7.2 `purpose-gate` 的三件套：`input` 拦截 + `before_agent_start` 注入 + `setWidget` 显示（★★★★）

theta 每次 session start 应该问"**今天要 review 哪个 ticker 的 wheel？预算？**"，然后 lock 进 system prompt + 顶部 widget。`purpose-gate.ts` 只有 84 行，模板可以直接 fork。

### 7.3 `agent-chain.yaml` 的"$INPUT / $ORIGINAL"模板（★★★★）

theta 的 wheel decision flow 本质就是 chain：`scan-options → score → propose-trade → risk-review`。把这套写进 yaml 比写进 prompt 可维护得多。`agent-chain.ts` 的解析器只用了 regex，没拉 yaml 库（虽然有 `yaml` dep）——可以直接抄。

### 7.4 `cross-agent.ts` 的 frontmatter+slash-command 复用（★★★）

theta 用 Pi SDK embed 模式，也可以扫 `.theta/agents/*.md` 自动注册成 `/wheel-scan`、`/wheel-roll` 等 slash command。frontmatter parser 是 ~10 行 regex（README 里说 "Pi 直接消费 `.claude/commands/`"，theta 可以也消费它自己 family 内的）。

### 7.5 `subagent-widget` 的 "spawn pi + persistent jsonl session + 复活 via `/subcont N`"（★★★）

theta 的 "research a ticker" 子任务很适合派一个 background pi，主 TUI 不阻塞。这个 pattern 比直接同步调 `createAgentSession({...})` 多一层隔离——失败/慢不会拖垮 board。

### 7.6 `pi-pi` 的"并行 expert + 单一 writer"（★★）

如果 theta 要做 "auto-research a new ticker"，可以同样布局：earnings-expert / iv-expert / catalyst-expert / chart-expert 各跑自己的 sub-process 拉数据，主 agent 综合后只它一个写 decision 文件。注意 `query_experts` 这个 tool 的 input 是**数组**（一次性触发并行），不是循环调用——这是 Pi 工具系统的隐式约束（见 user 自己整理的 "pi sdk gotchas" memory）。

### 7.7 themeMap.ts 的"每个 extension 自带默认主题"（★）

theta 的"trade-running" mode 用红/绿主题，"analysis" mode 用 cool 主题——可以用同样的 `applyExtensionDefaults(import.meta.url, ctx)` 模式。

### 7.8 不要抄：`coms-net` 的跨机 peer-to-peer

很酷但 theta 不需要——你一个 Mac 全搞定，加 HTTP/SSE hub 是不必要复杂度。同样的 `coms.ts`（同机 Unix socket）也用不上：theta 的 sub-agent 都是父子关系，没有 peer 场景。

---

## 8. 引用 / 视频 / 相关资源

| URL                                                          | 用途                                                                          |
| ------------------------------------------------------------ | --------------------------------------------------------------------------- |
| https://youtu.be/f8cfH5XX-XU                                 | 主视频："Pi Coding Agent: The Only Claude Code Competitor"——README 头条           |
| https://youtu.be/PIdETjcXNIk                                 | "Pi to Pi: Two-Way Agent Orchestration"——`coms`/`coms-net` 配套               |
| https://github.com/mariozechner/pi-coding-agent              | Pi 主仓库（README 里到处引用）                                                        |
| https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/extensions.md | Pi extension event 列表权威源                                                     |
| https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/sdk.md | Pi TypeScript SDK reference                                                |
| https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/rpc.md | Pi RPC 协议                                                                   |
| https://docs.anthropic.com/en/docs/claude-code/hooks        | CC hooks 官方文档（README hook 对比表的对照源）                                          |
| https://x.com/badlogicgames                                  | Mario Zechner（Pi 作者，libGDX 24.8K stars 作者）                                  |
| https://agenticengineer.com/tactical-agentic-coding?y=pivscc | disler 自家 paid course，README 脚注                                              |
| https://www.youtube.com/@indydevdan                          | disler YouTube                                                              |
| https://agentskills.io                                       | Agent Skills 跨工具标准（COMPARISON.md 提到）                                        |
| https://shittycodingagent.ai/packages                        | Pi gallery（pi-package npm keyword）                                          |

---

## 9. 一句话总结

> **pi-vs-claude-code 不是"Pi vs CC"的客观 benchmark，而是 disler 一份带立场的 "Pi 已经是 platform 级别的 agent harness" 自证演示——18 个 extension 把 Pi 的 25+ 事件/UI API/sub-process orchestration 全用了一遍，并附上 100KB 的对比文档把 CC/OpenCode 在哪些维度赢、Pi 在哪些维度赢全部摊开；对 theta 直接可抄的有 `damage-control` (YAML 规则 + tool_call 拦截)、`purpose-gate` (input + before_agent_start 三件套)、`agent-chain.yaml` ($INPUT/$ORIGINAL 模板) 三套 pattern，其它（peer-to-peer、grid dashboard、meta-agent）是 demo，theta 不必跟。**
