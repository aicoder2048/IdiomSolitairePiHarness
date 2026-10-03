# 成语接龙 · Pi Harness

default: check

# 离线测试（不联网、不花钱）
test:
    bun test

typecheck:
    bunx tsc --noEmit

# 类型检查 + 测试
check: typecheck test
