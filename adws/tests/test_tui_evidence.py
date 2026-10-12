"""TUI screenshots in the evidence bundle: the same scenes on the baseline and on HEAD.

The capture command here is a small Python script standing in for
scripts/tui_capture.py: it writes each scene's screen from `screens/<name>.txt`
in the tree it is pointed at, plus the manifest — so the repo is real git (the
baseline is a real checkout) and nothing starts a terminal.

Run with `just test-adws` (the adws need pydantic; the project venv does not).
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adw_modules import evidence, tui  # noqa: E402
from adw_modules.data_types import EvidenceInput, ModelUsage, TuiConfig, TuiParams, TuiResult, TuiScene  # noqa: E402
from adw_modules.runner import Run  # noqa: E402

# Scenes come from the file at {scenes}; a screen from the tree at {repo}. A tree with
# a `broken` file fails like a bad scene file (exit 2, no manifest).
FAKE = """
import json, sys
from pathlib import Path
scenes, out, repo = (Path(a) for a in sys.argv[1:])
if (repo / "broken").exists():
    sys.exit("tui_capture: bad scene file")
entries = []
for scene in json.loads(scenes.read_text())["scenes"]:
    screen = repo / "screens" / f"{scene['name']}.txt"
    ok = screen.exists()
    (out / f"{scene['name']}.txt").write_text(screen.read_text() if ok else "")
    entries.append({"name": scene["name"], "file": f"{scene['name']}.txt", "ok": ok,
                    "error": None if ok else "timeout waiting for marker\\nLast screen:\\n..."})
(out / "manifest.json").write_text(json.dumps({"scenes": entries}))
sys.exit(0 if all(e["ok"] for e in entries) else 1)
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True).stdout


def write(root: Path, path: str, text: str) -> None:
    (root / path).parent.mkdir(parents=True, exist_ok=True)
    (root / path).write_text(text)


@pytest.fixture
def repo(tmp_path, monkeypatch):
    root = tmp_path / "repo"
    root.mkdir()
    monkeypatch.chdir(root)
    git(root, "init", "-q")
    git(root, "config", "user.email", "test@example.com")
    git(root, "config", "user.name", "test")
    write(root, "screens/status.txt", "📊 状态（卡片）\n")
    write(root, "screens/help.txt", "📖 成语接龙\n")
    git(root, "add", "-A")
    git(root, "commit", "-qm", "base")
    # HEAD's engine and scene file only: the baseline never had them, and must not need them.
    write(root, "fake_capture.py", FAKE)
    write(root, "scenes.json", json.dumps({"scenes": [{"name": "status"}, {"name": "help"}]}))
    return root


@pytest.fixture
def run(repo, tmp_path):
    handoff = tmp_path / "handoff"
    handoff.mkdir()
    return SimpleNamespace(repo_root=repo, context_handoff_dir=handoff, phases=[SimpleNamespace(seq=9)])


def config(**changes) -> TuiConfig:
    base = dict(
        argv=[sys.executable, "fake_capture.py", "{scenes}", "{out}", "{repo}"],
        scenes="scenes.json",
        uncaptured=["终局结算画面（需要 Bot 回合）"],
    )
    return TuiConfig(**{**base, **changes})


def capture(run, repo, **changes) -> TuiResult:
    return tui.capture(run, TuiParams(config=config(**changes), baseline=git(repo, "rev-parse", "HEAD").strip()))


def bundle(result: TuiResult | None, **changes) -> str:
    return evidence.render(
        EvidenceInput(adw_id="cafe1234", workflow="adw_simple_sdlc", accepted=True, tui=result, **changes)
    )


def section(text: str, title: str) -> str:
    start = text.index(f"## {title}")
    end = text.find("\n## ", start + 1)
    return text[start : end if end > 0 else len(text)]


# --- capturing both trees ------------------------------------------------------------------------------


def test_a_changed_scene_carries_both_screens_and_an_unchanged_one_does_not_differ(run, repo):
    write(repo, "screens/status.txt", "╭─ 📊 状态 ─╮\n")
    result = capture(run, repo)
    assert result.configured and not result.error
    status, help_ = result.scenes
    assert (status.name, status.before, status.after, status.changed) == (
        "status",
        "📊 状态（卡片）\n",
        "╭─ 📊 状态 ─╮\n",
        True,
    )
    assert help_.name == "help" and not help_.changed


def test_each_side_keeps_its_screens_and_command_log_in_the_session(run, repo):
    capture(run, repo)
    for side in ("baseline", "head"):
        out = Path(run.context_handoff_dir) / "tui" / side
        assert (out / "status.txt").is_file() and (out / "manifest.json").is_file()
        assert "fake_capture.py" in (out / "command.log").read_text()


def test_a_scene_that_fails_on_one_side_is_not_compared(run, repo):
    (repo / "screens" / "help.txt").unlink()
    result = capture(run, repo)
    help_ = next(s for s in result.scenes if s.name == "help")
    assert help_.error.startswith("HEAD: timeout waiting for marker") and not help_.changed


def test_a_scene_new_on_head_says_the_baseline_had_none(run, repo):
    write(repo, "screens/chain.txt", "📜 接龙链\n")
    write(repo, "scenes.json", json.dumps({"scenes": [{"name": "status"}, {"name": "chain"}]}))
    chain = capture(run, repo).scenes[1]
    assert chain.name == "chain" and "基线" in chain.error


def test_a_capture_that_cannot_run_is_an_error_not_an_exception(run, repo):
    write(repo, "broken", "")
    result = capture(run, repo)
    assert result.scenes == []
    assert result.error.startswith("HEAD: ") and "bad scene file" in result.error
    assert "基线" not in result.error  # the baseline tree has no `broken` file


def test_a_stale_manifest_from_an_earlier_attempt_is_not_read(run, repo):
    capture(run, repo)
    write(repo, "broken", "")
    assert capture(run, repo).error


def test_a_missing_command_is_an_error_on_both_sides(run, repo):
    result = capture(run, repo, argv=["no-such-capture-binary", "{out}"])
    assert "基线" in result.error and "HEAD" in result.error and "exit 127" in result.error


def test_unconfigured_skips_without_touching_git(run):
    result = tui.capture(run, TuiParams(config=None, baseline="not-a-commit"))
    assert result == TuiResult(configured=False, baseline="not-a-commit")


def test_the_baseline_checkout_is_removed_afterwards(run, repo):
    capture(run, repo)
    assert git(repo, "worktree", "list", "--porcelain").count("worktree ") == 1


# --- the section and what it adds to the unverified list -----------------------------------------------


def screens(*scenes: TuiScene, **changes) -> TuiResult:
    return TuiResult(configured=True, baseline="a" * 40, scenes=list(scenes), **changes)


def test_a_changed_scene_is_shown_before_and_after():
    text = section(bundle(screens(TuiScene(name="status", before="旧卡片", after="新面板"))), "8. 界面截屏")
    assert "`status`：有变化" in text
    assert text.index("基线：") < text.index("旧卡片") < text.index("HEAD：") < text.index("新面板")


def test_unchanged_scenes_are_only_named():
    same = TuiScene(name="help", before="x", after="x")
    text = section(bundle(screens(same, TuiScene(name="chain", before="y", after="y"))), "8. 界面截屏")
    assert "2 个画面无变化：`help`、`chain`" in text and "```" not in text


def test_a_failed_scene_and_the_uncaptured_screens_are_unverified():
    result = screens(TuiScene(name="help", error="HEAD: timeout waiting for marker\nLast screen:\n..."))
    result.uncaptured = ["终局结算画面（需要 Bot 回合）"]
    text = bundle(result)
    assert "`help` 截屏失败" in section(text, "8. 界面截屏")
    unverified = section(text, "10. 未验证项")
    assert "截屏失败（`help`）：HEAD: timeout waiting for marker" in unverified and "Last screen" not in unverified
    assert "未截屏：终局结算画面（需要 Bot 回合）" in unverified


def test_a_capture_failure_is_shown_and_unverified_but_never_fails_the_verdict():
    text = bundle(screens(error="HEAD: `just tui-capture` exit 2, no manifest: tmux not found on PATH"))
    assert "❌ 截屏失败" in section(text, "8. 界面截屏")
    assert "截屏失败，界面没有比较：HEAD:" in section(text, "10. 未验证项")
    assert "✅ 已接受" in section(text, "1. 结论")


def test_unconfigured_says_so_and_adds_nothing_unverified():
    text = bundle(TuiResult(configured=False))
    assert "本项目未配置 TUI 截屏" in section(text, "8. 界面截屏")
    assert "截屏" not in section(text, "10. 未验证项")


def test_not_run_when_the_phase_never_ran():
    assert evidence.NOT_RUN in section(bundle(None), "8. 界面截屏")


# --- cost, split by how each provider bills -------------------------------------------------------------


def test_cost_separates_subscription_list_price_from_what_is_charged():
    usage = [
        ModelUsage(model="openai-codex/gpt-6-astra", tokens=821941, cost=2.577194),
        ModelUsage(model="deepseek/deepseek-flash", tokens=406428, cost=0.033613),
    ]
    text = section(bundle(None, tokens=1228369, cost=2.610807, usage=usage, subscription=["openai-codex"]), "11. 成本")
    assert "1,228,369 tokens · 标价合计 $2.6108" in text
    assert "| `openai-codex/gpt-6-astra` | 订阅（不扣费） | 821,941 | $2.5772 |" in text
    assert "| `deepseek/deepseek-flash` | 按量 | 406,428 | $0.0336 |" in text
    assert "实际按量扣费：**$0.0336**" in text


def test_a_model_of_unknown_billing_counts_as_paid():
    assert not evidence.subscribed(ModelUsage(model=""), ["openai-codex"])
    assert not evidence.subscribed(ModelUsage(model="openai/gpt-6"), ["openai-codex"])


def test_the_run_totals_usage_per_model():
    tracer = SimpleNamespace(session_add_usage=lambda *a: None)
    totals = SimpleNamespace(tokens=0, cost=0.0, usage={}, tracer=tracer, adw_id="cafe1234")
    Run.add_usage(totals, 100, 0.5, "openai-codex/gpt-6-astra")
    Run.add_usage(totals, 50, 0.01, "deepseek/deepseek-flash")
    Run.add_usage(totals, 10, 0.1, "openai-codex/gpt-6-astra")
    assert (totals.tokens, round(totals.cost, 2)) == (160, 0.61)
    assert [(u.model, u.tokens) for u in totals.usage.values()] == [
        ("openai-codex/gpt-6-astra", 110),
        ("deepseek/deepseek-flash", 50),
    ]
