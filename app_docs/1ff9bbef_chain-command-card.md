# `/chain` 完整接龙链卡片

新增 `/chain` 只读命令，方便在对话流中回看当前整局的接龙记录。它追加标题为「📜 接龙链」的 `idiom-card`，按顺序逐行显示序号、出词者、成语和已记账步分；分数总带符号（如 `+2`、`-1`、`+0`），空链显示「还没有成语」。展示读取完整链节点，不截断，也不按当前难度重算历史分数。

实现位于 `src/extension/view.ts` 与 `src/extension/index.ts`：纯函数 `chainLines(game)` 负责生成卡片行，命令通过现有 `card()` / `pi.appendEntry()` 路径接入。`chain` 已加入共享 `COMMANDS`，因此 `/help` 会自动列出。该路径不调用模型或 `sendUserMessage`，也不改变对局状态；仪表盘和 `/status` 未作改动。

验证覆盖 `tests/extension/view.test.ts` 中的空链、完整历史、角色、符号、历史步分及纯展示行为；`tests/extension/extension.test.ts` 覆盖命令卡片、零模型副作用、帮助、撤销/重开后的当前链，以及无 UI 情形。可运行 `just test-extensions` 执行扩展测试，或运行 `just test` 执行完整离线测试套件。README 与 `docs/tech-papers/cookbook.md` 提供了使用示例和说明。