# 成语接龙使用配方

## 用 `/chain` 回看本局

1. 在已配置 Pi / DeepSeek 的环境中运行 `just play`。
2. 输入「心想事成」，等待 Bot 接龙。正常出词会调用裁判与 Bot 模型，按量计费。
3. 输入 `/chain`。若 Bot 接的是「成竹在胸」，普通难度下会在对话流看到：

   ```text
   📜 接龙链
   1. 你：心想事成（+2）
   2. Bot：成竹在胸（+2）
   ```

序号从 1 开始，按链中出词顺序排列；「你 / Bot」表示出词者，括号是该步已记账的得分（正数带 `+`，负数带 `-`，零为 `+0`）。切换难度不会重新计算历史步分。Bot 尚未完成时，人类已入链的成语也会显示。

即使超过仪表盘的 6 个节点，卡片仍逐行展示完整链，不截断。空链显示「还没有成语」。`/undo` 撤销整轮或 `/restart` 重开后，再执行 `/chain` 展示的是当前链，不含已撤销或上一局的节点。

`/chain` 本身不调用模型（0 token）、不发送模型消息，也不改变对局状态。仪表盘和 `/status` 的展示不变；无 UI 的 RPC 模式同样会追加卡片 entry。

### 维护入口

`src/extension/view.ts` 中的 `COMMANDS` 同时用于注册说明和 `/help`。展示路径为 `COMMANDS → chainLines(game) → card → pi.appendEntry("idiom-card", ...)`：纯函数读取完整 `chain.turns`，复用现有卡片渲染器，不进入模型回合。

回归验证：`just test-extensions`；全部离线检查：`just test`。
