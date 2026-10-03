# Upstream

## 本仓库的副本（2026-10-03）

本仓库的 `.claude/skills/sssf/`、`adws/`、`scripts/autoqueue.py`、`tests/test_autoqueue.py` 不是从上游安装的，而是从
`../OptionTradingPiHarness`（commit `c5752ce`）复制的 git 跟踪文件，所以下面「本地补丁」表里的改动都已包含。在此之上又改了：

| 文件 | 改动 |
|---|---|
| `adws/adw_data/harness_engineering/dev_guard.ts` + `adws/tests/dev_guard.test.ts` | 重写：去掉期权账本沙箱（`OPT_*`、`state/`、`runs/`）；拦截 `.env*`、`~/.pi/agent/auth.json`、gh 配置、ssh 密钥，以及 `gh` 和改动 git 历史的命令（commit、push、checkout、reset 等）；导入改为 `@earendil-works/*` |
| `adws/adw_modules/quality.py` | `test` = `just test`，`lint` = `just lint`（ruff 只管工厂的 Python），`typecheck` = `just typecheck`（tsc）；去掉占位的 `build` 块 |
| `scripts/autoqueue.py` + 测试 | 标签 `auto:ready / in-progress / failed` 改为 `factory:queued / running / needs-human`，成功后加 `factory:pr-open`；只接 `FACTORY_AUTHORS`（默认 gh 当前用户）开的 issue；worktree 里 `uv sync` 改为 `bun install --frozen-lockfile`；分支 `factory/issue-N` |
| prompts、注释、`test_permissions.py`、`test_quality_gate.py` | 期权项目的示例路径与说明换成本项目的 |
| roster `adws/adw_sssf_config/sssf.config.yaml` | 与来源项目相同（即用户给的 `sssf.config.yaml.sample`），只改了 dev_guard 那行注释 |

从来源项目同步时，以上几处要手动合并，不要整体覆盖。

## 上游

- 来源：https://github.com/disler/super-simple-software-factory （MIT）
- 路径：`.claude/skills/sssf/`
- 基线：`de31374`（2026-08-02）
- 本地安装生成的 `adws/` 来自这个版本的 `templates/`。

## 本地补丁

| 文件 | 改动 | 上游状态 |
|---|---|---|
| `templates/adws/adw_modules/agent_pi.py` | `context_window()` 在 `~/.pi/agent/models.json` 缺失时按空目录处理，回退到 `pi --list-models` | issue #5；PR #4 / #8 未合并 |
| `adws/adw_modules/gates.py` + `agents.py` + `runner.py`（仅 adws/，模板未改） | `diff_matches_claims` 核对"本次调用改了哪些文件"：基线是 `agents.execute` 调用前的 `permissions.snapshot`，双向校验（声明了没改 / 改了没声明）；builder `system.md` 写明 `changed_files` 的口径；测试在 `adws/tests/`，`just test-adws` | issue #6；取 PR #15 的思路，但它比对整个工作区，会误伤 plan→build 链与未提交改动，且 porcelain 折叠新目录、`lstrip("./")` 会吃掉 `.gitignore` 的点，故未照搬 |
| `adws/adw_modules/agent_pi.py`、`adws/adw_data/harness_engineering/{dev_guard.ts,subagents.ts}`、roster（仅 adws/） | pi 加 `--no-extensions` 与 `--no-skills`，agent 的 harness 和指令只来自 roster（不加载 .pi/extensions 与全局 skills）；新增 `dev_guard.ts`（本项目专用）；subagents 也带 `-e dev_guard.ts` | 本地需求，不上游 |
| `adws/adw_modules/permissions.py` + roster `protected_files`（仅 adws/） | `always_writable` 从整个 `data_dir` 收窄到 `data_dir/sessions/`（原先让所有 agent 都能改 prompt_engineering/ 与 harness_engineering/）；受保护路径只能被 `writes` 里显式的路径/目录解锁，通配符（documenter 的 `**/*.md`）不再解锁；两目录加入 `protected_files`；测试 `adws/tests/test_permissions.py` | 上游同样存在，未提 issue |
| `adws/adw_modules/git_helper.py` + `adw_simple_sdlc` / `adw_plan_build_test` / `adw_plan_build_test_quality`（仅 adws/） | 代码提交说明原先取最后一次 builder 返修的 `commit_message`；现由 `build_commit_message()` 以首次 build 为标题、修复/返修列入正文；测试 `adws/tests/test_commit_message.py` | 上游同样存在，未提 issue |
| `adws/adw_modules/{agent_pi,agents,data_types,console}.py` + roster（仅 adws/） | 模型调用加**空闲超时**（`idle_timeout_s`，默认 600 秒无任何输出即结束整个进程组，抛 `PiUnavailable`）与**备用模型**（`fallback_model`，不可用时在同一会话里换模型重试一次，控制台 `⇄` 提示、trace 记 `model_fallback`；下一阶段仍先用主模型）。roster：默认备用 `deepseek/deepseek-flash`，reviewer 备用 `openai-codex/gpt-6-sol`；测试 `adws/tests/test_model_fallback.py` | 上游无此功能（issue #13 讨论过截止时间，修复只在提出者的 fork）；起因：2026-10-01 DeepSeek 接口接受请求后不返回，reviewer 卡住 15 分钟 |

| `adws/adw_issue.py` + `adws/adw_data/prompt_engineering/issue/{bug,feature,chore,docs}.md` + `just issue`（仅 adws/） | 本项目自有 ADW：GitHub issue 按类型 label 选模板、渲染 `requests/issue-N-<slug>.md`、跑 `adw_simple_sdlc`、push 并 `gh pr create`（标题取 issue 标题，`Closes #N`）；分类是代码不是 prompt；在 base 分支或脏工作区上拒绝启动；测试 `adws/tests/test_adw_issue.py` | 本地需求（Agent Office 接线，ADR 0007），不上游 |

| `adws/adw_modules/runner.py`（仅 adws/） | `Run.listeners`：阶段结束（成功或失败）时回调，抛错的 listener 记录后移除；`adw_issue` 用它把工厂进度写成 issue 下一条原地编辑的评论；测试 `adws/tests/test_phase_listeners.py` | 项目接线，不上游 |
| `adws/adw_modules/quality.py`（仅 adws/） | `test()` 的 argv 改为 `just test`：套件在 justfile 里只定义一次，quality 门与规则 16 同口径（原先只跑 pytest + opt-trader 的 lib.test，issue #7）；测试 `adws/tests/test_quality_gate.py` | 项目接线，不上游 |

## 升级流程

1. 用上游新版本覆盖本目录（保留本文件），`git diff` 检查本地补丁是否已被上游吸收。
2. 生成的 `adws/` 已经按项目 ruff 规则格式化，而模板没有。所以要看 `templates/adws/` 的 diff，再手动合并到 `adws/`，不要用 `install.py --force`。它会覆盖 `sssf.config.yaml` 和 `prompt_engineering/`。
3. 更新本文件的基线 commit。
