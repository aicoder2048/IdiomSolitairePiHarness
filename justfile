# 成语接龙 · Pi Harness，以及开发它的 SSSF 软件工厂

# `.env` 进入每个 recipe：游戏读 DEEPSEEK_*；工厂的模型认证在 ~/.pi/agent/auth.json
set dotenv-load := true
set positional-arguments

model := env("DEEPSEEK_MODEL", "deepseek-flash")

# 只加载本扩展：不带内置工具、skills、模板、AGENTS.md，不落盘 session
game_flags := "-ne -nbt -ns -np -nc --no-session --thinking off -e ./src/extension/index.ts"

# Every factory recipe passes this through, so `SSSF_CONFIG=other.yaml just sdlc "..."` swaps the roster.
config := env_var_or_default("SSSF_CONFIG", "adws/adw_sssf_config/sssf.config.yaml")
db := "adws/adw_data/sssf.db"

# list every recipe
default:
    @just --list

# ── 游戏 ────────────────────────────────────────────────────────────────────

# 开一局（Bot 用 deepseek/$DEEPSEEK_MODEL，按量计费）
play:
    pi {{game_flags}} --model deepseek/{{model}}

# 真实冒烟：RPC 模式跑两回合（会调用 DeepSeek，产生少量费用）
smoke:
    bun run scripts/smoke.ts

# ── 测试与检查 ──────────────────────────────────────────────────────────────

# every suite, offline (also the factory's quality gate: adw_modules/quality.py runs `just test`)
test:
    just typecheck
    bun test
    just test-adws
    just test-autoqueue

# 扩展展示与胶水层测试，离线
test-extensions:
    bun test tests/extension

typecheck:
    bunx tsc --noEmit

# the factory's Python: ruff check + format check
lint:
    uvx ruff check adws scripts tests
    uvx ruff format --check adws scripts tests

# lint + every suite
check: lint test

# the factory's own tests — separate env, the adws need pydantic
test-adws:
    uv run --no-project --with pytest --with pydantic --with pyyaml --with python-dotenv --with rich pytest adws/tests -q
    node --test adws/tests/dev_guard.test.ts

# the unattended issue runner: real local git, canned GitHub
test-autoqueue:
    uv run --no-project --with pytest pytest tests/test_autoqueue.py -q

# ── 软件工厂：跑一个 workflow ───────────────────────────────────────────────
# Args pass straight through: "<prompt or path/to/prompt.md>" [--adw-id X]

# one agent, one prompt: just prompt --agent scout "summarize this repo"
prompt *ARGS:
    uv run adws/adw_prompt.py --config {{config}} "$@"

# read-only recon: just scout "where is the round prompt built"
scout *ARGS:
    uv run adws/adw_scout.py --config {{config}} "$@"

# plan only: just plan "add a /history command"
plan *ARGS:
    uv run adws/adw_plan.py --config {{config}} "$@"

# plan, build, test, commit: just sdlc "add a /history command"
sdlc *ARGS:
    uv run adws/adw_plan_build_test.py --config {{config}} "$@"

# the full chain, plus review and docs: just simple-sdlc "add a /history command"
simple-sdlc *ARGS:
    uv run adws/adw_simple_sdlc.py --config {{config}} "$@"

# a GitHub issue, by its type label, through simple-sdlc and into a PR: just issue 42 [--kind bug] [--no-pr] [--dry-run]
issue NUMBER *ARGS:
    uv run adws/adw_issue.py --config {{config}} "$@"

# review comments on a factory PR, through build + test, back onto the PR: just pr-feedback 5 [--check] [--dry-run]
pr-feedback NUMBER *ARGS:
    uv run adws/adw_pr_feedback.py --config {{config}} "$@"

# ── 软件工厂：无人值守队列 ─────────────────────────────────────────────────

# issues labelled factory:queued, one at a time, each in its own worktree (main checkout only)
autoqueue *ARGS:
    uv run --no-project python scripts/autoqueue.py "$@"

# factory PRs labelled factory:revise, one at a time, each in a worktree of its branch (main checkout only)
autoqueue-feedback *ARGS:
    uv run --no-project python scripts/autoqueue.py feedback "$@"

# print a cron line only; never install: just autoqueue-cron [MINUTES]
autoqueue-cron MINUTES="30":
    uv run --no-project python scripts/autoqueue.py cron "$@"

# ── 软件工厂：观察 ─────────────────────────────────────────────────────────
# Reads never block a running workflow, the db is WAL.

# the last 10 runs
sessions:
    @sqlite3 {{db}} "select adw_id, status, substr(request,1,50), total_tokens, round(total_cost,4) from sessions order by started_at desc limit 10;"

# phase status in sequence: just phases <adw_id>
phases ADW_ID:
    @sqlite3 {{db}} "select seq, name, kind, owner, status, attempt from phases where adw_id='{{ADW_ID}}' order by seq;"

# the live event tail: just tail <adw_id>
tail ADW_ID:
    @sqlite3 {{db}} "select rowid, type, name, started_at from events where adw_id='{{ADW_ID}}' order by rowid desc limit 25;"

# what a run has alive right now, with pids: just procs <adw_id>
procs ADW_ID:
    @sqlite3 {{db}} "select kind, name, pid, command, started_at from processes where adw_id='{{ADW_ID}}' and ended_at is null order by id;"

# boot the trace UI, http://localhost:4601 (api on :4600); needs bun
obs:
    cd .claude/skills/sssf/apps/visualizer && bun install && (SSSF_DB={{justfile_directory()}}/{{db}} bun run server/index.ts &) && bunx vite
