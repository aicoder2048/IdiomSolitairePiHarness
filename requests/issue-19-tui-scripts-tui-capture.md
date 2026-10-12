Implement GitHub issue #19: "TUI 截屏引擎：scripts/tui_capture.py" (https://github.com/aicoder2048/IdiomSolitairePiHarness/issues/19). The issue and its comments are quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a FEATURE — new behaviour, or existing behaviour made better:
- Plan before building: the plan names the files, the data flow and the tests, and the builder follows it.
- New behaviour comes with tests that describe it. Existing tests keep passing unchanged, unless the issue changes what they test.
- Document it in the same change: README.md (player-facing: how to play, commands) and AGENTS.md when it adds a rule.
- Where the issue leaves a choice open, take the simplest option that satisfies it and record the choice in the plan.

Where: the files the issue names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point under the issue's own "Done means" holds; tests cover the new behaviour; `just test` passes; README/docs describe what changed.
Out of scope: anything the issue does not ask for; redesigns of neighbouring code.

## Issue #19 as filed

## 背景
工厂的证据包目前只有文字：命令、退出码、红绿证明、reviewer 核对。界面改动（overlay、卡片、底栏）是否真的变了，只能人自己开 Pi 看。要做一个**通用的** TUI 截屏引擎：在隔离的 tmux 里启动 TUI，按场景发按键，等画面出现后把屏幕抓成文本，掩掉每次都会变的部分，让同一份代码连跑几次结果逐字节相同。之后会把它接进工厂，给同一场景的 before/after 做 diff，但这个 issue 只做引擎本身。

引擎不认识本项目：启动命令、尺寸、就绪标记、掩码、场景都来自场景文件。

## 要做的
新建 `scripts/tui_capture.py`，只用标准库（和 `scripts/autoqueue.py` 一样）：

```
uv run scripts/tui_capture.py --repo <dir> --scenes <file.json> --out <dir>
```

每个场景在 `--out` 下写一个 `<场景名>.txt`，最后写 `manifest.json`。

### 场景文件（JSON）
```json
{
  "launch": "pi -ne -nbt -ns -np -nc --no-session --thinking off -e ./src/extension/index.ts --model deepseek/deepseek-flash",
  "size": [100, 30],
  "ready": "成语接龙开始",
  "timeout_seconds": 10,
  "masks": [
    {"pattern": "(?<=⏱ )\\d+"},
    {"pattern": "(?<=本轮剩 )\\d+"},
    {"pattern": "(?<=<repo> \\()[^)]*(?=\\)$)", "replace": "<branch>"}
  ],
  "scenes": [
    {"name": "status", "steps": [{"text": "/status"}, {"key": "Enter"}, {"wait_for": "📊 状态"}]},
    {"name": "help", "steps": [{"text": "/help"}, {"key": "Enter"}, {"wait_for": "📖 成语接龙"}]}
  ]
}
```

- `steps` 按顺序执行。`text` 原样输入（`tmux send-keys -l`），`key` 发一个 tmux 键名（`Enter`、`Escape`、`Up`…），`wait_for` 轮询屏幕，直到出现这段文字。
- 场景名只允许 `[a-z0-9_-]+`，不允许重名。文件格式不对就直接报错退出，不做任何截屏。
- 把这个文件提交为 `scripts/tui_scenes.example.json`，内容就是上面的例子。

### 每个场景怎么跑（下面都来自 spike 实测）
1. **隔离**：每个场景用一个新的 tmux server，socket 名唯一（`tmux -L <唯一名>`，加 `-u`），尺寸固定为 `-x/-y`，工作目录是 `--repo`。不碰用户的 tmux。
2. **tmux 配置**：用一个临时配置文件（`-f`），里面写 `set -g extended-keys on` 和 `set -g extended-keys-format csi-u`。不加的话，Pi 会在屏幕上打出 extended-keys 警告，画面就变了。
3. **环境**：pane 里的命令用 `env -i` 启动，只放行 `PATH`、`HOME`、`TERM`、`LANG`/`LC_ALL`（调用方有才放，否则 `LANG=en_US.UTF-8`），另外设 `PI_CODING_AGENT_DIR=<空的临时目录>`、`PI_OFFLINE=1`、`PI_SKIP_VERSION_CHECK=1`、`PI_TELEMETRY=0`。这样拿不到任何 API key，也读不到用户的 Pi 配置，截屏不可能调用模型。
4. **等待**：先等 `ready`，再按顺序执行 `steps`。每次 `wait_for` 每 0.2s 抓一次屏，直到出现标记。超过 `timeout_seconds` 就判这个场景失败，错误信息里带上最后一屏的内容。**不要用固定 sleep 来等。** 所有步骤做完后再等 0.3s，让画面稳定，然后 `capture-pane -p`。
5. **掩码**：
   - 先把 `--repo` 的绝对路径和它的 `~/…` 写法替换成 `<repo>`（Pi 底栏会显示 cwd；基线树和 HEAD 树的路径不一样）。
   - 然后按顺序应用 `masks`：有 `replace` 的，用它替换整段匹配；没有的，匹配到的每个字符换成 `#`，双宽字符（`unicodedata.east_asian_width` 是 W/F）换成 `##`，保证宽度不变，边框还能对齐。
   - **绝不删行，也不删字符。**
6. **清理**：不管成功、失败还是超时，都要 `kill-server`，并删掉临时目录和配置文件（用 `try/finally`）。

### manifest 和退出码
- `manifest.json`：`{"scenes": [{"name", "file", "ok", "error"}]}`，按场景文件里的顺序排。不要写时间戳或耗时，manifest 也要逐字节可复现。
- 一个场景失败不影响其它场景，照样会写 manifest。
- 退出码：全部成功是 0；有场景失败是 1；参数或场景文件不对、或者找不到 `tmux`，是 2。

### just
- `just tui-capture scenes out repo="."`：真实运行，需要本机有 tmux 和 pi。**不加入 `just test`。**
- 离线测试放 `tests/test_tui_capture.py`，加进 `just test`，写法参照 `test-autoqueue` 那个 recipe。

## 离线测试（不能真起 tmux）
往 `tests/test_tui_capture.py` 里注入一个假的 tmux 运行器，它记录收到的 argv，并按脚本返回屏幕内容。至少测这些：
- 掩码保宽：数字逐位变成 `#`；双宽字符变成 `##`；`replace` 生效；行数不变；`<repo>` 替换同时覆盖绝对路径和 `~/` 写法。
- argv 和 env：每个场景的 socket 唯一，带 `-u`、`-f` 和 `-x/-y`；pane 命令以 `env -i` 开头，只带上面列出的变量，**不带** `DEEPSEEK_API_KEY` 这类调用方环境里有的变量。
- 场景解析：缺字段、场景名非法、重名、未知的步骤类型，都会报错，退出码 2。
- 等待：标记第 N 次轮询才出现时能等到；一直不出现就超时，场景判失败，错误里带最后一屏，其它场景照常跑，退出码 1。
- 清理：场景成功和超时两种情况下都调用了 `kill-server`。
- manifest：顺序和字段正确，同样的输入跑两次，结果逐字节相同。

## 验收标准
- `just test` 通过。
- `uv run scripts/tui_capture.py --repo . --scenes scripts/tui_scenes.example.json --out <dir>` 在装了 tmux 的机器上能产出 `status.txt`、`help.txt` 和 `manifest.json`，连跑 3 次逐字节相同。这一条由人在合并前验证，工厂不跑。

## 不做的
- 不接进 ADW 或证据包，不做 before/after diff（后续再做）。
- 不截需要 Bot 回合的画面（`/hint` 选择框、结算画面）：离线拿不到模型回复。
- 不改 `src/`。

## Comments

(no comments)
