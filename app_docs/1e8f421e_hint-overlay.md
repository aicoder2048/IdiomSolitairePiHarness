# `/hint` 候选 TUI 浮层

成功的 `/hint` 在 TUI 中改为显示可关闭的「💡 提示」浮层：候选逐行展示，末行提示「本轮 0 分，Bot 接龙中…」。按任意键关闭；面板仅负责展示，命令不会等待关闭才启动 Bot。提示仍只调用一次提示模型，游戏仍照常开新回合并发送 Bot 回合 prompt。

实现位于 `src/extension/index.ts`：只在 `ctx.mode === "tui"` 且存在候选时调用 `ctx.ui.custom(..., { overlay: true })`，其余模式继续写原有提示卡片。`src/extension/panel.ts` 提供静态面板组件，按可见终端宽度截断文本，并通过 `done()` 关闭。浮层创建失败只发送错误通知，不改变游戏流程。提示生成、候选过滤及其它命令未改。

`tests/extension/fake-pi.ts` 可设置运行模式并记录浮层调用；`tests/extension/extension.test.ts` 覆盖 TUI 展示、非 TUI 卡片回退、Bot 流程及失败情形，`tests/extension/panel.test.ts` 覆盖内容、任意键关闭和窄宽度渲染。玩家用法见 `README.md`；TUI 输出例外规则记在 `AGENTS.md`。

验证：运行 `just test`。离线测试中，TUI 模式通过 fake `ui.custom` 断言 overlay 配置并驱动真实面板工厂；RPC、JSON、print 模式验证保留原卡片。