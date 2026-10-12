"""TUI screenshots: the same scenes captured on the baseline and on HEAD, as text.

"The overlay renders" from an agent is a claim; two screens side by side are
evidence. The project's capture command (scripts/tui_capture.py, through
`just tui-capture`) starts its TUI in an isolated terminal, plays each scene's
keys and writes the masked screen to `<scene>.txt`, with a `manifest.json`
saying which scenes succeeded. This module runs it twice — on a checkout of the
baseline and on the repo — and compares scene by scene.

It never imports the engine: the command is a subprocess, so `adws/` stays
project-agnostic and the engine stays stdlib-only. Both trees are captured with
HEAD's engine and HEAD's scene file; only the app under capture differs.

A failed capture is evidence too, not a gate: it becomes an unverified item and
the run goes on. Screenshots show what changed; whether the change is right is
the reviewer's call and the human's.
"""

from __future__ import annotations

import json
import shlex
import shutil
from pathlib import Path

from . import baseline, proof
from .data_types import TuiConfig, TuiParams, TuiResult, TuiScene

Screens = dict[str, tuple[str, str]]  # scene name -> (masked screen, error or "")


def _manifest(out: Path) -> Screens:
    screens = {}
    for entry in json.loads((out / "manifest.json").read_text(encoding="utf-8"))["scenes"]:
        text = out / entry["file"]
        screens[entry["name"]] = (text.read_text(encoding="utf-8") if text.is_file() else "", entry.get("error") or "")
    return screens


def _side(run, config: TuiConfig, out: Path, tree: Path) -> tuple[Screens, str]:
    """Capture every scene of `tree` into `out`. Returns the scenes, or an error saying why there are none."""
    root = Path(run.repo_root)
    values = {"scenes": str(root / config.scenes), "out": str(out), "repo": str(tree)}
    argv = [arg.format(**values) for arg in config.argv]
    shutil.rmtree(out, ignore_errors=True)  # a joined run's old manifest must not stand in for this one
    out.mkdir(parents=True)
    returncode, output = proof.execute(argv, root, config.timeout_seconds)
    (out / "command.log").write_text(f"$ {shlex.join(argv)}\nexit: {returncode}\n\n{output}", encoding="utf-8")
    try:
        return _manifest(out), ""
    except (OSError, ValueError, KeyError, TypeError):
        tail = "\n".join(output.strip().splitlines()[-5:])
        return {}, f"`{shlex.join(config.argv)}` exit {returncode}, no manifest: {tail or '(no output)'}"


def capture(run, params: TuiParams) -> TuiResult:
    """Capture the configured scenes on the baseline and on HEAD, and pair them up by name."""
    config = params.config
    if config is None:
        return TuiResult(configured=False, baseline=params.baseline)
    out = Path(run.context_handoff_dir) / "tui"
    result = TuiResult(
        configured=True,
        baseline=params.baseline,
        uncaptured=config.uncaptured,
        artifacts=[str(out / "baseline"), str(out / "head")],
    )
    try:
        with baseline.checkout(run, params.baseline) as tree:
            before, before_error = _side(run, config, out / "baseline", tree)
    except RuntimeError as e:  # the baseline could not be checked out
        before, before_error = {}, str(e)
    after, after_error = _side(run, config, out / "head", Path(run.repo_root))
    if before_error or after_error:
        result.error = "; ".join(
            f"{side}: {err}" for side, err in (("基线", before_error), ("HEAD", after_error)) if err
        )
        return result
    for name, (screen, head_error) in after.items():
        old, base_error = before.get(name, ("", "基线上没有这个场景"))
        errors = [f"{side}: {err}" for side, err in (("基线", base_error), ("HEAD", head_error)) if err]
        result.scenes.append(TuiScene(name=name, before=old, after=screen, error="; ".join(errors)))
    return result
