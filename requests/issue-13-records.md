Implement GitHub issue #13: "跨局战绩：/records 命令" (https://github.com/aicoder2048/IdiomSolitairePiHarness/issues/13). The issue and its comments are quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a FEATURE — new behaviour, or existing behaviour made better:
- Plan before building: the plan names the files, the data flow and the tests, and the builder follows it.
- New behaviour comes with tests that describe it. Existing tests keep passing unchanged, unless the issue changes what they test.
- Document it in the same change: README.md (player-facing: how to play, commands) and AGENTS.md when it adds a rule.
- Where the issue leaves a choice open, take the simplest option that satisfies it and record the choice in the plan.

Where: the files the issue names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point under the issue's own "Done means" holds; tests cover the new behaviour; `just test` passes; README/docs describe what changed.
Out of scope: anything the issue does not ask for; redesigns of neighbouring code.

## Issue #13 as filed

## 背景
现在每局结束就没了，没有历史战绩。

## 要做的
1. **记录**：对局结束时把一条战绩追加到 JSON 文件：时间（ISO 8601）、难度、总轮数、双方比分、胜负。文件路径取环境变量 `IDIOM_RECORDS_FILE`，默认 `~/.pi/agent/idiom-solitaire/records.json`；目录不存在就创建。
2. **一局只记一次**：每局有一个 id（开局和 `/restart` 时生成）。如果 `/undo` 撤销了最后一轮又重新打完，用同一个 id 覆盖那条记录，不新增。
3. **查看**：新命令 `/records`，写一张卡片：总场次、胜/负/平、胜率，以及最近 10 局（每行：日期、难度、比分、胜负）。没有记录时写「还没有战绩」。0 token。
4. 读写失败（文件损坏、没有权限）不能影响游戏：`notify` 一条警告，继续玩。

## 设计约束
- 统计与格式化是纯函数（放 `src/engine/` 或 `view.ts`），有单元测试；文件读写放 `src/extension/`。
- `/records` 登记在 `view.COMMANDS`，加入「确定性命令 0 token」测试。
- 测试用临时目录设置 `IDIOM_RECORDS_FILE`，不能碰真实的 home 目录。

## 验收标准
- 记录、覆盖（undo 后重打）、统计、空记录、文件损坏 五种情形都有测试；
- `just test` 通过。

## 不做的
不做排行榜、不做多玩家、不上传。

## Comments

(no comments)
