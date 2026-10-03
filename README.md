# 成语接龙 · Pi Harness

在 Pi 中和 Bot 玩成语接龙：模型提议成语，代码负责规则、计分与对局状态。

使用已配置的 Pi / DeepSeek 环境运行 `just play`。正常游戏中的 Bot、裁判与提示会调用 DeepSeek，按量计费；输入 `/help` 查看命令。

## 回看完整接龙链

输入 `/chain`，对话流中会追加一张「📜 接龙链」卡片，逐行列出本局全部成语：

```text
1. 你：心想事成（+2）
2. Bot：成竹在胸（+2）
```

每行包含序号、出词者、成语及带正负号的已记账步分。空链显示「还没有成语」。查看本身 **0 token**，只给人看，不向模型发送消息，也不改变对局；仪表盘和 `/status` 保持原样。

详见 [使用配方](docs/tech-papers/cookbook.md)。

## 离线验证

- `just test`：类型检查及全部游戏、工厂、autoqueue 测试。
- `just test-extensions`：扩展展示与胶水层测试。
- `just test-adws`：工厂测试。
- `uv run pytest`：Python 测试（需要 pytest、pydantic、pyyaml、python-dotenv、rich；工厂测试入口会准备临时依赖环境）。
