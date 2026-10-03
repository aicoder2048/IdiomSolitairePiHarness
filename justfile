# 成语接龙 · Pi Harness

set dotenv-load := true

model := env("DEEPSEEK_MODEL", "deepseek-flash")

# 只加载本扩展：不带内置工具、skills、模板、AGENTS.md，不落盘 session
game_flags := "-ne -nbt -ns -np -nc --no-session --thinking off -e ./src/extension/index.ts"

default: check

# 开一局（Bot 用 deepseek/$DEEPSEEK_MODEL，按量计费）
play:
    pi {{game_flags}} --model deepseek/{{model}}

# 离线测试（不联网、不花钱）
test:
    bun test

typecheck:
    bunx tsc --noEmit

# 类型检查 + 测试
check: typecheck test

# 真实冒烟：RPC 模式跑两回合（会调用 DeepSeek，产生少量费用）
smoke:
    bun run scripts/smoke.ts
