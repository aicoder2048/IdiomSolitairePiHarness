"""Offline capture contracts: scripted tmux only; no terminals, models or network."""

import copy
import importlib.util
import json
import subprocess
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("tui_capture", ROOT / "scripts/tui_capture.py")
capture = importlib.util.module_from_spec(spec)
spec.loader.exec_module(capture)


class Clock:
    def __init__(self):
        self.now = 0.0
        self.sleeps = []

    def monotonic(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


class Tmux:
    def __init__(self, screens, clock, fail=None):
        self.screens = screens
        self.clock = clock
        self.fail = fail or {}
        self.calls = []
        self.scene = -1
        self.index = 0
        self.configs = []
        self.agents = []

    def __call__(self, argv, **kwargs):
        self.calls.append((argv, kwargs, self.clock.now))
        assert argv[:2] == ["tmux", "-L"]
        assert argv[3:5] == ["-u", "-f"]
        assert kwargs["timeout"] > 0
        assert kwargs["encoding"] == "utf-8"
        op = argv[6]
        if op == "new-session":
            self.scene += 1
            self.index = 0
            config = Path(argv[5])
            assert config.read_text() == ("set -g extended-keys on\nset -g extended-keys-format csi-u\n")
            self.configs.append(config)
            start = argv.index("env")
            assert argv[start : start + 2] == ["env", "-i"]
            end = argv.index("sh", start)
            env = dict(item.split("=", 1) for item in argv[start + 2 : end])
            assert env == kwargs["env"]
            agent = Path(env["PI_CODING_AGENT_DIR"])
            assert agent.is_dir() and list(agent.iterdir()) == []
            assert agent != config.parent
            self.agents.append(agent)
        failure = self.fail.get(op) if self.scene == 0 else None
        if isinstance(failure, BaseException):
            raise failure
        if failure:
            return SimpleNamespace(returncode=failure, stdout="", stderr="random details")
        text = ""
        if op == "capture-pane":
            script = self.screens[self.scene]
            text = script[min(self.index, len(script) - 1)]
            self.index += 1
        return SimpleNamespace(returncode=0, stdout=text, stderr="")


@pytest.fixture
def setup(tmp_path):
    home = tmp_path / "home"
    repo = home / "repo 'with spaces'"
    repo.mkdir(parents=True)
    config = {
        "launch": "some-tui --title 'hello world'",
        "size": [100, 30],
        "ready": "ready",
        "timeout_seconds": 0.6,
        "masks": [{"pattern": r"\d"}],
        "scenes": [
            {"name": "first", "steps": [{"text": "/status 'x'"}, {"key": "Enter"}, {"wait_for": "状态"}]},
            {"name": "second", "steps": []},
        ],
    }
    environ = {
        "PATH": "/fake/bin",
        "HOME": str(home),
        "TERM": "xterm-256color",
        "DEEPSEEK_API_KEY": "dummy-secret",
        "OTHER_TOKEN": "dummy-token",
        "TMUX": "user-socket",
        "PI_CODING_AGENT_DIR": "/user/pi",
        "PI_OFFLINE": "0",
        "PI_TELEMETRY": "1",
    }

    def run(screens=None, fail=None, document=None, raw=None, out="out", which=lambda _: "tmux", args=None):
        scene_file = tmp_path / "scenes.json"
        scene_file.write_text(raw if raw is not None else json.dumps(document if document is not None else config))
        clock = Clock()
        tmux = Tmux(
            screens or [["ready", "状态", "error is ordinary text 12\n"], ["ready", "second 34\n"]], clock, fail
        )
        output = tmp_path / out
        code = capture.main(
            args if args is not None else ["--repo", str(repo), "--scenes", str(scene_file), "--out", str(output)],
            runner=tmux,
            clock=clock.monotonic,
            sleep=clock.sleep,
            environ=environ,
            which=which,
        )
        return code, tmux, clock, output

    return SimpleNamespace(run=run, config=config, repo=repo, home=home, environ=environ)


def manifest(out):
    return json.loads((out / "manifest.json").read_text())["scenes"]


def test_masks_preserve_width_rows_whitespace_and_literal_replacement(setup):
    text = f"{setup.repo} (topic)\n~/repo 'with spaces' (other)\n⏱ 123 中Ａ\n\nkeep  \n"
    masks = [
        {"pattern": r"(?<=<repo> \()[^)]*(?=\)$)", "replace": "<branch>"},
        {"pattern": r"\d+|中Ａ"},
        {"pattern": "keep", "replace": r"\1"},
        {"pattern": "branch", "replace": "ref"},
    ]
    result = capture.normalize_screen(text, setup.repo, setup.home, masks)
    assert result == "<repo> (<ref>)\n<repo> (<ref>)\n⏱ ### ####\n\n\\1  \n"
    assert result.count("\n") == text.count("\n")
    assert capture.normalize_screen("中\nＡ\n", setup.repo, setup.home, [{"pattern": "(?s).+"}]) == "##\n##\n"
    outside = Path(str(setup.home) + "-other") / "repo"
    assert capture.normalize_screen(f"{outside}\n~/repo", outside, setup.home, []) == "<repo>\n~/repo"


def test_isolation_argv_environment_polling_and_artifacts(setup):
    code, tmux, clock, out = setup.run(
        screens=[["loading", "almost", "ready", "waiting", "状态", "screen 12\n"], ["ready", "second 34\n"]]
    )
    assert code == 0
    launches = [a for a, _, _ in tmux.calls if a[6] == "new-session"]
    assert len({a[2] for a in launches}) == 2
    for a in launches:
        assert a[7:17] == ["-d", "-s", "capture", "-x", "100", "-y", "30", "-c", str(setup.repo), "env"]
        assert a[-3:] == ["sh", "-c", setup.config["launch"]]
    for argv, kw, _ in tmux.calls:
        env = kw["env"]
        assert set(env) == {
            "PATH",
            "HOME",
            "TERM",
            "LANG",
            "PI_CODING_AGENT_DIR",
            "PI_OFFLINE",
            "PI_SKIP_VERSION_CHECK",
            "PI_TELEMETRY",
        }
        assert env["LANG"] == "en_US.UTF-8"
        assert env["PI_OFFLINE"] == env["PI_SKIP_VERSION_CHECK"] == "1"
        assert env["PI_TELEMETRY"] == "0"
        assert env["PATH"] == "/fake/bin" and env["HOME"] == str(setup.home)
        if argv[6] in ("capture-pane", "send-keys"):
            assert argv[argv.index("-t") + 1] == "capture:0.0"
    actions = [a[6:] for a, _, _ in tmux.calls if a[6] == "send-keys"]
    assert actions == [
        ["send-keys", "-t", "capture:0.0", "-l", "--", "/status 'x'"],
        ["send-keys", "-t", "capture:0.0", "--", "Enter"],
    ]
    assert clock.sleeps == [0.2, 0.2, 0.2, 0.3, 0.3]
    operations = [a[6] for a, _, _ in tmux.calls]
    assert operations == [
        "new-session",
        "capture-pane",
        "capture-pane",
        "capture-pane",
        "send-keys",
        "send-keys",
        "capture-pane",
        "capture-pane",
        "capture-pane",
        "kill-server",
        "new-session",
        "capture-pane",
        "capture-pane",
        "kill-server",
    ]
    captures = [t for a, _, t in tmux.calls if a[6] == "capture-pane"]
    assert captures[:3] == [0, 0.2, 0.4]
    assert captures[5] - captures[4] == pytest.approx(0.3)
    assert captures[-1] - captures[-2] == pytest.approx(0.3)
    assert (out / "first.txt").read_text() == "screen ##\n"
    assert manifest(out) == [
        {"name": "first", "file": "first.txt", "ok": True, "error": None},
        {"name": "second", "file": "second.txt", "ok": True, "error": None},
    ]
    assert_cleaned(tmux)


def assert_cleaned(tmux):
    started = [a[2] for a, _, _ in tmux.calls if a[6] == "new-session"]
    killed = [a[2] for a, _, _ in tmux.calls if a[6] == "kill-server"]
    assert killed == started
    assert all(not p.exists() for p in tmux.configs + tmux.agents)


@pytest.mark.parametrize(
    "locale", [{}, {"LANG": "zh_CN.UTF-8"}, {"LC_ALL": "C.UTF-8"}, {"LANG": "C", "LC_ALL": "C.UTF-8"}]
)
def test_locale_and_fallbacks(locale, tmp_path):
    env = capture.pane_environment(locale, tmp_path)
    assert env["PATH"] and env["HOME"] and env["TERM"]
    assert {k: v for k, v in env.items() if k in ("LANG", "LC_ALL")} == (locale or {"LANG": "en_US.UTF-8"})


@pytest.mark.parametrize(
    "change",
    [
        lambda c: c.pop("launch"),
        lambda c: c.update(extra=True),
        lambda c: c.update(size=[True, 30]),
        lambda c: c.update(size=[0, 30]),
        lambda c: c.update(size=[100]),
        lambda c: c.update(timeout_seconds=True),
        lambda c: c.update(timeout_seconds=0),
        lambda c: c.update(timeout_seconds=float("nan")),
        lambda c: c.update(timeout_seconds=float("inf")),
        lambda c: c.update(ready=""),
        lambda c: c.update(launch="x\0y"),
        lambda c: c.update(masks=[{"pattern": "["}]),
        lambda c: c.update(masks=[{"pattern": "x", "replace": 42}]),
        lambda c: c.update(masks=[{"pattern": "x", "extra": "x"}]),
        lambda c: c.update(scenes=[]),
        lambda c: c["scenes"][1].update(name="../bad"),
        lambda c: c["scenes"][1].update(name="UPPER"),
        lambda c: c["scenes"][1].update(name="first"),
        lambda c: c["scenes"][1].update(steps=[{"sleep": 1}]),
        lambda c: c["scenes"][1].update(steps=[{"text": "x", "key": "Enter"}]),
        lambda c: c["scenes"][1].update(steps=[{"key": ""}]),
        lambda c: c["scenes"][1].update(steps=[{"wait_for": ""}]),
        lambda c: c["scenes"][1].update(steps="x"),
        lambda c: c["scenes"][1].pop("steps"),
    ],
)
def test_invalid_document_is_preflight_failure(setup, change):
    document = copy.deepcopy(setup.config)
    change(document)
    code, tmux, _, out = setup.run(document=document)
    assert code == 2
    assert tmux.calls == []
    assert not out.exists()


@pytest.mark.parametrize("raw", ["{", "[]", "null", '{"launch": 3}'])
def test_invalid_json(setup, raw):
    code, tmux, _, out = setup.run(raw=raw)
    assert code == 2 and not tmux.calls and not out.exists()


def test_cli_preflight(setup, tmp_path):
    for args in ([], ["--repo", str(tmp_path / "missing"), "--scenes", "missing", "--out", str(tmp_path / "unused")]):
        code, tmux, _, _ = setup.run(args=args)
        assert code == 2 and not tmux.calls
    code, tmux, _, out = setup.run(which=lambda _: None)
    assert code == 2 and not tmux.calls and not out.exists()
    (tmp_path / "file").write_text("not a directory")
    code, tmux, _, _ = setup.run(out="file/nested")
    assert code == 2 and not tmux.calls


@pytest.mark.parametrize("stage", ["ready", "step"])
def test_timeout_continues_and_is_reproducible(setup, stage):
    last = f"{setup.repo}\nlast 123\n"
    screens = [[last] if stage == "ready" else ["ready", last], ["ready", "ok\n"]]
    results = []
    for out_name in ("one", "two"):
        code, tmux, clock, out = setup.run(screens=screens, out=out_name)
        assert code == 1
        scenes = manifest(out)
        assert scenes[0]["ok"] is False and scenes[1]["ok"] is True
        assert "<repo>\nlast ###\n" in scenes[0]["error"]
        assert stage in scenes[0]["error"]
        assert (out / "first.txt").read_text() == "<repo>\nlast ###\n"
        assert clock.now == pytest.approx(0.9)
        assert_cleaned(tmux)
        results.append({p.name: p.read_bytes() for p in out.iterdir()})
    assert results[0] == results[1]


def test_success_reproducibility_and_exit_status_not_stdout(setup):
    runs = [setup.run(out=name) for name in ("one", "two")]
    assert all(code == 0 for code, _, _, _ in runs)
    assert {p.name: p.read_bytes() for p in runs[0][3].iterdir()} == {
        p.name: p.read_bytes() for p in runs[1][3].iterdir()
    }


@pytest.mark.parametrize("op", ["new-session", "send-keys", "capture-pane"])
@pytest.mark.parametrize("failure", [7, OSError("random path"), subprocess.TimeoutExpired("random argv", 1)])
def test_command_failure_cleanup_and_continuation(setup, tmp_path, op, failure):
    out = tmp_path / "out"
    out.mkdir()
    (out / "first.txt").write_text("stale screen")
    code, tmux, _, out = setup.run(fail={op: failure})
    assert code == 1
    scenes = manifest(out)
    assert scenes[0]["ok"] is False and scenes[1]["ok"] is True
    assert op in scenes[0]["error"] and "random" not in scenes[0]["error"]
    if op in ("new-session", "capture-pane"):
        assert (out / "first.txt").read_text() == ""
    assert_cleaned(tmux)


def test_cleanup_failure_is_reported_without_hiding_original(setup):
    code, tmux, _, out = setup.run(fail={"send-keys": 7, "kill-server": 9})
    assert code == 1
    assert "send-keys" in manifest(out)[0]["error"]
    assert "kill-server" in manifest(out)[0]["error"]
    assert_cleaned(tmux)
    code, tmux, _, out = setup.run(fail={"kill-server": 9}, out="cleanup-only")
    assert code == 1 and "kill-server" in manifest(out)[0]["error"]
    assert_cleaned(tmux)


def test_interruption_still_cleans_up(setup):
    clock = Clock()
    tmux = Tmux([["ready"]], clock, {"new-session": KeyboardInterrupt()})
    with pytest.raises(KeyboardInterrupt):
        capture.capture_scene(
            setup.config, setup.config["scenes"][0], setup.repo, setup.environ, tmux, clock.monotonic, clock.sleep
        )
    assert_cleaned(tmux)


def test_example():
    config = capture.load_scenes(ROOT / "scripts/tui_scenes.example.json")
    assert config["size"] == [100, 30]
    assert config["ready"] == "成语接龙开始"
    assert config["timeout_seconds"] == 10
    assert (
        config["launch"]
        == "pi -ne -nbt -ns -np -nc --no-session --thinking off -e ./src/extension/index.ts --model deepseek/deepseek-flash"
    )
    assert [s["name"] for s in config["scenes"]] == ["status", "help"]
    assert len(config["masks"]) == 3
    assert config["scenes"][0]["steps"] == [{"text": "/status"}, {"key": "Enter"}, {"wait_for": "📊 状态"}]
    assert config["scenes"][1]["steps"] == [{"text": "/help"}, {"key": "Enter"}, {"wait_for": "📖 成语接龙"}]


def test_empty_text_is_noop_and_unrelated_files_survive(setup, tmp_path):
    setup.config["scenes"][0]["steps"].insert(0, {"text": ""})
    out = tmp_path / "out"
    out.mkdir()
    (out / "unrelated.txt").write_text("keep me")
    code, tmux, _, _ = setup.run()
    assert code == 0
    assert len([a for a, _, _ in tmux.calls if a[6] == "send-keys"]) == 2
    assert (out / "unrelated.txt").read_text() == "keep me"


@pytest.mark.parametrize("filename", ["first.txt", "manifest.json"])
def test_artifact_write_failure_returns_one_and_cleans_all_scenes(setup, tmp_path, filename):
    out = tmp_path / "out"
    (out / filename).mkdir(parents=True)
    code, tmux, _, _ = setup.run()
    assert code == 1
    assert (out / "second.txt").is_file()
    if filename == "first.txt":
        scenes = manifest(out)
        assert scenes[0]["ok"] is False
        assert "write first.txt" in scenes[0]["error"]
        assert scenes[1]["ok"] is True
    assert_cleaned(tmux)


def test_already_exited_server_is_not_cleanup_failure(setup, monkeypatch):
    original = Tmux.__call__

    def run(self, argv, **kwargs):
        result = original(self, argv, **kwargs)
        if argv[6] == "kill-server":
            result.returncode = 1
            result.stderr = f"no server running on {argv[2]}"
        return result

    monkeypatch.setattr(Tmux, "__call__", run)
    code, tmux, _, _ = setup.run()
    assert code == 0
    assert_cleaned(tmux)


def test_poll_client_timeout_is_bounded_by_remaining_deadline(setup):
    code, tmux, _, _ = setup.run(screens=[["loading"], ["ready", "ok"]])
    assert code == 1
    first_socket = tmux.calls[0][0][2]
    limits = [kw["timeout"] for a, kw, _ in tmux.calls if a[2] == first_socket and a[6] == "capture-pane"]
    assert limits == pytest.approx([0.6, 0.4, 0.2])
    assert_cleaned(tmux)
