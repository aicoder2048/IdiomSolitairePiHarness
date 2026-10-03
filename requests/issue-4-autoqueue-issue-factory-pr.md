Implement GitHub issue #4: "autoqueue：每轮开始时清掉已关闭 issue 上残留的 factory:pr-open" (https://github.com/aicoder2048/IdiomSolitairePiHarness/issues/4). The issue and its comments are quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a FEATURE — new behaviour, or existing behaviour made better:
- Plan before building: the plan names the files, the data flow and the tests, and the builder follows it.
- New behaviour comes with tests that describe it. Existing tests keep passing unchanged, unless the issue changes what they test.
- Document it in the same change: README.md (player-facing: how to play, commands) and AGENTS.md when it adds a rule.
- Where the issue leaves a choice open, take the simplest option that satisfies it and record the choice in the plan.

Where: the files the issue names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point under the issue's own "Done means" holds; tests cover the new behaviour; `just test` passes; README/docs describe what changed.
Out of scope: anything the issue does not ask for; redesigns of neighbouring code.

## Issue #4 as filed

## 背景
`scripts/autoqueue.py` 把 issue 推进到 `factory:pr-open` 后就不再管它。PR 合并后 GitHub 自动关闭 issue，但 `factory:pr-open` 标签留在已关闭的 issue 上，看起来像"还在等审"（#1 就是这样，后来手工清掉的）。

## 要做的
在 `just autoqueue`（issue 通道）每一轮开始、拿到锁并 `git fetch` 之后，挑候选之前，加一步清理：

1. 找出**已关闭**且带 `factory:pr-open` 的 issue：用现有的 `listing()` 助手，`gh issue list --state closed --label factory:pr-open --json number`（`listing()` 会自动加 `--limit`）。
2. 对每个这样的 issue 执行 `gh issue edit N --remove-label factory:pr-open`，用现有的 `mutation()` 助手，按编号从小到大。
3. 每清一个，向 stdout 打一行 `cleared factory:pr-open from closed #N`。

约束：
- **只清 `factory:pr-open`**。已关闭 issue 上的 `factory:needs-human` 等标签不动：它们可能代表没处理的失败，应当保持可见。
- `--dry-run` 下**不改任何东西**，只打印 `would clear factory:pr-open from closed #N`。
- 清理失败（`gh` 报错、返回的不是合法列表）不能挡住本轮的正常排队：写一行诊断到 stderr，然后继续挑候选；本轮的退出码不因清理失败而变化。
- `feedback` 子命令和 `cron` 子命令不加这一步。
- 把新标签名写成常量，沿用文件里现有的 `DONE` 常量，不要硬编码字符串。

## 测试
在 `tests/test_autoqueue.py` 里，沿用现有的 shim 和 `harness` fixture：
- 关闭的 issue 带 `factory:pr-open` → 本轮对它执行一次 `gh issue edit N --remove-label factory:pr-open`，然后照常处理排队的 issue；
- `--dry-run` 下不产生任何 `gh issue edit`，只打印 would-clear 行；
- 列表查询失败时，清理被跳过、有诊断输出，排队的 issue 照常被处理。

现有测试里对 `gh` 调用序列的精确断言（例如只有 `issue list` 和 `pr list` 两次调用）会因为多了一次查询而需要更新：只更新期望的调用列表，每条断言原本要表达的意思保持不变。shim 需要能区分 `--state closed` 的查询并返回可配置的列表（默认空列表）。

## 文档
- `docs/factory-labels.md` 第 3 节的生命周期里，合并之后补一句：下一轮 `just autoqueue` 会清掉 `factory:pr-open`；
- `AGENTS.md` 第 12 条同步补半句。

## 验收标准
- 上面三种测试情形都有测试并通过；
- `just test` 和 `just lint` 通过；
- 已关闭 issue 上除 `factory:pr-open` 以外的标签不受影响。

## 不做的
不加 GitHub Action；不处理"PR 被关闭但没合并"的情况（那时 issue 没被自动关闭，不在本次范围内）；不清理 PR 上的标签。

## Comments

(no comments)
