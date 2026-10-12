# IMPLEMENTATION_PLAN — SSSF 证据驱动改进（P1–P5）

借鉴 Ras Mic 的 `evidence-driven-testing`：验收声明要附带**代码产生的证据**，并且送到合并闸门（PR 正文）。
已定的决定：证据只放 PR 正文，不进仓库；红绿证明对 `bug` 硬拦，其它类型只记录；不回馈上游；P5 截屏做成「通用引擎 + 项目配置」。

## 分工

| Stage | 内容 | 谁做 | 原因 |
|---|---|---|---|
| 1–3 | P1 红绿证明、P3 测试完整性、P2 证据包 + P4 未验证项 | 手写 | 评分器，且都在 `protected_files` 里 |
| 4 | P5 截屏引擎 `scripts/tui_capture.py` | 工厂（issue） | 不是评分器，与 `scripts/autoqueue.py` 同类；这次运行同时是 Stage 1–3 的端到端验收 |
| 5 | P5 接线 + 本项目场景配置 | 手写 | `adws/` 受保护 |

## 贯穿全部 stage 的约定

- 证据由代码 phase（`kind="code"`）产生，不新增 agent；`just test` 保持全离线。
- 基线树放在仓库**之外**（`tempfile.mkdtemp()`），否则在仓库里跑 `bun test` 会把基线副本里的测试也扫进去；用完一定要删（`git worktree remove --force` + `prune`），出异常也要删。
- 基线树通过 symlink 共用 HEAD 的 `node_modules`。如果改动新增了依赖，基线上的结果可能失真，这一点记入未验证项。
- 每改一处 envelope，就按 SKILL.md 硬规则 2 同步三处：`data_types.py` 里的类型、对应的 `user.md` 示例、所有调用点。
- 每个 stage：先写测试（红），再实现（绿），然后 `just check`，最后提交一次；同时在 `.claude/skills/sssf/UPSTREAM.md` 的本地补丁表里登记。
- 新函数超过 4 个参数时，改为接收一个数据类型（硬规则 4）。

---

## Stage 1: 基线工作区 + 红绿证明（P1）
**Goal**: 测试变绿之后，代码证明「本次新增或修改的测试在基线上失败、在 HEAD 上通过」。`bug` 不满足就退回 builder，其它类型只记录。

**设计**:
- `adw_modules/baseline.py`：`checkout(run, sha)` 是一个 context manager，在仓库外为 `sha` 建一个 detached worktree，symlink `node_modules`，yield 出路径，退出时删除。
- `adw_modules/proof.py`：
  - `changed_tests(baseline)`：用 tracked diff 加 untracked 文件，按测试文件模式过滤，**以文件为粒度**。被删除的测试文件交给 Stage 2 处理。
  - `prove(run, ProofParams) -> ProofResult`：把每个测试文件的 HEAD 版本复制进基线树，在基线树里跑一次，在仓库里再跑一次，两次的退出码和输出尾部都保存为 artifact。
  - 判定规则：`kind == "bug"` 时，没有任何改动过的测试算失败（「bug 修复必须带复现测试」）；有任何一个文件在基线上没变红也算失败。其它 kind 一律通过，只记录 `red` / `green`。
  - `as_envelope(ProofResult) -> VerifyOutput`：失败时用它把结果交回 builder，复用现有的修复通道。
- 测试文件模式与运行命令是项目专用的，放在 `quality.py` 的 `PROOF_RUNNERS` 里（风格和现有 block 一致），并且可以通过 `ProofParams` 注入：
  - `tests/**/*.test.ts` → `bun test <file>`
  - `tests/test_*.py` → `uv run --no-project --with pytest pytest -q <file>`
  - `adws/tests/test_*.py` → 和 `just test-adws` 相同的 `--with` 依赖列表
- `adw_simple_sdlc.main(prompt, config, adw_id, kind=None)`，CLI 增加 `--kind`；`adw_issue` 传入分类结果。
  - 验证循环改为 `test → (绿) prove`。prove 失败时，builder 进入 `reproduce_i` 补测试，然后回到 test。和修复循环共用 `MAX_FIX_LOOPS` 上限。
  - `retest` 之后再跑一次 prove。
  - 最终 `accepted` 还要求 `proof.passed`。

**Success Criteria**:
- 用一个 bug 型请求跑 `just sdlc --kind bug`，新测试在基线上就通过时，run 不被接受，并且 builder 收到的 envelope 指名了是哪个文件。
- feature 型请求不会因为红绿证明失败。
- 跑完之后，`git worktree list` 里没有残留。

**Tests**（`adws/tests/test_proof.py`，用临时 git 仓库，运行器注入为 `sh` 脚本，不依赖 bun）:
- bug：新测试在基线红、HEAD 绿 → 通过
- bug：测试在基线上就通过 → 失败，消息里带文件名和基线输出
- bug：没有改动任何测试 → 失败
- feature：测试在基线上不红 → 通过，记录 `red=false`
- untracked 的新测试文件会被纳入
- 被删除的测试文件不进入 prove
- 基线树在仓库根目录之外；正常退出和抛异常两种情况下都会被删除
- 4 参数的 `main` 接收 `kind`，`adw_issue` 会把分类结果传下去（扩展 `test_adw_issue.py`）

**Status**: Complete

---

## Stage 2: 测试完整性检查（P3）
**Goal**: 防止 builder 为了变绿而改弱测试。没有声明的改弱退回 builder；声明了的放行，但会在 PR 正文顶部醒目标出。

**设计**:
- `adw_modules/test_integrity.py`：`check(run, baseline_tree, declared) -> IntegrityResult`。
  - 标记：在测试文件的新增行里查 `.skip(`、`.only(`、`.todo(`、`.if(false`、`@pytest.mark.skip`、`@pytest.mark.xfail`、`pytest.skip(`。
  - 删除：检查是否有测试文件被删除。
  - 计数：在基线树和 HEAD 上各跑一次 `bun test`，解析 `Ran N tests`、`M expect() calls`，任何一项下降都算违规。
  - pytest 的用例数这次**不比较**，只查标记，并把这一点写进未验证项。
- 三处同步：`BuildOutput.weakened_tests: list[WeakenedTest{file, reason}]` + builder `user.md` 的 Report 示例 + builder `system.md` 加一条「删除、跳过或放宽测试必须在这里声明原因」。调用点的类型不变。
- 接线位置：
  - `adw_simple_sdlc`：在 prove 之后加 `integrity_i` phase，与 prove 共用同一轮的基线树。
  - `adw_build_test`（`pr-feedback` 用的链）：也接上 integrity，基线取运行开始时的 HEAD；prove 只记录不拦截。

**Success Criteria**:
- 让 builder 在测试里加 `.skip` 却不声明时，run 回到修复循环。
- 声明过的改弱会出现在 integrity 的结果里，供 Stage 3 使用。

**Tests**（`adws/tests/test_test_integrity.py`）:
- 新增 `.skip(` / `.only(` / `@pytest.mark.skip` 各判一次违规
- 删除测试文件判违规
- `expect()` 数量下降判违规；测试数下降判违规
- 声明过的改弱 → 通过，附带警告
- 测试没变 → 通过
- 解析真实的 bun 汇总行（`Ran 210 tests across 9 files.`、`1091 expect() calls`）
- 新增的 `weakened_tests` 字段可以被解析，缺省时为空列表（扩展 envelope 相关测试）

**实施时的偏差**:
- 模块名改为 `adw_modules/integrity.py`（`test_*.py` 形状的模块名会被 pytest 当成测试收集），测试文件为 `adws/tests/test_integrity.py`；签名为 `check(run, IntegrityParams) -> IntegrityResult`。
- 不与 prove 共用基线树：prove 会把 HEAD 的测试文件拷进它的树，计数必须在干净的基线上跑，所以 integrity 自己 checkout 一次（只在计数器覆盖的测试文件有改动时）。
- 标记另加了 `.skipIf(`、`.todoIf(`、`unittest.skip`；用例数下降是全套件的，任何一条声明都能放行它。
- 真实验证：在 `tests/engine/context.test.ts` 加 `test.skip` 并删一条 expect，抓到标记，且 `expect()` 1091→1089（bun 的 `Ran N tests` 含被跳过的测试，所以掉的是 expect 数）；声明后两条都放行。

**Status**: Complete

---

## Stage 3: 证据包、未验证项与 PR 正文（P2 + P4）
**Goal**: 代码拼出 `context_handoff/evidence.md` 作为 PR 正文；`pr-feedback` 的回复也带上证据。

**设计**:
- `adw_modules/evidence.py`：纯函数 `render(EvidenceInput) -> str`，加 `write(run, EvidenceInput) -> Path`。各节如下，缺失的节写「（本次未运行）」，不能省略：
  1. 结论：run 是否被接受
  2. 版本：branch、基线 sha、HEAD sha
  3. 改了什么：diff stat
  4. 怎么验证的：每项检查列出命令、退出码、耗时和摘要（如 `210 pass 0 fail`）
  5. 红绿证明：每个文件在基线和 HEAD 上的退出码与输出尾部
  6. 测试完整性：用例数变化、标记、声明（声明过的改弱用 ⚠️ 置顶）
  7. 新增测试名：从新增行里抓 `test("…")`、`it("…")`、`def test_…`
  8. Reviewer 逐条：需求 / 是否满足 / 证据（单元格里的 `|` 要转义）
  9. 未验证项
  10. 成本：tokens / $
- 未验证项有三个来源：
  - 配置：新增 `evidence:` 段，即 `EvidenceConfig.unverified`；本项目填「未运行 `just smoke`（按量计费）」
  - Reviewer：三处同步 `ReviewOutput.unverified: list[str]` + reviewer `user.md` 示例 + `system.md`「列出你无法验证的需求及原因」
  - 代码自动生成：feature 没有红绿证明、pytest 用例数未比较、依赖变动导致基线可能失真
- `adw_simple_sdlc` 在最后加一个 `evidence` phase，`commit_docs` 之后运行；没被接受的 run 也写，供进度评论引用。
- `adw_issue.open_pr` 的正文改为 `Closes #N` + evidence.md，超过 60k 字符时截断，并注明 session 路径。
- `adw_pr_feedback.reply` 在 builder 说明之后附上 evidence。
- 文档：
  - SKILL.md 加硬规则 11：「验收声明必须附带代码产生的证据，证据进 PR 正文」
  - AGENTS.md 规则 12 补一句：PR 正文就是工厂的证据包
  - UPSTREAM.md 登记

**Success Criteria**:
- 本地跑 `just issue N --no-pr` 后，session 里生成 evidence.md，10 节齐全。
- `open_pr` 的正文以 `Closes #N` 开头，后面就是 evidence.md 的内容。

**Tests**（`adws/tests/test_evidence.py`，并扩展 `test_adw_issue.py`、`test_adw_pr_feedback.py`）:
- 输入完整时 10 节都在
- 缺失的节显示「（本次未运行）」
- 截断时附带说明
- 表格里的 `|` 被转义
- 声明过的改弱出现在最前面
- PR 正文和反馈回复里包含证据

**Status**: Not Started

---

## Stage 4: TUI 截屏引擎（P5 L1+L2，由工厂开发，同时做端到端验收）
**Goal**: 开一个 `enhancement` issue，打上 `factory:queued`，由 `just autoqueue` 开发 `scripts/tui_capture.py`。这次运行本身就是 Stage 1–3 的验收。

**Issue 要点**（来自 spike 实测）:
- CLI：`uv run scripts/tui_capture.py --repo <dir> --scenes <file> --out <dir>`，每个场景输出一个 `<scene>.txt`，外加一个 `manifest.json`。
- 隔离：用 `env -i` 只放行 `PATH` / `HOME` / `TERM`，另设空的 `PI_CODING_AGENT_DIR`、`PI_OFFLINE=1`、`PI_SKIP_VERSION_CHECK=1`、`PI_TELEMETRY=0`。
- tmux：每次用唯一的 `-L` socket，配置文件里设 `extended-keys on` 和 `extended-keys-format csi-u`，固定 `-x/-y` 尺寸。
- 等待：轮询等标记出现（不用固定 sleep），超时就报错；出现后再等 0.3s 让画面稳定。
- 场景用按键序列描述；掩码逐位替换，保持宽度不变，**绝不删行**；Pi 底栏的 cwd 路径也要掩码。
- 无论成功还是失败，都要清理 tmux server。
- 离线单元测试放 `tests/test_tui_capture.py`，注入假的 tmux 运行器，覆盖掩码保宽、env/argv 构造、场景解析、超时；加入 `just test`。真实运行走 `just tui-capture`，不加入 `just test`。

**Success Criteria**（逐条对照工厂开出的 PR）:
- PR 正文就是证据包，10 节齐全
- 红绿证明记录了新测试在基线上为红（模块不存在）、在 HEAD 上为绿；kind 是 feature，所以只记录不拦截
- 测试完整性显示用例数没有下降
- 未验证项如实列出
- 在 PR 上留一条意见并打上 `factory:revise`，回复里同样带证据
- 任何一项不达标：回到 Stage 1–3 手工修，再让工厂重跑

**Tests**: 由工厂写（见上），人工合并前审查。

**Status**: Not Started

---

## Stage 5: 截屏接线 + 本项目场景（P5 L3）
**Goal**: 证据包里多一节「界面截屏」，只贴有变化的场景，并列出 before/after。

**设计**:
- 配置 `evidence.tui`：`launch`、`size`、`ready`、`masks`、`scenes`（`status`、`help`、`chain`），以及 `uncaptured`（结算画面、有内容的接龙链、`/hint` 选择框，原因都是需要 Bot 回合）。
- `adw_simple_sdlc` 增加 `tui_capture` 这个 code phase：对基线树和 HEAD 各跑一次 `just tui-capture`（走子进程边界，`adws/` 不 import `scripts/`），按场景做 diff。
  - 截屏失败只写进未验证项（「截屏失败：…」），**不会让 run 失败**。截屏是证据，不是 gate。
  - 没有配置 `evidence.tui` 时跳过这一 phase，并注明「本项目未配置 TUI 截屏」。
- evidence 增加一节：有变化的场景贴 before/after 代码块，没变化的写「N 个画面无变化」；`uncaptured` 里的条目进入未验证项。
- 文档：README 写 `just tui-capture` 的用法；UPSTREAM.md 登记；删除本文件。

**Success Criteria**:
- 拿 #12 的改动（基线 `cfb6326` vs `a0a395d`）跑一遍，能复现 spike 的结果：`status` 场景出现 before 卡片 / after overlay，`help` 场景无变化。
- 连跑 3 次，结果逐字节相同。

**Tests**（`adws/tests/test_tui_evidence.py`）:
- 用假的引擎输出测：有变化 / 无变化 / 截屏失败 / 未配置 四种情况
- evidence 渲染 before/after 代码块
- `uncaptured` 的条目进入未验证项

**Status**: Not Started

---

## 不在本计划内（以后再说）

- 假模型服务：用来截取需要 Bot 回合的画面，需要另做 spike
- 给 OptionTradingPiHarness 写 L3 配置，验证引擎的通用性
- 把这些改动合进 `.claude/skills/sssf/templates/`
- 推送前先 rebase 到最新的 `origin/main`
