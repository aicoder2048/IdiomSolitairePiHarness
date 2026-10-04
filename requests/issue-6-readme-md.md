Write GitHub issue #6: "README.md 两处失效链接" (https://github.com/aicoder2048/IdiomSolitairePiHarness/issues/6). The issue and its comments are quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is DOCUMENTATION only:
- Only Markdown changes: README.md, docs/, app_docs/, and *.md next to code. No code, config, tests or justfile edits.
- Describe what the code does today — read it before writing, and never describe behaviour that does not exist.
- Keep each file's language and conventions (Chinese with English technical terms; player-facing text in the game is Chinese).

Where: the files the issue names; otherwise the document that already covers the topic.
Done means: the issue's own "Done means" holds; `git diff --stat` against the baseline touches documentation files only; the suites still pass because nothing else changed.
Out of scope: code changes, even to fix something the writing reveals — note those in the report for a separate issue.

## Issue #6 as filed

## 现象
`README.md` 里有两处链接指向不存在的文件：

1. 「工厂队列」一节：`详见 [工厂标签生命周期](docs/factory-labels.md)`。这份文档已移到 `docs/study-notes/factory-labels-guide-20261003-1605.md`。
2. `详见 [使用配方](docs/tech-papers/cookbook.md)。` 这个文件在 PR #2 的返工中已删除，仓库里没有对应的使用配方文档。

## 要做的
1. 把第 1 处链接改为 `docs/study-notes/factory-labels-guide-20261003-1605.md`，链接文字保持「工厂标签生命周期」。
2. 删除第 2 处整行（`详见 [使用配方](docs/tech-papers/cookbook.md)。`），以及因此多出来的空行。
3. 顺手检查 `README.md` 里其余的相对链接：如果还有指向不存在文件的，按同样方式处理（能找到正确目标就改链接，找不到就删除），并在报告里列出。

## 验收标准
- `README.md` 里所有相对链接都指向仓库中存在的文件；
- 只改 `README.md`，不动代码、测试和其它文档；
- `just test` 通过。

## 不做的
不改写 README 的其它内容；不新建使用配方文档。

## Comments

(no comments)
