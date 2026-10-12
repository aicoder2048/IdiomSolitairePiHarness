#!/usr/bin/env python3
"""Capture trusted, model-free TUI scenes in isolated tmux servers (stdlib only)."""

import argparse
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import uuid
from pathlib import Path


class SceneError(Exception):
    """Stable diagnostic safe to include in reproducible artifacts."""


def _object(value, required, optional=()):
    if not isinstance(value, dict) or not set(required) <= value.keys():
        raise ValueError(f"expected object with fields: {', '.join(required)}")
    if value.keys() - set(required) - set(optional):
        raise ValueError("unrecognized object fields")


def _string(value, empty=False):
    if not isinstance(value, str) or (not empty and not value) or "\0" in value:
        raise ValueError("expected a string without NUL" + ("" if empty else " (nonempty)"))


def load_scenes(path):
    """Validate the entire file before any output or tmux activity."""
    with Path(path).open(encoding="utf-8") as stream:
        config = json.load(stream)
    _object(config, ("launch", "size", "ready", "timeout_seconds", "masks", "scenes"))
    for field in ("launch", "ready"):
        _string(config[field])
    size = config["size"]
    if not isinstance(size, list) or len(size) != 2 or any(type(n) is not int or n <= 0 for n in size):
        raise ValueError("size must be two positive integers")
    timeout = config["timeout_seconds"]
    if type(timeout) not in (int, float) or not 0 < timeout < math.inf:
        raise ValueError("timeout_seconds must be finite and positive")
    if not isinstance(config["masks"], list):
        raise ValueError("masks must be a list")
    for mask in config["masks"]:
        _object(mask, ("pattern",), ("replace",))
        _string(mask["pattern"], empty=True)
        re.compile(mask["pattern"], re.MULTILINE)
        if "replace" in mask:
            _string(mask["replace"], empty=True)
    if not isinstance(config["scenes"], list) or not config["scenes"]:
        raise ValueError("scenes must be a nonempty list")
    names = set()
    for scene in config["scenes"]:
        _object(scene, ("name", "steps"))
        name = scene["name"]
        _string(name)
        if not re.fullmatch(r"[a-z0-9_-]+", name) or name in names:
            raise ValueError("scene names must be unique and match [a-z0-9_-]+")
        names.add(name)
        if not isinstance(scene["steps"], list):
            raise ValueError("steps must be a list")
        for step in scene["steps"]:
            if not isinstance(step, dict) or len(step) != 1:
                raise ValueError("each step must contain exactly one action")
            action, value = next(iter(step.items()))
            if action not in ("text", "key", "wait_for"):
                raise ValueError(f"unknown step action: {action}")
            _string(value, empty=action == "text")
    return config


def pane_environment(environ, agent_dir):
    """Never inherit credentials, Pi settings, or the caller's tmux socket."""
    env = {
        "PATH": environ.get("PATH", os.defpath),
        "HOME": environ.get("HOME", str(Path.home())),
        "TERM": environ.get("TERM", "screen-256color"),
    }
    env.update({key: environ[key] for key in ("LANG", "LC_ALL") if key in environ})
    if "LANG" not in env and "LC_ALL" not in env:
        env["LANG"] = "en_US.UTF-8"
    env.update(
        PI_CODING_AGENT_DIR=str(agent_dir),
        PI_OFFLINE="1",
        PI_SKIP_VERSION_CHECK="1",
        PI_TELEMETRY="0",
    )
    return env


def normalize_screen(screen, repo, home, masks):
    screen = screen.replace(str(repo), "<repo>")
    try:
        relative = Path(repo).relative_to(Path(home))
    except ValueError:
        pass
    else:
        shorthand = "~" if relative == Path(".") else f"~/{relative}"
        screen = screen.replace(shorthand, "<repo>")

    def hashes(match):
        return "".join(
            char if char in "\r\n" else "##" if unicodedata.east_asian_width(char) in ("W", "F") else "#"
            for char in match.group()
        )

    for mask in masks:
        replacement = (lambda match, value=mask["replace"]: value) if "replace" in mask else hashes
        screen = re.sub(mask["pattern"], replacement, screen, flags=re.MULTILINE)
    return screen


def capture_scene(config, scene, repo, environ, runner, clock, sleep):
    """Return (last screen, stable error); always tear down the unique server."""
    last_screen = ""
    errors = []
    timeout = config["timeout_seconds"]
    try:
        with tempfile.TemporaryDirectory(prefix="tui-capture-") as temporary:
            directory = Path(temporary)
            config_path = directory / "tmux.conf"
            agent_dir = directory / "agent"
            prefix = ["tmux", "-L", f"tui-capture-{uuid.uuid4().hex}", "-u", "-f", str(config_path)]
            env = pane_environment(environ, agent_dir)

            def command(args, limit=None, cleanup=False):
                operation = args[0]
                try:
                    result = runner(
                        prefix + args,
                        env=env,
                        capture_output=True,
                        encoding="utf-8",
                        timeout=timeout if limit is None else limit,
                    )
                except subprocess.TimeoutExpired:
                    raise SceneError(f"{operation}: command timed out") from None
                except (OSError, UnicodeError) as exc:
                    raise SceneError(f"{operation}: {type(exc).__name__}") from None
                if result.returncode != 0:
                    # A TUI may have already exited, taking its server with it.
                    absent = any(
                        message in result.stderr
                        for message in (
                            "no server running",
                            "No such file or directory",
                            "Connection refused",
                        )
                    )
                    if not (cleanup and absent):
                        raise SceneError(f"{operation}: exit {result.returncode}")
                return result.stdout

            def screen(limit=None):
                nonlocal last_screen
                last_screen = command(["capture-pane", "-p", "-t", "capture:0.0"], limit)
                return last_screen

            def wait_for(marker, stage):
                deadline = clock() + timeout
                while True:
                    remaining = deadline - clock()
                    if remaining <= 0:
                        raise SceneError(f"{stage}: timed out waiting for {marker!r}")
                    if marker in screen(remaining):
                        return
                    remaining = deadline - clock()
                    if remaining > 0:
                        sleep(min(0.2, remaining))

            try:
                config_path.write_text("set -g extended-keys on\nset -g extended-keys-format csi-u\n", encoding="utf-8")
                agent_dir.mkdir()
                command(
                    [
                        "new-session",
                        "-d",
                        "-s",
                        "capture",
                        "-x",
                        str(config["size"][0]),
                        "-y",
                        str(config["size"][1]),
                        "-c",
                        str(repo),
                        "env",
                        "-i",
                        *[f"{key}={value}" for key, value in env.items()],
                        "sh",
                        "-c",
                        config["launch"],
                    ]
                )
                wait_for(config["ready"], "ready")
                for index, step in enumerate(scene["steps"], 1):
                    action, value = next(iter(step.items()))
                    if action == "wait_for":
                        wait_for(value, f"step {index}")
                    elif action == "key":
                        command(["send-keys", "-t", "capture:0.0", "--", value])
                    elif value:
                        command(["send-keys", "-t", "capture:0.0", "-l", "--", value])
                sleep(0.3)
                screen()
            except SceneError as exc:
                errors.append(str(exc))
            finally:
                try:
                    command(["kill-server"], cleanup=True)
                except SceneError as exc:
                    errors.append(str(exc))
    except (OSError, UnicodeError) as exc:
        errors.append(f"scene resources: {type(exc).__name__}")
    return last_screen, "; ".join(errors) if errors else None


def run_scenes(config, repo, out, environ, runner, clock, sleep):
    entries = []
    home = Path(environ.get("HOME", str(Path.home()))).resolve()
    for scene in config["scenes"]:
        screen, error = capture_scene(config, scene, repo, environ, runner, clock, sleep)
        screen = normalize_screen(screen, repo, home, config["masks"])
        if error:
            error = normalize_screen(error, repo, home, config["masks"]) + "\nLast screen:\n" + screen
        filename = f"{scene['name']}.txt"
        try:
            (out / filename).write_text(screen, encoding="utf-8")
        except OSError as exc:
            error = (error + "\n" if error else "") + f"write {filename}: {type(exc).__name__}"
        entries.append({"name": scene["name"], "file": filename, "ok": error is None, "error": error})
    try:
        (out / "manifest.json").write_text(
            json.dumps({"scenes": entries}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except OSError as exc:
        print(f"manifest write failed: {exc}", file=sys.stderr)
        return 1
    for entry in entries:
        if entry["error"]:
            print(f"{entry['name']}: {entry['error']}", file=sys.stderr)
    return 0 if all(entry["ok"] for entry in entries) else 1


def main(argv=None, *, runner=subprocess.run, clock=time.monotonic, sleep=time.sleep, environ=None, which=shutil.which):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--scenes", required=True)
    parser.add_argument("--out", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return exc.code
    try:
        repo = Path(args.repo).expanduser().resolve()
        if not repo.is_dir():
            raise ValueError("--repo must be an existing directory")
        config = load_scenes(Path(args.scenes).expanduser())
        if which("tmux") is None:
            raise ValueError("tmux not found on PATH")
        out = Path(args.out).expanduser().resolve()
        out.mkdir(parents=True, exist_ok=True)
        if not os.access(out, os.W_OK):
            raise ValueError("--out must be writable")
    except (OSError, ValueError, re.error) as exc:
        print(f"tui_capture: {exc}", file=sys.stderr)
        return 2
    return run_scenes(config, repo, out, os.environ if environ is None else environ, runner, clock, sleep)


if __name__ == "__main__":
    raise SystemExit(main())
