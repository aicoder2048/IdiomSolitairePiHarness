# docs/

## 最后更新：2026-10-03

| 项目 | 状态（2026-10-03） |
|---|---|
| 官方文档来源 | <https://pi.dev/docs/latest>（内容与 GitHub `earendil-works/pi` 的 `main` 一致，见下） |
| 上游仓库 | [`earendil-works/pi`](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/docs)（原 `badlogic/pi-mono`） |
| 上游 docs 最新 commit | `11449730c8a7`（2026-10-03T11:54Z） |
| 对应 npm 包 | `@earendil-works/pi-coding-agent` **1.0.1**（原 `@mariozechner/pi-coding-agent`） |
| 本机已安装的 `pi` | 1.0.1（2026-10-03 从 0.99.1 升级；hello 扩展已用 RPC 模式实测通过） |
| 上一次同步 | 约 2026-04-29（旧版 26 页） |

## 目录

- `study-notes/`：学习笔记，文件名为「内容-时间戳」。
  - `factory-labels-guide-20261003-1605.md`：软件工厂怎么通过 GitHub issue、PR 和标签接活、交付、返工（操作步骤与设计理由）。
  - `just-autoqueue-walkthrough-20261003-1601.md`：`just autoqueue` 对一个 issue 做了什么（四步流程）。
- `pi-docs/official-docs/`：官方文档镜像，共 40 页，按 `docs.json` 导航分为 5 组，索引见其中的 `README.md`。
- `pi-docs/llm/pi-docs-combined.md`：把上面 40 页合并成一个文件，方便上传给 NotebookLM 或喂给 LLM。
- `pi-docs/llm/pi-extension-tutorial.md`：Extension 入门教程（中文），2026-10-03 已对照新文档核对过。
- `pi-docs/CHANGES-2026-10-03.md`：旧镜像（2026-04）与新镜像的差异汇总，包括页面映射和 API、设置、CLI 的变化。
- `pi-docs/sync_official_docs.py`：同步脚本。
- 以下文件**未随本次同步更新**，属于第三方文章或个人笔记，内容可能过时：
  - `pi-docs/llm/indydevdan-pi-docs.md`
  - `pi-docs/00-harness-engineering.md`
  - `pi-docs/reference-articles/`
  - `agentic-engineering-paper.md`

## 如何重新同步

```bash
uv run --no-project python docs/pi-docs/sync_official_docs.py
```

这个脚本会做四件事：

1. 从上游拉取 `docs.json` 和全部页面。
2. 重建 `official-docs/`（先整个删除再生成）。
3. 改写链接：页面之间的链接改成本地相对路径，指向 `examples/` 或 `src/` 的链接改成 GitHub 绝对链接。
4. 重新生成合并文件。

同步完成后，记得更新本文件里的日期，并另写一份新的 `CHANGES-<date>.md`。

## 2026-10-03 这次的要点（详见 CHANGES 文件）

- **包名改了**：`@mariozechner/*` 全部改成 `@earendil-works/*`，旧代码里的 import 都要改。
- **新增 project trust**：项目里的 `.pi/` 资源要先授信才会加载。print、JSON、RPC 这类无人值守的模式默认会跳过这些资源，需要加 `--approve` 或设置 `defaultProjectTrust`。
- **新功能**：内置 MCP 和 codemode，新增 virtual models，还有新事件 `agent_before_settle` 和 `agent_settled`。
- **`pi update` 的语义变了**：不带参数时只更新 Pi 本身，扩展用 `--extensions`，全部更新用 `--all`。
- **文档结构重排了**：旧的 `01-start-here/` 等目录已不存在，新旧页面的对应关系见 CHANGES 文件。
