# 成语接龙 · Pi Harness

在 Pi 中和 Bot 玩成语接龙：模型提议成语，代码负责规则、计分与对局状态。

使用已配置的 Pi / DeepSeek 环境运行 `just play`。正常游戏中的 Bot、裁判与提示会调用 DeepSeek，按量计费；输入 `/help` 查看命令。

## 求助提示

输入 `/hint` 获取候选。TUI 中「💡 提示」居中浮层捕获键盘焦点，等待你用 ↑↓ 或数字选择、回车确认，Esc 取消；宽度至少 40 列且不超过屏宽 60%（窄屏优先遵守 60% 上限）。底部显示操作说明与剩余次数，空间不足时换行。RPC / JSON / print 模式显示编号卡片，输入候选编号或直接输入成语作答。

选词与手打共用当前难度的裁判和计分：原字 2 分、谐音 1 分，再乘难度倍率；有效入账后 Bot 接所选词的末字。无效时说明原因并返回选择框；取消、无效或超时按跳过时均不扣提示次数，倒计时不暂停。

每局提示上限：简单 3 次、普通 2 次、困难 1 次、极限 0 次；仅有效选词入账消耗 1 次，用完后 `/hint` 提示「本局提示次数已用完」，不调用模型。`/undo` 退回撤销轮次的提示，`/restart` 重置次数，中途换难度按新上限减本局已用次数（最少 0）。仪表盘和 `/status` 显示剩余次数。

## 查看详细状态

输入 `/status` 查看「📊 状态」，详细状态内容不变。TUI 中以居中浮层展示，按任意键关闭，反复查看不再追加对话卡片；RPC / JSON / print 模式仍显示卡片。查看和关闭均 **0 token**，不向模型发送消息，也不改变对局。

## 对局结算

最后一轮 Bot 提交成功或放弃后，自动显示「🏁 对局结束」：总比分与胜负，以及每轮双方的出词和已记账得分（含跳过、超时、使用提示和 Bot 放弃）。TUI 中以浮层展示，按任意键关闭；RPC / JSON / print 模式则追加同样文字的终局卡片。

输入 `/restart` 再来一局，或用 `/rounds <N>` 增加总轮数继续当前对局。查看和关闭结算 **不额外消耗模型 token**，不改变计分或对局状态。

## 回看完整接龙链

输入 `/chain`，对话流中会追加一张「📜 接龙链」卡片，逐行列出本局全部成语：

```text
1. 你：心想事成（+2）
2. Bot：成竹在胸（+2）
```

每行包含序号、出词者、成语及带正负号的已记账步分。空链显示「还没有成语」。查看本身 **0 token**，只给人看，不向模型发送消息，也不改变对局；仪表盘和 `/status` 保持原样。

## 工厂队列

PR 合并、issue 关闭后，下一轮 `just autoqueue` 会清掉残留的 `factory:pr-open`，其他标签不动；`just autoqueue --dry-run` 只预览清理与排队。详见 [工厂标签生命周期](docs/study-notes/factory-labels-guide-20261003-1605.md)。

## TUI 文本截屏

`scripts/tui_capture.py` 是通用截屏引擎，只依赖 Python 标准库；真实运行需要本机安装支持 `extended-keys-format csi-u` 的 tmux，以及场景的启动程序（示例用 Pi）。

```sh
uv run scripts/tui_capture.py --repo . --scenes scripts/tui_scenes.json --out captures
# 等价；第三个参数 repo 默认是当前目录
just tui-capture scripts/tui_scenes.json captures .
```

输出每个场景的 `<场景名>.txt` 和按场景顺序排列的 `manifest.json`（`name`、相对路径 `file`、`ok`、`error`；成功时 error 为 null）。失败仍保存最后一屏并继续其它场景。退出码：全部成功 0，场景或写入失败 1，参数/场景文件不合法或找不到 tmux 为 2。manifest 不含时间戳或耗时。

本项目的场景见 [`scripts/tui_scenes.json`](scripts/tui_scenes.json)：`launch`、`size`、`ready`、`timeout_seconds`、`masks`、`scenes` 全部必填。场景名限不重复的 `[a-z0-9_-]+`；步骤依次执行 `text`（原样输入）、`key`（一个 tmux 键名）、`wait_for`（每 0.2 秒轮询文字，单次等待受 timeout 限制）。先等待 ready，完成步骤后再稳定 0.3 秒截屏；格式错误会在任何截屏前报错。

每个场景使用独立 tmux server、固定尺寸和临时配置，不碰用户 tmux。通过 `-S <场景临时目录>/tmux.sock` 指定 socket，结束时 kill-server 后连同临时目录一起删除，不在 `/tmp/tmux-<uid>/` 留下 socket。pane 用 `env -i`，仅保留 PATH/HOME/TERM 和调用方的 LANG/LC_ALL（都没有则 LANG=en_US.UTF-8），并设置空的 `PI_CODING_AGENT_DIR`、`PI_OFFLINE=1`、`PI_SKIP_VERSION_CHECK=1`、`PI_TELEMETRY=0`；不传 API key 或用户 Pi 配置。**只运行可信场景**：launch 是 shell 命令，这不是限制任意文件/网络访问的安全沙箱。

引擎先将 repo 绝对路径和对应 `~/…` 替换为 `<repo>`，再按顺序应用正则 masks（多行模式）。未指定 replace 时逐字符变成 `#`，中日韩等双宽字符变成 `##`；指定 replace 时是整段匹配的**字面替换**，不展开反向引用。掩码应只匹配行内内容，不要用替换吞掉换行；引擎不额外裁行、去空白，默认掩码保留换行。路径归一化与显式 replace 不保证等宽。分支掩码为 `{"pattern": "(?<=<repo> )\\(.*$", "replace": "(<branch>)"}`，从 `<repo> ` 后的左括号匹配到行尾；即使底栏截断成 `<repo> (factory/iss...`、没有右括号，也统一替换为 `<repo> (<branch>)`。

场景只截不调用模型的 `/status`、`/help`、`/chain`，不截 `/hint`、Bot 回合或结算：离线拿不到模型回复，它们登记在 `sssf.config.yaml` 的 `evidence.tui.uncaptured`，每个 PR 的未验证项都会列出。真实截屏**不加入 `just test`**。

工厂每次 run 末尾的 `tui_capture` phase 用 HEAD 的引擎和场景，分别在基线 checkout 和 HEAD 上各截一次（`evidence.tui`），证据包「界面截屏」一节贴出有变化场景的 before/after，没变化的只列名字。截屏失败只进未验证项，不会让 run 失败。手动复现某次 run 的对比：

```sh
just tui-capture scripts/tui_scenes.json /tmp/head .
git worktree add --detach /tmp/base <基线 sha> && ln -s "$PWD/node_modules" /tmp/base/node_modules
just tui-capture scripts/tui_scenes.json /tmp/before /tmp/base && diff -r /tmp/before /tmp/head
```

## 离线验证

- `just test`：类型检查及全部游戏、工厂、autoqueue、TUI 截屏假运行器测试。
- `just test-tui-capture`：仅截屏引擎离线测试，不启动 tmux/Pi、不调用模型。
- `just test-extensions`：扩展展示与胶水层测试。
- `just test-adws`：工厂测试。
- `uv run pytest`：Python 测试（需要 pytest、pydantic、pyyaml、python-dotenv、rich；工厂测试入口会准备临时依赖环境）。
