"""The evidence bundle: what a run's code saw, rendered as the PR body.

"Tests pass" from an agent is a claim. The bundle is the record the run's own
code kept: each command with its exit code and the counts it printed, the
red/green pair, the integrity comparison with the baseline, the reviewer's
verdict requirement by requirement, and — said out loud — what nobody checked.
It is rendered from typed results only, never from an agent's summary of them.

Every section is always present. One that did not run says NOT_RUN instead of
disappearing, so a missing check reads as missing rather than as fine. Declared
test weakening goes above everything else: it is the one thing a reviewer of the
PR must not miss.

The file lands in the session (`context_handoff/evidence.md`), not in the repo;
adw_issue puts it in the PR body and adw_pr_feedback in its reply.
"""

from __future__ import annotations

import re
from pathlib import Path

from .agents import load_config
from .data_types import EvidenceInput, IntegrityResult, ProofResult, QualityResult, ReviewOutput
from .integrity import added_test_lines

NOT_RUN = "（本次未运行）"
GITHUB_LIMIT = 60_000  # GitHub caps a body at 65,536 characters; leave room for the lines around it
DEPENDENCY_FILES = {"package.json", "bun.lock", "bun.lockb", "uv.lock", "pyproject.toml"}

SUMMARY = re.compile(
    r"^(?:\d+ (?:pass|fail|skip|todo)|\d+ expect\(\) calls?|Ran \d+ tests? across .*|\d+ (?:passed|failed)\b.*"
    r"|ℹ (?:tests|pass|fail) \d+|All checks passed!|\d+ files? already formatted|Found \d+ errors?.*"
    r"|\d+ files? would be reformatted.*)$"
)
BUN_TEST = re.compile(r"(?<![\w.])(?:test|it)(?:\.\w+(?:\([^)]*\))?)*\(\s*([\"'`])(.*?)\1")
PY_TEST = re.compile(r"^\s*(?:async\s+)?def (test_\w+)\(")


# ── reading what the run produced ────────────────────────────────────────────


def summary_lines(text: str) -> list[str]:
    """The lines of a log that carry counts or a verdict — `210 pass`, `160 passed in 15s`, `All checks passed!`."""
    found = []
    for raw in text.splitlines():
        line = raw.strip().strip("=").strip()
        if SUMMARY.match(line):
            found.append(line)
    return found


def tests_named(path: str, lines: list[str]) -> list[str]:
    """The names of the tests these lines of `path` declare: pytest's `def test_…` in a .py file, else `test("…")`."""
    if path.endswith(".py"):
        return [m[1] for m in map(PY_TEST.match, lines) if m]
    return [m[2] for m in map(BUN_TEST.search, lines) if m]


def new_tests(base: str, patterns: list[str]) -> list[str]:
    """Names of the tests the change adds, from the added lines of every changed or new test file."""
    return [name for path, lines in added_test_lines(base, patterns).items() for name in tests_named(path, lines)]


# ── rendering ────────────────────────────────────────────────────────────────


def cell(text: str) -> str:
    """Safe inside a Markdown table cell: pipes escaped, newlines as <br>."""
    return str(text).replace("|", r"\|").replace("\r\n", "\n").replace("\n", "<br>")


def _sha(sha: str) -> str:
    return f"`{sha[:7]}`" if sha else "（未知）"


def _fence(text: str) -> str:
    return f"```text\n{text.rstrip() or '(empty)'}\n```"


def _weakening(integrity: IntegrityResult | None) -> list[str]:
    if integrity is None or not (integrity.declared or any(f.declared for f in integrity.findings)):
        return []
    lines = ["> ⚠️ **本次改弱了测试（builder 已声明原因）**", ">"]
    lines += [f"> - `{w.file}`：{w.reason}" for w in integrity.declared]
    lines += [f"> - 检查发现：`{f.file or '整个套件'}` {f.problem}" for f in integrity.findings if f.declared]
    return [*lines, ""]


def _verdict(inp: EvidenceInput) -> list[str]:
    verdict = "✅ 已接受" if inp.accepted else f"❌ 未接受：{inp.reason or '验收条件不满足'}"
    return [verdict, "", f"- workflow：`{inp.workflow}`", f"- kind：{inp.kind or '未指定'}"]


def _versions(inp: EvidenceInput) -> list[str]:
    head = _sha(inp.head) if inp.head else "工作区（未提交，由调用方提交）"
    return [
        f"- run：`{inp.adw_id}`",
        f"- branch：`{inp.branch or '（未知）'}`",
        f"- 基线：{_sha(inp.baseline)}",
        f"- HEAD：{head}",
    ]


def _quality(result: QualityResult | None) -> list[str]:
    if result is None:
        return [NOT_RUN]
    lines = ["| 检查 | 命令 | 退出码 | 耗时 | 摘要 |", "| :-- | :-- | :-: | --: | :-- |"]
    for check in result.checks:
        path = Path(check.output_artifact)
        log = path.read_text(encoding="utf-8", errors="replace") if path.is_file() else check.output_tail
        mark = "✅" if check.passed else "❌"
        summary = "; ".join(summary_lines(log)) or "—"
        lines.append(
            f"| {mark} {cell(check.name)} | `{cell(check.command)}` | {check.returncode} "
            f"| {check.duration_seconds:.1f}s | {cell(summary)} |"
        )
    return lines


def _proof(result: ProofResult | None) -> list[str]:
    if result is None:
        return [NOT_RUN]
    rule = "bug：每个改动的测试必须在基线上失败、在 HEAD 上通过" if result.required else "只记录，不拦截"
    lines = [f"基线 {_sha(result.baseline)}，{rule}。", ""]
    if not result.checks:
        return [*lines, "本次没有新增或修改测试文件。"]
    lines += ["| 测试文件 | 基线 | HEAD | 判定 |", "| :-- | :-: | :-: | :-- |"]
    for c in result.checks:
        verdict = "✅ 红→绿" if c.red and c.green else ("⚠️ 基线上也通过" if not c.red else "❌ HEAD 上失败")
        base = f"exit {c.base_returncode} {'🔴' if c.red else '🟢'}"
        head = f"exit {c.head_returncode} {'🟢' if c.green else '🔴'}"
        lines.append(f"| `{cell(c.file)}` | {base} | {head} | {verdict} |")
    for c in result.checks:
        lines += [
            "",
            f"<details><summary><code>{c.command}</code> 的输出</summary>",
            "",
            "基线：",
            "",
            _fence(c.base_tail),
            "",
            "HEAD：",
            "",
            _fence(c.head_tail),
            "",
            "</details>",
        ]
    return lines


def _integrity(result: IntegrityResult | None) -> list[str]:
    if result is None:
        return [NOT_RUN]
    if result.base_counts and result.head_counts:
        b, h = result.base_counts, result.head_counts
        lines = [f"- bun 用例数 {b.tests} → {h.tests}，expect() {b.expects} → {h.expects}"]
    else:
        lines = ["- 用例数没有比较（没有改动计数器覆盖的测试文件，或无法解析）"]
    if not result.findings:
        return [*lines, "- 没有发现改弱测试"]
    for f in result.findings:
        mark = "⚠️ 已声明" if f.declared else "❌ 未声明"
        lines.append(f"- {mark}：`{f.file or '整个套件'}` {f.problem}")
    return lines


def _new_tests(names: list[str] | None) -> list[str]:
    if names is None:
        return [NOT_RUN]
    return [f"- {name}" for name in names] or ["（没有）"]


def _review(review: ReviewOutput | None) -> list[str]:
    if review is None:
        return [NOT_RUN]
    lines = [f"{'✅ 通过' if review.approved else '❌ 未通过'}：{review.summary}".rstrip("："), ""]
    if review.findings:
        lines += ["| 需求 | 满足 | 证据 |", "| :-- | :-: | :-- |"]
        lines += [
            f"| {cell(f.requirement)} | {'✅' if f.met else '❌'} | {cell(f.evidence)} |" for f in review.findings
        ]
    if review.blocking:
        lines += ["", "阻塞项：", *[f"- {b}" for b in review.blocking]]
    return lines


def unverified(inp: EvidenceInput) -> list[str]:
    """What nobody checked: the project's standing list, the reviewer's, the integrity check's, and code's own."""
    items = list(inp.unverified)
    if inp.review is not None:
        items += [f"Reviewer：{item}" for item in inp.review.unverified]
    if inp.integrity is not None:
        items += inp.integrity.unverified
    if inp.proof is not None and not inp.proof.required:
        items.append(f"红绿证明只做了记录、没有拦截（kind 为 {inp.kind or '未指定'}，不是 bug）")
    if DEPENDENCY_FILES & {Path(f).name for f in inp.changed_files}:
        items.append("依赖有变动：基线是借用 HEAD 的 node_modules 跑的，红绿证明和用例计数可能失真")
    return items


def _cost(inp: EvidenceInput) -> list[str]:
    return [f"{inp.tokens:,} tokens · ${inp.cost:.4f}"]


def render(inp: EvidenceInput) -> str:
    sections = [
        ("1. 结论", _verdict(inp)),
        ("2. 版本", _versions(inp)),
        ("3. 改了什么", [_fence(inp.diff_stat)] if inp.diff_stat else ["（没有改动）"]),
        ("4. 怎么验证的", _quality(inp.quality)),
        ("5. 红绿证明", _proof(inp.proof)),
        ("6. 测试完整性", _integrity(inp.integrity)),
        ("7. 新增的测试", _new_tests(inp.new_tests)),
        ("8. Reviewer 逐条核对", _review(inp.review)),
        ("9. 未验证项", [f"- {item}" for item in unverified(inp)] or ["（无）"]),
        ("10. 成本", _cost(inp)),
    ]
    out = [f"# SSSF 证据包 · run `{inp.adw_id}`", "", *_weakening(inp.integrity)]
    for title, body in sections:
        out += [f"## {title}", "", *body, ""]
    return "\n".join(out)


# ── the file, and GitHub's copy of it ───────────────────────────────────────


def path_for(data_dir: str, adw_id: str) -> Path:
    return Path(data_dir) / "sessions" / adw_id / "context_handoff" / "evidence.md"


def write(run, inp: EvidenceInput) -> Path:
    path = Path(run.context_handoff_dir) / "evidence.md"
    path.write_text(render(inp), encoding="utf-8")
    return path


def load(config: str, adw_id: str) -> str:
    """A finished run's bundle, or "" when there is none (or no config to find it by)."""
    try:
        path = path_for(load_config(config).defaults.data_dir, adw_id)
        return path.read_text(encoding="utf-8") if path.is_file() else ""
    except (OSError, ValueError):
        return ""


def for_github(text: str, where: str) -> str:
    """The bundle as a PR body or comment can hold it: cut at GITHUB_LIMIT, saying where the whole is."""
    if len(text) <= GITHUB_LIMIT:
        return text
    return text[:GITHUB_LIMIT] + f"\n\n…（证据包超过 {GITHUB_LIMIT} 字符，已截断；全文在 session 的 `{where}`）\n"
