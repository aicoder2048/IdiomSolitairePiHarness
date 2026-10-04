Address review feedback on pull request #16: "对局结束时显示结算画面" (https://github.com/aicoder2048/IdiomSolitairePiHarness/pull/16). The factory opened it; you are on its branch, and its earlier commits are the factory's own plan (under specs/), code and write-up. The feedback is quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a REVISION of work under review:
- Address every point below. Where a point is a question, or you think the change would be wrong, change nothing for it and answer it in your report's summary: the reply to the reviewer is built from that summary.
- Change only what the feedback asks for. Existing tests keep passing; feedback that changes behaviour comes with tests that describe it.
- An inline point names its file and line; read the code around it before editing.

Where: the files the feedback names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point below is either handled in code or answered in the report; `just test` passes.
Out of scope: anything the feedback does not ask for, including cleanups the reviewer did not mention.

## Pull request description

Closes #11

Built by SSSF run `a5e93a00` (adw_issue, kind: feature) from `requests/issue-11.md`. Plan, code and write-up are its three commits.

## Feedback since the factory's last reply

### 1. @aicoder2048 · comment

实测结算画面横向铺满了整个屏幕（120 列终端里约 118 列），实际内容最宽只有约 60 列，两侧大片空白。请不要写死 width: "100%"，改用 panel.ts 里现有的 panelWidth() 计算宽度（与 /hint 选择框一致：内容最宽行 + 边框和内边距，下限 40 列，上限 60%）；如果结算的行在 60% 下会被截断，上限可以放宽到 80%，但不要铺满。请在 extension.test.ts 里断言结算画面的 overlayOptions.width 是按内容算出的数值，而不是 "100%"。
