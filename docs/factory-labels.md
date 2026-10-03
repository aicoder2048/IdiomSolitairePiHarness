# 软件工厂的标签：怎么用、为什么这样设计

本文说明本仓库的 SSSF 软件工厂如何通过 GitHub 的 issue、PR 和标签接活、交付、返工。只想知道"我该做什么"，看第 3 节和第 4 节即可。

## 1. 三个基本概念

| 概念 | 是什么 | 在本项目里 |
| :-- | :-- | :-- |
| **Issue** | 一张任务卡：要做什么、为什么 | 你写需求，例如 #1「新增 /chain 命令」 |
| **PR（Pull Request）** | 一个分支上的代码，请求合并进 `main` | 工厂的产出，例如 #2 |
| **Label（标签）** | 贴在 issue 或 PR 上的彩色标记，可以按它筛选 | 工厂的"开关"和"进度指示" |

工厂开的 PR，描述里会写 `Closes #N`，把 PR 和 issue 关联起来：PR 一合并，GitHub 就自动关闭对应的 issue。

## 2. 为什么用标签

**标签是授权开关。** 公开仓库里任何人都能开 issue、写评论，但只有仓库主人和协作者能打标签。所以"有标签"就等于"主人批准了"。

这一点很重要，因为 issue 的正文会直接变成工厂 agent 的 prompt。如果谁写了 issue 工厂就做，等于让陌生人给你的 agent 下指令。工厂还加了第二道保险：只接**你本人开的** issue（`scripts/autoqueue.py` 的作者检查，默认是当前 `gh` 登录用户，可用环境变量 `FACTORY_AUTHORS` 指定）。

**标签让状态一目了然。** 在 issue 列表页就能看到哪些在排队、哪些在做、哪些等你审、哪些失败了，不用去翻日志。

**标签让队列不怕中断。** 工厂不需要一直开着。每次运行 `just autoqueue`，它都去问 GitHub"现在哪些 issue 带着 `factory:queued`"，这就是待办清单。进程崩了、电脑重启了，状态都还在 GitHub 上，不会丢。

## 3. 完整生命周期

```text
你开 issue，打上 enhancement（类型）+ factory:queued（排队）
        │
        ▼  just autoqueue 认领
   factory:running        工厂在干活：计划 → 写代码 → 跑测试 → 评审 → 写文档
        │
        ├─ 成功 → factory:pr-open      PR 已开，等你审
        └─ 失败 → factory:needs-human  停下，保留现场，不会自动重试

你审 PR、留评论，给 PR 打上 factory:revise
        │
        ▼  just autoqueue-feedback 认领（先撤下 PR 上的 factory:revise）
   issue 变成 factory:revising   工厂按你的评论修改
        │
        ├─ 成功 → 回到 factory:pr-open（PR 上多一个提交和一条工厂回复）
        └─ 失败 → factory:needs-human

你点 Merge → issue 自动关闭，远端分支自动删除
```

下一轮 `just autoqueue` 拿到锁并完成 `git fetch` 后、挑候选之前，会清掉已关闭 issue 上的 `factory:pr-open`；其他标签（尤其是 `factory:needs-human`）保持不变。`--dry-run` 只打印清理预览，不改标签；清理失败会输出诊断，但不阻塞正常排队，也不改变本轮退出码。`feedback` 和 `cron` 子命令不执行这一步。

## 4. 每个标签的含义

| 标签 | 贴在 | 谁打 | 含义 |
| :-- | :-- | :-- | :-- |
| `bug` / `enhancement` / `chore` / `documentation` | issue | **你** | 工作类型，决定工厂用哪份模板（例如 bug 修复要先写一个能复现问题的测试） |
| `factory:queued` | issue | **你** | "工厂，接这个活" |
| `factory:running` | issue | 工厂 | 正在做 |
| `factory:pr-open` | issue | 工厂 | PR 已开，轮到你审 |
| `factory:revise` | **PR** | **你** | "我留了意见，请修改" |
| `factory:revising` | issue | 工厂 | 正在按你的意见修改 |
| `factory:needs-human` | issue | 工厂 | 失败了，需要你看一下 |

记住一条就够了：**你只打三种标签**，即一个类型标签、`factory:queued`、`factory:revise`。其余的 `factory:*` 都由工厂自己挪，你只需要看。

类型标签必须**恰好一个**。没有类型标签或有两个的 issue，工厂会拒绝处理，并在一个 token 都没花之前就停下。

## 5. 操作步骤

### 交给工厂一个新任务

1. 在 GitHub 上新建 issue，写清楚背景、要做什么、验收标准、不做什么（参考 #1 的写法）。
2. 打上一个类型标签和 `factory:queued`。
3. 运行 `just autoqueue`（可以先加 `--dry-run` 看它会挑哪个 issue）。一个 issue 通常要 10 到 40 分钟，完成后 PR 自动打开。

### 让工厂按评论修改 PR

1. 打开 PR，在 **Files changed** 里留行内评论，或者在 **Conversation** 里留总体评论。
   - 用 "Start a review" 写的评论，最后一定要点 **Submit review**。没提交的草稿评论工厂看不到。
2. 给 PR 打上 `factory:revise`：
   - 网页：PR 页面右侧栏 **Labels** 旁的齿轮 → 勾选 `factory:revise` → 点空白处保存；
   - 命令行：`gh pr edit <PR号> --add-label factory:revise`。
3. 运行 `just autoqueue-feedback`。完成后 PR 上会多一个提交，以及一条工厂回复，里面有 builder 的说明和改动统计。
4. 还要再改：继续留言，再打一次 `factory:revise`。工厂只看它上次回复**之后**的评论。

### 合并

审过没问题就点 **Merge pull request**。issue 会自动关闭，远端分支自动删除（仓库已开启 "Automatically delete head branches"）。

## 6. 为什么返工靠标签，而不是 "Request changes"

GitHub 正规的评审流程是由评审人选 "Request changes"。但工厂是用你自己的账号开的 PR，而 **GitHub 不允许对自己的 PR 选 Request changes**，只能选 Comment。所以返工改用 `factory:revise` 标签触发，做法和 `factory:queued` 一致：先留评论，再打标签。

工厂自己在 PR 上发的评论都带一个隐藏标记 `<!-- factory -->`，所以不会被当成你的意见读回去。因为工厂和你用的是同一个账号，这是区分两者的唯一办法。如果以后给工厂单独开一个 GitHub 机器人账号，就可以改回 Request changes 触发。

## 7. 失败了怎么办

`factory:needs-human` 是有意设计的：工厂**从不自动重试**，以免在同一个错误上反复消耗 token。失败时：

- 工厂会在 issue 或 PR 下留言，说明卡在哪一步，并附上日志的最后几行；
- 现场保留在本机 `.autoqueue/worktrees/` 下（`issue-N` 或 `pr-N`），对应的本地分支 `factory/issue-N` 也保留；
- 完整日志在 `.autoqueue/logs/`；如果卡在工厂内部的某个阶段，可以用 `just phases <adw_id>` 查看各阶段状态。

处理完之后，删掉留下的 worktree 和本地分支，再重新打一次标签即可重试：

```bash
git worktree remove --force .autoqueue/worktrees/pr-2
git branch -D factory/issue-1
gh pr edit 2 --add-label factory:revise    # issue 的话是 gh issue edit N --add-label factory:queued
```

如果不删，工厂下次看到残留的 worktree 会跳过这个任务，以免覆盖你还没看完的现场。

## 8. 相关文件

| 文件 | 作用 |
| :-- | :-- |
| `scripts/autoqueue.py` | 队列：认领、建 worktree、打标签、失败留言 |
| `adws/adw_issue.py` | 一个 issue → 计划、代码、测试、评审、文档 → PR |
| `adws/adw_pr_feedback.py` | PR 评论 → 修改 → 测试 → 提交、推送、回复 |
| `adws/adw_data/prompt_engineering/issue/` | 各类型 issue 与 PR 返工的模板 |
| `AGENTS.md` 第 12、13 条 | 工厂接活与返工规则的简要版 |
