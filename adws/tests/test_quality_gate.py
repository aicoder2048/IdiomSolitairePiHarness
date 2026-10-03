"""The factory's test gate is the justfile's `test` recipe, not a copy of it.

In the project this factory was ported from, quality.test() carried a shorter
list than the justfile, so a broken suite passed the factory's own gate.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adw_modules import quality  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


def captured_spec(monkeypatch, block):
    seen = {}
    monkeypatch.setattr(quality, "_run", lambda spec, run: seen.setdefault("spec", spec))
    block(run=None)
    return seen["spec"]


def test_the_test_block_runs_just_test(monkeypatch):
    spec = captured_spec(monkeypatch, quality.test)
    assert spec.argv == ["just", "test"]
    assert spec.timeout_seconds >= 600  # the whole suite takes a few minutes


def test_just_test_runs_every_suite():
    """The recipe the gate calls names every suite, so the gate does too."""
    justfile = (ROOT / "justfile").read_text(encoding="utf-8")
    recipe = re.search(r"^test:\n((?:    .*\n)+)", justfile, re.M)
    assert recipe, "no `test:` recipe in the justfile"
    lines = [line.strip() for line in recipe.group(1).splitlines()]
    assert lines == ["just typecheck", "bun test", "just test-adws", "just test-autoqueue"]
