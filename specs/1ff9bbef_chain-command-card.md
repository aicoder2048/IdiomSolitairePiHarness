# Issue #1：新增 `/chain` 完整接龙链卡片

## 目标与边界

新增只读、确定性的 `/chain` 斜杠命令，通过现有 `idiom-card` / `pi.appendEntry()` 在对话流中逐行展示本局完整接龙链。每行包括从 1 开始的序号、出词者（你 / Bot）、成语和带符号的该步得分；空链显示 `还没有成语`。命令列入 `COMMANDS`，由 `/help` 自动展示。不调用模型，不调用 `sendUserMessage`。

不修改仪表盘、`/status`、游戏规则、计分、模型上下文或引擎。不要引入新依赖、模型调用、分页或新的卡片渲染器。

## 已确认的实现位置与数据流

- `src/engine/context.ts` 的 `ChainHistory.turns` 保存完整的 `{ player, idiom, score }` 数组；只有 `recentIdioms()` 裁剪模型视野。
- `src/engine/game.ts` 在合法人类出词时立即写入链，在 Bot 成功结算时写入 Bot 出词；`score` 已包含当时的倍率。跳过、超时、提示和失败候选不构成成语链节点。撤销和重新开始已经修改当前链。
- `src/extension/view.ts` 包含纯展示函数、共享命令表和自动生成帮助的逻辑。现有 `signed()` 对 0 输出 `0`，不要改变它而影响其他卡片。
- `src/extension/index.ts` 的 `command()` 注册命令；`card()` 调用 `pi.appendEntry("idiom-card", { title, lines })`，现有 renderer 显示这些行。`/status` 是直接复用的接入模式。
- 测试用 `tests/fakes.ts` 的 `FakeLLM` / `FakeClock` 和 `tests/extension/fake-pi.ts` 的 `FakePi`；已有 `entries`、`cards()`、`userMessages` 可直接断言，不需要新增替身机制。

数据流：玩家 `/chain` → 现有命令注册处理器 → `view.chainLines(game)` 读取 `game.chain.turns` → `card(lines, "📜 接龙链")` → `pi.appendEntry`。这是展示路径，不经过 `report()`、`startBotTurn()`、模型或状态写入。

## 明确的产品选择

1. 导出 `chainLines(game: IdiomGame): string[]`，与现有展示函数风格一致。
2. 非空时每个节点恰好一行，格式固定为 `1. 你：心想事成（+2）`、`2. Bot：成竹在胸（+2）`。卡片标题为 `📜 接龙链`，行数组中不另加表头。
3. 正数加 `+`，负数保留 `-`，0 用 `+0`，满足显式符号要求。在新函数内格式化，不改共享 `signed()` 的现有行为。
4. 空链精确返回 `["还没有成语"]`。
5. 使用全部 `turns`，不使用轮次日志、`recentIdioms()`、仪表盘文本或任何截断。序号是链节点序号，不是轮次；出词者从 `turn.player` 读取，不根据序号奇偶推断。
6. 直接展示已记账 `turn.score`，不按当前难度重新计算。包括 Bot 尚未完成时已经入链的人类出词。查看当前对局，不拼接已撤销或上一局记录。
7. 新命令不需要参数，不依赖 `ctx.hasUI`；RPC / 无 widget 时仍然追加 entry。现有渲染器负责文本显示，不实现宽度计算。

## 文件与具体改动

### 1. 先写测试（红灯）

**`tests/extension/view.test.ts`**

导入 `chainLines`，增加以下单元测试：

- 空链返回精确空提示。
- 正常人类 / Bot 一轮的精确两行（序号、角色、成语、`+2`）；可用现有 `make()` 和异步提交构造。
- 完整历史不截断：用 `chain.addTurn()` 构造至少 12 个唯一测试节点，超过仪表盘 6 个和默认模型视野 10 个限制，断言整个输出数组及首尾顺序；包含相邻同一角色，证明不按序号猜角色。
- 用链节点直接构造 `+4`、`-1`、`+0` 的格式测试，说明负数 / 零是展示边界 fixture，不是修改现行合法成语计分规则。
- 历史分数不随难度变化：简单难度成功出词得到 `+4`，完成该轮后改回普通，展示仍是当时分数。
- 人类刚提交、Bot 尚未出词时，链行已包含人类节点（不能只从 `roundLog` 取数据）。
- 纯函数：调用前后链节点内容和对局关键状态相同，多次调用输出相同。
- 在现有“帮助列出全部命令”的显式命令列表中加入 `/chain`。

**`tests/extension/extension.test.ts`**

- 在现有“确定性命令 0 token”的命令列表中加入 `["chain", ""]`；保留原断言，可补充该组 `pi.userMessages` 为空的断言。
- 独立 `/chain` 空链测试：恰好追加一个 `idiom-card` entry，标题 `📜 接龙链`、lines 为 `["还没有成语"]`；`llm.calls` 和 `pi.userMessages` 均为空。
- 非空链测试：通过 `pi.input()` / `pi.submit()` 完成一轮，记录调用数与 entries 数后调用 `/chain`；精确断言新增卡片的两行与类型，模型调用数不增加，`userMessages` 不增加。准备数据期间的裁判调用不算命令调用。
- `/help` 实际命令产生的卡片包含 `/chain`。
- 用现有命令撤销一整轮、重新开始后分别查看 `/chain`，确认显示当前链（空提示），不保留旧记录。
- 无 UI 测试：临时将 fake context 的 `hasUI` 设为 false（可用 `Object.assign`），执行 `/chain` 仍追加卡片、无模型调用或用户消息；不改 FakePi 默认行为。

先运行 `bun test tests/extension/view.test.ts tests/extension/extension.test.ts` 并确认新增功能测试以非零退出状态失败；不要调整无关旧测试来掩盖失败。

### 2. 最小实现（绿灯）

**`src/extension/view.ts`**

- 在 `COMMANDS` 的 `status` 附近加 `chain: ["", "查看完整接龙链"]`。
- 在状态 / 帮助展示函数附近添加纯函数 `chainLines`。空数组返回空提示，否则单次 `map` 全部节点并格式化。
- 不修改 `boardLines`、`statusLines`、既有分数格式工具或 `helpLines` 的生成机制。

**`src/extension/index.ts`**

- 在 `status` / `help` 注册附近增加 `command("chain", () => card(view.chainLines(game), "📜 接龙链"));`。
- 复用现有 `view` namespace、card helper 和 renderer，不改任何生命周期、工具或模型相关路径。

### 3. 文档（同一改动）

仓库当前没有根 `README.md`，也没有 `docs/tech-papers/` 或其中的 cookbook；`docs/README.md` 是 Pi 文档镜像说明，不要把新功能塞到上游镜像文档中。

**新增 `README.md`**

- 简短中文项目介绍，现有 `just play` 入口与模型按量计费提示。
- 描述 `/chain` 是零 token、仅给人看的完整历史卡片，展示两行实例和空链文案，说明不会改变仪表盘或 `/status`。
- 链接下述 cookbook；列出离线测试入口。

**新增 `docs/tech-papers/cookbook.md`**

- 添加聚焦的“用 `/chain` 回看本局”配方：运行游戏、正常接龙、输入 `/chain`，预期标题和逐行输出。
- 解释每行的序号、你 / Bot、成语、已记账步分；即使超过 6 个节点也完整展示，空链显示 `还没有成语`。
- 说明查看链本身不启动模型，不改变对局；撤销 / 重开后显示当前链。不要暗示正常游戏提交也不调用模型。
- 可用一小段说明维护模式 `COMMANDS → chainLines → card → appendEntry`，不扩写无关架构文章。

### 4. 满足请求中的验证入口

**`justfile`**

本任务明确要求 `just test-extensions`，但仓库目前没有这个 recipe。仅新增离线入口：

```just
# 扩展展示与胶水层测试，离线
 test-extensions:
     bun test tests/extension
```

实际文件中 recipe 名顶格、命令沿用现有缩进。保持 `test`、`typecheck`、`test-adws`、`test-autoqueue` 的原有行为不变；不重构测试系统。

## 验证与完成条件

实现后按退出状态判断命令成败，不按输出中是否出现 `error` 等字词判断。

1. `bun test tests/extension/view.test.ts tests/extension/extension.test.ts`
2. `just test-extensions`
3. `uv run pytest`
4. `just test-adws`
5. `just test`（包含类型检查、所有 bun 测试、工厂 Python / Node 测试和 autoqueue 测试）

当前无 `pyproject.toml`，工厂 recipe 通过 uv 临时依赖环境执行。先按要求直接运行 `uv run pytest`，沿用 operator 环境。如果缺少 Python 测试依赖，使用现有 `test-adws` recipe 中的依赖集合（pytest、pydantic、pyyaml、python-dotenv、rich）准备临时环境再执行原命令，例如 `uv run --no-project --with pytest --with pydantic --with pyyaml --with python-dotenv --with rich uv run pytest`；记录实际执行方式，不为这个功能新增 Python 项目配置，也不把未通过的 gate 写成通过。

不运行联网 `just smoke`，不读取密钥，不调用 `gh`。手动 TUI 游戏不是完成此功能的必要验证。

完成检查：

- `/chain` 从共享命令表注册且 `/help` 展示它。
- 一张与 `/status` 相同类型的 appendEntry 卡片，完整有序行与空链文案正确。
- 纯函数与扩展级测试覆盖格式、完整性、已记账分数以及零模型 / 零消息副作用。
- 仪表盘和 `/status` 代码及其既有测试不变。
- README 与 cookbook 均包含实际使用说明。
- 所有要求的离线 gate 成功；保留其退出状态证据。

## 交接说明

本计划阶段只做了只读代码检查与计划产出，未实现功能，未运行测试。无需子 agent；相关实现集中在两个扩展文件。`specs/` 已列出并确认尚不存在，本计划的仓库副本使用 `specs/1ff9bbef_chain-command-card.md`，不得覆盖其他计划记录。
