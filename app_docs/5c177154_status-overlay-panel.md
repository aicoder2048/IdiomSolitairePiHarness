# `/status` TUI 状态浮层

`/status` 在 TUI 中现在打开标题为「📊 状态」的居中浮层，正文继续使用原有 `statusLines()` 内容。按任意键关闭；反复查看不会向对话流追加状态卡片。RPC、JSON、print 及其它非 TUI 模式仍通过 `pi.appendEntry` 显示原有状态卡片。浮层无法显示时仅发送错误通知，不回退为卡片。查看和关闭不调用模型或发送模型消息。

## 实现位置

- `src/extension/index.ts`：状态命令按 `ctx.mode === "tui"` 分流。TUI 使用现有 `createDismissiblePanel`，设定 `overlay: true`、居中及边距，并按终端宽度调整面板；非 TUI 使用原卡片路径。
- `tests/extension/extension.test.ts`：覆盖默认 fake 与 rpc/json/print（含 UI 开关）的卡片行为，以及 TUI 浮层、正文、关闭、重复查看、失败通知和 0 token 行为；也验证 `/help`、`/chain` 仍写卡片，并调整结算相关状态命令回归测试。
- `README.md`：新增玩家查看状态的说明。
- `AGENTS.md`：更新规则 5，说明 TUI 浮层与非 TUI 卡片的区别，以及不进入模型上下文、不消耗 token。
- `specs/5c177154_status-overlay-panel.md` 与 `requests/issue-12-status-overlay.md`：记录本次需求和实现计划。

## 使用与验证

在 TUI 输入 `/status` 打开面板，按任意键关闭；在 RPC、JSON 或 print 模式输入 `/status`，状态仍以卡片展示。离线验证可运行 `bun test tests/extension/extension.test.ts`，完整验证按项目规则运行 `just test`。