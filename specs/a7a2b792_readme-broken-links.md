# Issue #6：修复 README 两处失效链接

## 目标与范围

仅修复 `README.md` 的失效相对链接，不改写其它文字，不新增使用配方文档，不修改代码、测试、配置、justfile 或其它现有文档。保留中文与现有 Markdown 排版。

本计划及 `specs/` 副本是流程要求的规划产物，不属于 README 修复内容。builder 的实现修改只能涉及 `README.md`；最终报告应明确区分规划产物与实现改动，不能把包含 spec 的整体 diff 宣称为只有 README。

## 已确认的现状

- 调研基线：`2f02e8f206be9451983e68e22f54d0ae0cef358b`。
- 初始工作区有未跟踪文件 `requests/issue-6-readme-md.md`，不得修改或删除。
- 已完整阅读 README：仅有两个 Markdown 相对链接，均为 issue 列出的失效链接；没有其它相对链接需要修复。
- `docs/study-notes/factory-labels-guide-20261003-1605.md` 存在，文首注明原路径为 `docs/factory-labels.md`，内容涵盖工厂标签生命周期。
- `docs/tech-papers/cookbook.md` 不存在；不使用不相关的工厂 cookbook 替代它。
- 已阅读 `scripts/autoqueue.py` 的 `clear_closed_done()`：当前代码清理已关闭 issue 的 `factory:pr-open`，dry-run 只预览。本次不修改或扩写行为说明。
- 已阅读 `justfile`：`just test` 依次运行类型检查、bun 测试、工厂测试、autoqueue 测试；不需要运行收费的 `just smoke`。

## 实施步骤

1. 修改前检查工作区状态，保留已有文件和流程产物。重新确认 README 链接清单；不要新增测试文件（本次没有行为变更）。
2. 在 `README.md` 删除整行 `详见 [使用配方](docs/tech-papers/cookbook.md)。`，同时移除多余空行，使上一段和 `## 工厂队列` 之间只留一个空行。
3. 将工厂队列段落里的 `[工厂标签生命周期](docs/factory-labels.md)` 替换为 `[工厂标签生命周期](docs/study-notes/factory-labels-guide-20261003-1605.md)`，链接文字和该段其它内容完全不变。
4. 复查全部 README 相对链接。当前没有其它链接要改；若工作区内容发生变化而出现额外失效链接，仅在能确认正确目标时改路径，否则删除相应链接内容并在报告列明，避免无关改写。

## 验证

无需持久化任何校验脚本。可在修改前后运行以下只读校验：当前 README 的全部链接都是普通内联 Markdown 链接，此命令覆盖当前清单；修改前预期退出 1，修改后预期退出 0。

```sh
bun -e 'import {readFileSync,statSync} from "node:fs"; const text=readFileSync("README.md","utf8"); let bad=false; for(const m of text.matchAll(/\[[^\]]*\]\(([^)]+)\)/g)){ const target=m[1]; if(/^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(target)) continue; const path=decodeURIComponent(target.split(/[?#]/)[0]); let ok=false; try{ok=statSync(path).isFile();}catch{} console.log(`${ok?"exists":"missing"}\t${target}`); if(!ok) bad=true; } process.exit(bad?1:0);'
```

然后执行：

```sh
just test
git diff --check
git diff 2f02e8f206be9451983e68e22f54d0ae0cef358b --stat
git diff 2f02e8f206be9451983e68e22f54d0ae0cef358b -- README.md
git status --short
```

- 以命令退出码判定成功，不按输出中是否出现 error 等文字判定。
- `just test` 必须通过；若环境或已有问题导致失败，记录命令、退出码和阻塞原因，不越界改代码或配置，不宣称通过。
- diff 应显示 README 只有两项指定修复及对应空行删除；除流程要求的 Markdown 规划产物外，不得有其它实现改动。对基线的整体统计只能涉及文档文件。
- 检查未跟踪文件，确保没有测试生成物等意外变更混入交付。

## 交付报告

列出工厂标签链接的新路径、删除的使用配方链接，以及“已检查其余相对链接，无其它失效链接”。报告 `just test` 和链接校验的真实结果，并区分 README 实现改动与规划产物。若发现与本修复无关的代码或文档问题，仅记录供另开 issue，不在此任务修复。
