# 学习笔记：`just autoqueue` 对一个 issue 做了什么

> 记录时间：2026-10-03 16:01 PDT
> 例子：issue #4「autoqueue：每轮开始时清掉已关闭 issue 上残留的 factory:pr-open」，记录时工厂正处在 build 阶段。
> 相关文档：`factory-labels-guide-20261003-1605.md`（标签与操作步骤）、`scripts/autoqueue.py`、`adws/adw_issue.py`

## 一句话

`just autoqueue` 是一条无人值守的流水线：从 GitHub 上找出你批准的 issue，在一个隔离的目录里让 agent 计划、写代码、测试、评审、写文档，最后由代码推送分支、开 PR、改标签。整个过程分四步，其中第 1、2、4 步全是确定性代码，agent 只在第 3 步里干活。

## 第 1 步：找活、认领（几秒钟）

1. **拿队列锁**（`.autoqueue/lock`，基于 `flock`），保证同一时间只有一个队列在跑。
2. **`git fetch`**，拿到最新的 `main`。
3. **问 GitHub**：哪些打开的 issue 带 `factory:queued`？对每个候选逐条检查：
   - 是不是允许的作者开的（默认是当前 `gh` 登录用户；issue 正文会变成 agent 的 prompt，陌生人开的不接）；
   - 有没有已经指派给别人；
   - 有没有已打开的 PR 声明要关闭它（`Closes #N`）；
   - 有没有上次失败留下的 worktree（有就跳过，不覆盖现场）。
4. **认领**：撤下 `factory:queued`，打上 `factory:running`，并把 issue 指派给自己。在 issue 页面上能立刻看到这个变化。

## 第 2 步：建一个隔离的工作区

```bash
git worktree add -b factory/issue-4 .autoqueue/worktrees/issue-4 origin/main
bun install --frozen-lockfile
```

- **worktree** 是同一个仓库的另一个工作目录。工厂在里面干活，主目录不受影响，你可以同时继续改自己的代码。
- 新分支 `factory/issue-4` 从最新的 `origin/main` 切出，不会带上你本地还没推送的提交。
- 新目录里没有 `node_modules`，所以要先装依赖，后面才能跑测试。

## 第 3 步：跑工厂流水线（agent 干活的地方）

在 worktree 里执行 `just issue 4`，也就是 `adws/adw_issue.py`。它按顺序走这些阶段：

| 阶段 | 谁做 | 做什么 |
| :-- | :-- | :-- |
| request | 代码 | 读取 #4，按类型标签（这里是 `enhancement`，即 feature）选模板，写出 `requests/issue-4-….md` |
| plan | planner（Codex 订阅） | 写实现计划，放进 `specs/` |
| commit_plan | 代码 | 先把计划单独提交，留下"写代码之前想的是什么"的记录 |
| build | builder（Codex 订阅） | 按计划改代码、测试、文档 |
| test | 代码 | 跑 `just test` 和 lint；不过就把原样输出交回 builder 修，最多 3 次 |
| review | reviewer（DeepSeek） | 对照计划检查结果，可以打回重改 |
| commit_build | 代码 | 测试和评审都通过后才提交代码 |
| document | documenter（Codex 订阅） | 写变更说明，单独提交 |

几个值得注意的设计：

- **测试是代码，不是 agent。** 跑什么命令是已知的，所以由代码直接跑，agent 只负责读懂失败输出并修复。
- **提交、推送都是代码做的。** `dev_guard.ts` 禁止 agent 执行 `gh` 和改动 git 历史的命令。
- **进度可见。** 每过一个阶段，工厂就编辑 issue 下**同一条**评论（✅ request、✅ plan……然后是"running…"），不用看日志也知道走到哪了。
- **结果有三个提交、三位作者**：计划（planner）、代码（builder）、说明（documenter），各自的提交说明用各自 agent 的话。

## 第 4 步：交付（又回到代码）

- `git push` 分支，`gh pr create` 开 PR：标题与 issue 相同，描述里写 `Closes #4`，合并时 GitHub 会自动关闭 #4。
- issue 标签改为 `factory:pr-open`，表示轮到人来审。
- 删除本地 worktree 和本地分支。

### 如果中途失败

- 标签改为 `factory:needs-human`，撤销指派；
- 在 issue 下留言，说明卡在哪一步，附上日志最后几行；
- **保留 worktree 和分支**给人排查，日志在 `.autoqueue/logs/`；
- **从不自动重试**，避免在同一个错误上反复消耗 token。人处理完、删掉残留后重新打 `factory:queued` 才会再跑。

## issue 和 PR 的编号

同一个仓库里，issue 和 PR **共用一套编号**，按创建先后依次分配。#1（issue）之后紧跟 #2（PR）只是因为中间没有新建别的东西。把 PR 和 issue 关联起来的是 PR 描述里的 `Closes #N`，而不是编号相邻；工厂内部还靠分支名 `factory/issue-N` 找到 PR 对应的 issue。

## 和四层工程的对应

这条流水线本身就是论文里"驱动循环 / 思考循环"分层的放大版：

| 论文里的概念 | 在 `just autoqueue` 里 |
| :-- | :-- |
| 驱动循环（确定性，由外部事件驱动） | 第 1、2、4 步：锁、查询、认领、worktree、推送、开 PR、改标签 |
| 思考循环（概率性，受预算约束） | 第 3 步里的各个 agent 阶段；修复循环最多 3 次 |
| Cheap Verifier | test 阶段跑 `just test`，以及每个 agent 阶段后的 gate（例如核对声明改了的文件和实际改动是否一致） |
| 记录系统只由驱动循环写 | 提交、推送、标签都由代码做；agent 只能"提议"（交回结构化的报告），代码"裁决" |
| 终止条件 | 成功开 PR，或失败标 `needs-human`；永远不会无限重试 |
