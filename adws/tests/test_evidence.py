"""The evidence bundle: what code saw during a run, written down for the PR to carry.

An agent saying "tests pass" is a claim. The bundle is what the run's own code
recorded — the commands and their exit codes, the red/green pair, the integrity
comparison, the reviewer's requirement-by-requirement verdict — plus what
nobody checked, said out loud. It is rendered from typed results only, every
section always present: a section that did not run says so instead of vanishing.

Run with `just test-adws` (the adws need pydantic; the project venv does not).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adw_modules import agents, evidence  # noqa: E402
from adw_modules.data_types import (  # noqa: E402
    EvidenceInput,
    IntegrityFinding,
    IntegrityResult,
    ProofCheck,
    ProofResult,
    QualityCheckResult,
    QualityResult,
    ReviewFinding,
    ReviewOutput,
    SuiteCounts,
    WeakenedTest,
)

ADWS = Path(__file__).resolve().parents[1]
HEADINGS = [
    "## 1. 结论",
    "## 2. 版本",
    "## 3. 改了什么",
    "## 4. 怎么验证的",
    "## 5. 红绿证明",
    "## 6. 测试完整性",
    "## 7. 新增的测试",
    "## 8. Reviewer 逐条核对",
    "## 9. 未验证项",
    "## 10. 成本",
]
BUN_LOG = """$ just test
exit: 0

--- stdout ---
bun test v1.4.2 (744846f84)
 210 pass
 1 skip
 0 fail
 1091 expect() calls
Ran 210 tests across 9 files. [79.00ms]
160 passed in 15.38s
"""


def quality(tmp_path: Path) -> QualityResult:
    log = tmp_path / "command.log"
    log.write_text(BUN_LOG)
    check = QualityCheckResult(
        name="test",
        area="backend",
        operation="build",
        command="just test",
        returncode=0,
        passed=True,
        duration_seconds=81.2,
        output_artifact=str(log),
    )
    return QualityResult(passed=True, checks=[check], artifacts=[str(log)])


def full(tmp_path: Path, **changes) -> EvidenceInput:
    base = dict(
        adw_id="cafe1234",
        workflow="adw_simple_sdlc",
        kind="bug",
        accepted=True,
        branch="factory/issue-7",
        baseline="a" * 40,
        head="b" * 40,
        diff_stat=" src/engine/game.ts | 4 ++--\n 1 file changed",
        changed_files=["src/engine/game.ts", "tests/engine/game.test.ts"],
        quality=quality(tmp_path),
        proof=ProofResult(
            required=True,
            passed=True,
            baseline="a" * 40,
            checks=[
                ProofCheck(
                    file="tests/engine/game.test.ts",
                    command="bun test ./tests/engine/game.test.ts",
                    base_returncode=1,
                    head_returncode=0,
                    base_tail="expected 3, got 2",
                    head_tail="1 pass",
                )
            ],
        ),
        integrity=IntegrityResult(
            passed=True,
            base_counts=SuiteCounts(tests=210, expects=1091),
            head_counts=SuiteCounts(tests=211, expects=1093),
        ),
        new_tests=["超时后结算本轮"],
        review=ReviewOutput(
            status="success",
            approved=True,
            findings=[ReviewFinding(requirement="超时结算", met=True, evidence="src/engine/game.ts:42")],
        ),
        unverified=["未运行 `just smoke`（按量计费）"],
        tokens=123456,
        cost=0.4321,
    )
    return EvidenceInput(**{**base, **changes})


# --- the shape ---------------------------------------------------------------------------------------


def test_a_full_bundle_has_all_ten_sections_in_order(tmp_path):
    text = evidence.render(full(tmp_path))
    positions = [text.index(h) for h in HEADINGS]
    assert positions == sorted(positions)
    assert evidence.NOT_RUN not in text


def test_a_section_that_did_not_run_says_so_instead_of_vanishing(tmp_path):
    bare = EvidenceInput(adw_id="cafe1234", workflow="adw_build_test", accepted=False, reason="the suite failed")
    text = evidence.render(bare)
    assert all(h in text for h in HEADINGS)
    # quality, proof, integrity, new tests, review
    assert text.count(evidence.NOT_RUN) == 5
    assert "the suite failed" in text


def test_the_verdict_and_versions_are_stated(tmp_path):
    text = evidence.render(full(tmp_path))
    assert "✅" in section(text, 1)
    assert "a" * 7 in section(text, 2) and "b" * 7 in section(text, 2) and "factory/issue-7" in section(text, 2)
    assert "src/engine/game.ts | 4" in section(text, 3)


def test_an_uncommitted_head_is_named_as_such(tmp_path):
    assert "未提交" in section(evidence.render(full(tmp_path, head="")), 2)


def test_each_check_shows_its_command_exit_code_duration_and_summary(tmp_path):
    text = section(evidence.render(full(tmp_path)), 4)
    assert "just test" in text and "81.2s" in text
    assert "210 pass" in text and "Ran 210 tests across 9 files." in text and "160 passed" in text


def test_the_proof_shows_both_sides_of_each_file(tmp_path):
    text = section(evidence.render(full(tmp_path)), 5)
    assert "tests/engine/game.test.ts" in text
    assert "expected 3, got 2" in text and "1 pass" in text
    assert "红→绿" in text


def test_the_integrity_section_shows_the_counts(tmp_path):
    text = section(evidence.render(full(tmp_path)), 6)
    assert "210 → 211" in text and "1091 → 1093" in text


def test_new_test_names_are_listed(tmp_path):
    assert "超时后结算本轮" in section(evidence.render(full(tmp_path)), 7)


def test_pipes_in_review_cells_are_escaped(tmp_path):
    review = ReviewOutput(
        status="success",
        approved=False,
        findings=[ReviewFinding(requirement="a | b", met=False, evidence="x|y\nsecond line")],
        blocking=["fix a | b"],
    )
    text = section(evidence.render(full(tmp_path, review=review)), 8)
    assert r"a \| b" in text and r"x\|y<br>second line" in text
    assert "fix a | b" in text  # a list item, not a cell


def test_declared_weakening_comes_before_everything_else(tmp_path):
    integrity = IntegrityResult(
        passed=True,
        findings=[IntegrityFinding(file="tests/engine/game.test.ts", problem="adds a skip marker", declared=True)],
        declared=[WeakenedTest(file="tests/engine/game.test.ts", reason="规则改了，这条已不适用")],
    )
    text = evidence.render(full(tmp_path, integrity=integrity))
    warning = text.index("⚠️")
    assert warning < text.index(HEADINGS[0])
    assert "规则改了，这条已不适用" in text[: text.index(HEADINGS[0])]


def test_cost_is_tokens_and_dollars(tmp_path):
    text = section(evidence.render(full(tmp_path)), 10)
    assert "123,456" in text and "$0.4321" in text


# --- unverified: config, reviewer, integrity, and what code knows it did not check -------------------


def test_unverified_gathers_every_source(tmp_path):
    review = ReviewOutput(status="success", approved=True, unverified=["无法在离线环境确认 TUI 渲染"])
    integrity = IntegrityResult(passed=True, unverified=["这些测试文件的用例数没有比较：adws/tests/test_x.py"])
    text = section(evidence.render(full(tmp_path, review=review, integrity=integrity)), 9)
    assert "just smoke" in text
    assert "无法在离线环境确认 TUI 渲染" in text
    assert "adws/tests/test_x.py" in text


def test_a_proof_that_was_only_recorded_is_unverified(tmp_path):
    proof = ProofResult(required=False, passed=True)
    text = section(evidence.render(full(tmp_path, kind="feature", proof=proof)), 9)
    assert "红绿证明" in text and "feature" in text


def test_a_dependency_change_warns_that_the_baseline_may_be_skewed(tmp_path):
    text = section(evidence.render(full(tmp_path, changed_files=["package.json", "bun.lock"])), 9)
    assert "node_modules" in text


# --- new test names ---------------------------------------------------------------------------------


def test_names_are_taken_from_bun_declarations_in_a_ts_file():
    lines = [
        'test("超时后结算本轮", () => {',
        "  it('keeps the chain', async () => {",
        "test.each([1, 2])(`case %d`, (n) => {",
        "    helper_test('not a declaration')",
        "const x = 1;",
    ]
    assert evidence.tests_named("t/a.test.ts", lines) == ["超时后结算本轮", "keeps the chain", "case %d"]


def test_names_in_a_python_file_are_its_test_functions_not_strings_that_look_like_bun():
    lines = ["def test_hint_costs_one():", "    write('test(\"old\", () => {});')", "async def test_waits():"]
    assert evidence.tests_named("adws/tests/test_x.py", lines) == ["test_hint_costs_one", "test_waits"]


def test_new_tests_come_from_added_lines_of_changed_and_new_test_files(tmp_path, monkeypatch):
    repo = tmp_path / "repo"
    repo.mkdir()
    monkeypatch.chdir(repo)
    git = lambda *a: subprocess.run(["git", *a], cwd=repo, check=True, capture_output=True)  # noqa: E731
    git("init", "-q")
    git("config", "user.email", "t@t")
    git("config", "user.name", "t")
    (repo / "t").mkdir()
    (repo / "t" / "a.test.ts").write_text('test("old", () => {});\n')
    git("add", "-A")
    git("commit", "-qm", "base")
    sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()
    (repo / "t" / "a.test.ts").write_text('test("old", () => {});\ntest("edited in", () => {});\n')
    (repo / "t" / "b.test.ts").write_text('test("brand new", () => {});\n')
    (repo / "src.ts").write_text('test("not a test file", () => {});\n')
    assert evidence.new_tests(sha, ["t/*.test.ts"]) == ["edited in", "brand new"]


# --- check summaries --------------------------------------------------------------------------------


def test_summary_lines_pick_the_counts_out_of_a_log():
    assert evidence.summary_lines(BUN_LOG) == [
        "210 pass",
        "1 skip",
        "0 fail",
        "1091 expect() calls",
        "Ran 210 tests across 9 files. [79.00ms]",
        "160 passed in 15.38s",
    ]


# --- the file, and the PR's copy of it --------------------------------------------------------------


def test_write_puts_the_bundle_in_the_sessions_handoff_dir(tmp_path):
    run = SimpleNamespace(context_handoff_dir=tmp_path)
    path = evidence.write(run, full(tmp_path))
    assert path == tmp_path / "evidence.md"
    assert path.read_text().startswith("# ")


def test_for_github_leaves_a_short_bundle_alone():
    assert evidence.for_github("short", "sessions/x/evidence.md") == "short"


def test_for_github_truncates_and_says_where_the_rest_is():
    text = evidence.for_github("x" * 70_000, "adws/adw_data/sessions/cafe1234/context_handoff/evidence.md")
    assert len(text) < 61_000
    assert "截断" in text and "sessions/cafe1234/context_handoff/evidence.md" in text


def test_load_reads_a_sessions_bundle_and_is_empty_without_one(tmp_path):
    config = tmp_path / "sssf.config.yaml"
    config.write_text(f"defaults:\n  data_dir: {tmp_path / 'data'}\n")
    assert evidence.load(str(config), "cafe1234") == ""
    path = evidence.path_for(str(tmp_path / "data"), "cafe1234")
    path.parent.mkdir(parents=True)
    path.write_text("# bundle")
    assert evidence.load(str(config), "cafe1234") == "# bundle"
    assert evidence.load(str(tmp_path / "missing.yaml"), "cafe1234") == ""


# --- the contract on the config and the reviewer ----------------------------------------------------


def test_the_project_config_lists_smoke_as_never_run():
    cfg = agents.load_config(str(ADWS / "adw_sssf_config" / "sssf.config.yaml"))
    assert any("just smoke" in item for item in cfg.evidence.unverified)


def test_review_unverified_defaults_to_empty():
    assert ReviewOutput(status="success").unverified == []


def test_the_reviewer_report_example_lists_unverified():
    prompts = ADWS / "adw_data" / "prompt_engineering" / "reviewer"
    example = json.loads(re.search(r"```json\n(.*?)\n```", (prompts / "user.md").read_text(), re.S).group(1))
    assert "unverified" in example
    ReviewOutput.model_validate(example)
    assert "unverified" in (prompts / "system.md").read_text()


def section(text: str, n: int) -> str:
    start = text.index(HEADINGS[n - 1])
    end = text.index(HEADINGS[n]) if n < len(HEADINGS) else len(text)
    return text[start:end]
