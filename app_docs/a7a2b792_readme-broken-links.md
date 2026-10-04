# README 相对链接修复

`README.md` 的「工厂队列」段落现在将「工厂标签生命周期」链接指向 `docs/study-notes/factory-labels-guide-20261003-1605.md`；该文档原先引用的 `docs/factory-labels.md` 路径已不再使用。README 中指向不存在的 `docs/tech-papers/cookbook.md` 的「使用配方」整行及其多余空行已删除，没有新增配方文档。其他 README 内容未改动。

## 变更所在

- `README.md`：唯一的实际内容修复。规格记录确认 README 当时只有上述两个相对链接，因此没有其他链接需要调整。
- `requests/issue-6-readme-md.md`：记录 issue #6 原始要求。
- `specs/a7a2b792_readme-broken-links.md`：记录范围、已确认的链接现状及验证步骤；这是流程规划产物，不是 README 的额外改写。

## 验证

规格文件给出了检查 README 内联 Markdown 相对链接是否存在的命令，并要求运行 `just test`、`git diff --check`。可按其中的命令复核链接和测试；此变更记录本身没有提供测试运行结果，不能据此声称测试已通过。
