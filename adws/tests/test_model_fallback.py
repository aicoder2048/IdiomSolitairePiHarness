"""A model call that hangs or dies must not stall the factory, and may fall back once.

Run 614fe8f4's reviewer (deepseek/deepseek-flash) sent one request and then
waited 15 minutes at 0% CPU: the provider accepted the connection and never
answered. `agent_pi.run` had no timeout and SSSF had no second model, so the
whole run died when the process was killed by hand.
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adw_modules import agent_pi, agents  # noqa: E402
from adw_modules.data_types import PiRequest  # noqa: E402

FAKE_PI = r"""#!/usr/bin/env python3
import json, sys, time
model = sys.argv[sys.argv.index("--model") + 1]
def emit(event):
    print(json.dumps(event), flush=True)
if model == "hang":
    time.sleep(120)
elif model == "fail":
    print("provider exploded", file=sys.stderr)
    sys.exit(3)
elif model == "slow":
    for _ in range(4):
        emit({"type": "message_update"})
        time.sleep(1)
    emit({"type": "message_end", "message": {"role": "assistant", "content": [{"type": "text", "text": "slow ok"}], "usage": {}}})
else:
    emit({"type": "message_end", "message": {"role": "assistant", "content": [{"type": "text", "text": "ok from " + model}], "usage": {}}})
"""


@pytest.fixture
def fake_pi(tmp_path, monkeypatch):
    script = tmp_path / "pi"
    script.write_text(FAKE_PI)
    script.chmod(0o755)
    monkeypatch.setattr(agent_pi, "PI_PATH", str(script))
    monkeypatch.setattr(agent_pi, "resolve_model", lambda pattern: tuple(pattern.split("/", 1)))
    monkeypatch.setattr(agent_pi, "context_window", lambda provider, model_id: 0)
    monkeypatch.setattr(agent_pi, "IDLE_POLL_S", 0.2)
    return tmp_path


def request(tmp_path, model, idle_timeout_s=600):
    return PiRequest(
        prompt="hi",
        system_prompt="sys",
        model=model,
        session_id="s",
        session_dir=str(tmp_path / "sessions"),
        raw_output_path=str(tmp_path / "raw.jsonl"),
        cwd=str(tmp_path),
        idle_timeout_s=idle_timeout_s,
    )


# ── agent_pi.run ─────────────────────────────────────────────────────────────


def test_silent_model_is_killed_after_idle_timeout(fake_pi):
    started = time.monotonic()
    with pytest.raises(agent_pi.PiUnavailable, match="no output for 1s"):
        agent_pi.run(request(fake_pi, "p/hang", idle_timeout_s=1))
    assert time.monotonic() - started < 15


def test_steady_output_resets_the_idle_timer(fake_pi):
    result = agent_pi.run(request(fake_pi, "p/slow", idle_timeout_s=2))
    assert result.text == "slow ok"


def test_nonzero_exit_without_an_answer_is_unavailable(fake_pi):
    with pytest.raises(agent_pi.PiUnavailable, match="provider exploded"):
        agent_pi.run(request(fake_pi, "p/fail"))


def test_unavailable_is_still_a_runtime_error_for_existing_callers(fake_pi):
    with pytest.raises(RuntimeError):
        agent_pi.run(request(fake_pi, "p/fail"))


def test_a_healthy_model_is_unaffected(fake_pi):
    assert agent_pi.run(request(fake_pi, "p/ok")).text == "ok from ok"


# ── agents.call_with_fallback ───────────────────────────────────────────────


def recorder():
    calls, switches = [], []

    def on_fallback(primary, fallback, error):
        switches.append((primary, fallback, str(error)))

    return calls, switches, on_fallback


def test_primary_success_never_touches_the_fallback():
    calls, switches, on_fallback = recorder()

    def call(model):
        calls.append(model)
        return f"ok {model}"

    assert agents.call_with_fallback(call, "a/primary", "b/backup", on_fallback) == ("ok a/primary", "a/primary")
    assert calls == ["a/primary"] and switches == []


def test_unavailable_primary_retries_once_on_the_fallback():
    calls, switches, on_fallback = recorder()

    def call(model):
        calls.append(model)
        if model == "a/primary":
            raise agent_pi.PiUnavailable("silent for 600s")
        return f"ok {model}"

    assert agents.call_with_fallback(call, "a/primary", "b/backup", on_fallback) == ("ok b/backup", "b/backup")
    assert calls == ["a/primary", "b/backup"]
    assert switches == [("a/primary", "b/backup", "silent for 600s")]


def test_without_a_fallback_the_failure_propagates():
    def call(model):
        raise agent_pi.PiUnavailable("down")

    with pytest.raises(agent_pi.PiUnavailable):
        agents.call_with_fallback(call, "a/primary", None, lambda *a: None)


def test_fallback_equal_to_primary_is_not_a_second_try():
    calls = []

    def call(model):
        calls.append(model)
        raise agent_pi.PiUnavailable("down")

    with pytest.raises(agent_pi.PiUnavailable):
        agents.call_with_fallback(call, "a/primary", "a/primary", lambda *a: None)
    assert calls == ["a/primary"]


def test_a_failing_fallback_propagates_its_own_error():
    def call(model):
        raise agent_pi.PiUnavailable(f"{model} down")

    with pytest.raises(agent_pi.PiUnavailable, match="b/backup down"):
        agents.call_with_fallback(call, "a/primary", "b/backup", lambda *a: None)


def test_other_errors_are_not_masked_by_the_fallback():
    calls = []

    def call(model):
        calls.append(model)
        raise ValueError("bad prompt")

    with pytest.raises(ValueError):
        agents.call_with_fallback(call, "a/primary", "b/backup", lambda *a: None)
    assert calls == ["a/primary"]


# ── config ───────────────────────────────────────────────────────────────────


def write_config(tmp_path, defaults, reviewer_extra=""):
    prompts = tmp_path / "p.md"
    prompts.write_text("x")
    text = f"""
defaults:
  model: a/primary
{defaults}
agents:
  - name: builder
    prompt_engineering: {{system: {prompts}, user: {prompts}}}
  - name: reviewer
    model: c/reviewer
{reviewer_extra}
    prompt_engineering: {{system: {prompts}, user: {prompts}}}
"""
    path = tmp_path / "sssf.yaml"
    path.write_text(text)
    return str(path)


def test_defaults_propagate_fallback_and_timeout(tmp_path):
    cfg = agents.load_config(write_config(tmp_path, "  fallback_model: b/backup\n  idle_timeout_s: 300"))
    builder = agents.resolve(cfg, "builder")
    assert builder.fallback_model == "b/backup" and builder.idle_timeout_s == 300


def test_agent_override_wins(tmp_path):
    cfg = agents.load_config(
        write_config(tmp_path, "  fallback_model: b/backup", "    fallback_model: d/other\n    idle_timeout_s: 120")
    )
    reviewer = agents.resolve(cfg, "reviewer")
    assert reviewer.fallback_model == "d/other" and reviewer.idle_timeout_s == 120


def test_omitted_settings_keep_the_old_behaviour(tmp_path):
    cfg = agents.load_config(write_config(tmp_path, ""))
    builder = agents.resolve(cfg, "builder")
    assert builder.fallback_model is None and builder.idle_timeout_s == agent_pi.DEFAULT_IDLE_TIMEOUT_S


def test_validate_rejects_an_unresolvable_fallback(tmp_path, monkeypatch):
    def resolve_model(pattern):
        if pattern == "z/missing":
            raise ValueError("no model z/missing")
        return tuple(pattern.split("/", 1))

    monkeypatch.setattr(agent_pi, "resolve_model", resolve_model)
    cfg = agents.load_config(write_config(tmp_path, "  fallback_model: z/missing"))
    with pytest.raises(SystemExit, match="fallback_model"):
        agents.validate(cfg, ["builder"])


def test_validate_rejects_a_non_positive_timeout(tmp_path):
    with pytest.raises(Exception, match="idle_timeout_s"):
        agents.load_config(write_config(tmp_path, "  idle_timeout_s: 0"))


def test_every_project_agent_has_a_different_fallback_model():
    root = Path(__file__).resolve().parents[2]
    cfg = agents.load_config(str(root / "adws/adw_sssf_config/sssf.config.yaml"))
    for agent in cfg.agents:
        assert agent.fallback_model and agent.fallback_model != agent.model, agent.name


def test_execute_keeps_its_agent_call_parameter():
    """Regression for run fe7aaf57: a local `call` function shadowed execute's `call: AgentCall`,
    so the phase died after the planner finished with "'function' object has no attribute 'output_type'"."""
    import ast
    import inspect
    import textwrap

    tree = ast.parse(textwrap.dedent(inspect.getsource(agents.execute)))
    params = {a.arg for a in tree.body[0].args.args}
    local_defs = {n.name for n in ast.walk(tree.body[0]) if isinstance(n, ast.FunctionDef) and n is not tree.body[0]}
    assert not params & local_defs, params & local_defs
