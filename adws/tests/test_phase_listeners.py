"""Run.listeners hear every phase as it ends, and a broken listener never fails a phase.

adw_issue reports the factory's progress to the GitHub issue through this; the
trace and the console stay the run's own record.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adw_modules.data_types import PhaseParams  # noqa: E402
from adw_modules.runner import Run  # noqa: E402
from adw_modules.tracer import Tracer  # noqa: E402


@pytest.fixture
def run(tmp_path, monkeypatch):
    """A real Run over a throwaway trace db, in a throwaway git repo."""
    subprocess.run(["git", "init", "-q"], cwd=tmp_path, check=True)
    monkeypatch.chdir(tmp_path)
    data = tmp_path / "data"
    cfg = SimpleNamespace(
        defaults=SimpleNamespace(data_dir=str(data)), observability=SimpleNamespace(db=str(data / "t.db"))
    )
    tracer = Tracer(data / "t.db", data / "events.jsonl")
    tracer.session_start("abcd1234", "tester")
    Run.listeners.clear()
    yield Run(cfg=cfg, adw_id="abcd1234", tracer=tracer, engineer="tester")
    Run.listeners.clear()


def params(name: str) -> PhaseParams:
    return PhaseParams(name=name, kind="code", owner="git", description=f"a test phase that does {name} things")


def test_listeners_hear_success_and_failure(run):
    heard = []
    Run.listeners.append(lambda phase: heard.append((phase.params.name, phase.status, phase.error)))
    with run.phase(params("one")):
        pass
    with pytest.raises(RuntimeError), run.phase(params("two")):
        raise RuntimeError("boom")
    assert heard == [("one", "success", None), ("two", "fail", "boom")]


def test_a_raising_listener_is_dropped_and_the_phase_still_passes(run):
    heard = []

    def bad(_phase):
        raise ValueError("reporter down")

    Run.listeners.extend([bad, lambda phase: heard.append(phase.params.name)])
    with run.phase(params("one")):
        pass
    with run.phase(params("two")):
        pass
    assert run.phases[-1].status == "success"
    assert heard == ["one", "two"]
    assert bad not in Run.listeners
