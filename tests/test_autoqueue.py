"""Offline runner contract: real local Git, canned GitHub, no models or credentials.

Ported with scripts/autoqueue.py from OptionTradingPiHarness; labels are factory:* here.
"""

import json
import os
import select
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

ROOT = Path(__file__).resolve().parents[1]
REAL_JUST = shutil.which("just")
REAL_GIT = shutil.which("git")

SHIM = r"""
import json, os, pathlib, subprocess, sys
name = pathlib.Path(sys.argv[0]).name
args = sys.argv[1:]
config = json.loads(pathlib.Path(os.environ["FAKE_CONFIG"]).read_text())
root = pathlib.Path(os.environ["FAKE_ROOT"])
record = dict(name=name, args=args, cwd=os.getcwd(), parent_pid=os.getppid(), marker=os.environ.get("QUEUE_MARKER"),
              worktrees=sorted(p.name for p in (root / ".autoqueue/worktrees").glob("*")))
lock = root / ".autoqueue/lock"
record["lock"] = lock.read_text() if lock.exists() else None
if name == "just" and args != ["autoqueue"]:
    record["head"] = subprocess.check_output([os.environ["FAKE_GIT"], "rev-parse", "HEAD"], text=True).strip()
    record["branch"] = subprocess.check_output([os.environ["FAKE_GIT"], "branch", "--show-current"], text=True).strip()
    record["local_only"] = pathlib.Path("local-only").exists()
with open(os.environ["FAKE_RECORD"], "a") as f:
    f.write(json.dumps(record) + "\n")
for reject in config.get("reject", []):
    if [name, *args][:len(reject)] == reject:
        print("synthetic refusal", file=sys.stderr)
        sys.exit(7)
if name == "git":
    sys.exit(subprocess.call([os.environ["FAKE_GIT"], *args]))
if name == "gh":
    if args[:2] == ["issue", "list"]:
        print(config.get("raw_issues", json.dumps(config["issues"])))
    elif args[:2] == ["pr", "list"] and "--label" in args:
        print(json.dumps(config.get("revise_prs", [])))
    elif args[:2] == ["pr", "list"]:
        print(config.get("raw_prs", json.dumps(config.get("prs", []))))
    elif args[:2] == ["api", "user"]:
        print(config.get("gh_user", "owner"))
elif name == "uv":
    print("uv output")
elif name == "bun":
    print("bun install output")
    sys.exit(config.get("bun_code", 0))
elif name == "just":
    record_input = sys.stdin.read()
    assert record_input == ""
    if args[-1:] == ["--check"]:
        sys.exit(config.get("check_code", 0))
    if args == ["autoqueue"]:
        print("cron fake just")
        sys.exit(0)
    pathlib.Path("recovery.txt").write_text("uncommitted recovery")
    pathlib.Path(".venv").mkdir(exist_ok=True)
    pathlib.Path(".venv/artifact").write_text("ignored runtime")
    for i in range(30):
        print(f"output-{i:02d} ``` error-looking text", file=sys.stderr if i % 2 else sys.stdout, flush=True)
    sys.exit(config.get("codes", {}).get(args[-1], 0))
"""


def issue(number, *, assigned=False, failed=False, author="owner"):
    return dict(
        number=number,
        title=f"Issue {number}",
        author={"login": author},
        assignees=[{"login": "worker"}] if assigned else [],
        labels=[{"name": "factory:queued"}] + ([{"name": "factory:needs-human"}] if failed else []),
    )


@pytest.fixture
def harness(tmp_path):
    root = tmp_path / "repo's % space"
    root.mkdir()
    bin_dir = tmp_path / "bin's % space"
    bin_dir.mkdir()
    config_path = tmp_path / "config.json"
    record_path = tmp_path / "calls.jsonl"
    home = tmp_path / "home"
    home.mkdir()
    env = dict(
        PATH=str(bin_dir) + os.pathsep + os.environ["PATH"],
        HOME=str(home),
        GIT_CONFIG_NOSYSTEM="1",
        GIT_CONFIG_GLOBAL=os.devnull,
        JUST_NO_DOTENV="true",
        FAKE_GIT=REAL_GIT,
        FAKE_CONFIG=str(config_path),
        FAKE_RECORD=str(record_path),
        FAKE_ROOT=str(root),
        QUEUE_MARKER="synthetic inherited environment",
        FACTORY_AUTHORS="owner",
    )

    def git(*args):
        return subprocess.check_output([REAL_GIT, *args], cwd=root, env=env, text=True, stderr=subprocess.PIPE).strip()

    git("init", "-b", "main")
    git("config", "user.name", "Queue Test")
    git("config", "user.email", "queue@example.invalid")
    (root / "scripts").mkdir()
    shutil.copyfile(ROOT / "scripts/autoqueue.py", root / "scripts/autoqueue.py")
    (root / ".gitignore").write_text(".autoqueue/\n.venv/\n")
    git("add", ".")
    git("commit", "-m", "origin base")
    origin = tmp_path / "origin.git"
    git("init", "--bare", str(origin))
    git("remote", "add", "origin", str(origin))
    git("push", "-u", "origin", "main")
    base = git("rev-parse", "HEAD")
    (root / "local-only").write_text("must not reach the worker")
    git("add", ".")
    git("commit", "-m", "local only")
    for name in ("gh", "uv", "bun", "just", "git", "node", "pi"):
        shim = bin_dir / name
        shim.write_text(f"#!{sys.executable}\n" + SHIM)
        shim.chmod(0o700)
    config = dict(issues=[issue(13)])

    def run(*args):
        config_path.write_text(json.dumps(config))
        return subprocess.run(
            [sys.executable, str(root / "scripts/autoqueue.py"), *args],
            cwd=tmp_path,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )

    def calls(name=None):
        data = [json.loads(line) for line in record_path.read_text().splitlines()] if record_path.exists() else []
        return [c for c in data if name is None or c["name"] == name]

    return SimpleNamespace(
        root=root,
        env=env,
        config=config,
        run=run,
        calls=calls,
        git=git,
        base=base,
        bin=bin_dir,
        tree=root / ".autoqueue/worktrees/issue-13",
        records=record_path,
    )


def gh_mutations(h):
    return [c["args"] for c in h.calls("gh") if c["args"][1] in {"edit", "comment"}]


def comments(h):
    return [args[-1] for args in gh_mutations(h) if args[1] == "comment"]


def test_dry_run_sorted_fetch_only(harness):
    h = harness
    h.config["issues"] = [issue(20), issue(13), issue(2)]
    before = h.git("show-ref")
    result = h.run("--dry-run", "--max", "2")
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == ["would pick #2: Issue 2", "would pick #13: Issue 13"]
    assert "skip #20: deferred by --max" in result.stderr
    assert gh_mutations(h) == [] and h.calls("bun") == [] and h.calls("just") == []
    assert h.calls("git")[0]["args"] == ["fetch", "origin"]
    assert h.git("show-ref") == before
    assert not (h.root / ".autoqueue/worktrees").exists()
    assert not (h.root / ".autoqueue/logs").exists()
    assert (h.root / ".autoqueue/lock").read_text() == ""
    for call in h.calls("gh"):
        assert call["args"][-2:] == ["--limit", "10000"]


def test_skip_priority_and_closing_keywords(harness):
    h = harness
    h.config["issues"] = [issue(n, assigned=n == 1) for n in range(1, 9)]
    h.config["prs"] = [dict(number=99, body="Closes #1; FiXeS\n#2; Resolves #3; discloses #4; #5; Closes #60")]
    leftover = h.tree.with_name("issue-7")
    leftover.mkdir(parents=True)
    (leftover / "keep").write_text("preserve")
    registered = h.tree.with_name("issue-8")
    h.git("worktree", "add", "-b", "old", str(registered), "origin/main")
    shutil.rmtree(registered)
    result = h.run("--dry-run", "--max", "10")
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == [f"would pick #{n}: Issue {n}" for n in (4, 5, 6)]
    skips = [line for line in result.stderr.splitlines() if line.startswith("skip")]
    assert len(skips) == 5
    assert "#1: already assigned" in skips[0]
    assert all("open PR" in line for line in skips[1:3])
    assert all("leftover worktree" in line for line in skips[3:])
    assert (leftover / "keep").read_text() == "preserve"
    assert str(registered) in h.git("worktree", "list", "--porcelain")
    assert gh_mutations(h) == []


@pytest.mark.parametrize("failed", [False, True])
def test_claim_origin_base_success_cleanup_and_inherited_environment(harness, failed):
    h = harness
    h.config["issues"] = [issue(13, failed=failed)]
    result = h.run()
    assert result.returncode == 0, result.stderr
    expected = [
        "issue",
        "edit",
        "13",
        "--add-label",
        "factory:running",
        "--remove-label",
        "factory:queued",
        "--add-assignee",
        "@me",
    ]
    if failed:
        expected += ["--remove-label", "factory:needs-human"]
    assert gh_mutations(h) == [
        expected,
        ["issue", "edit", "13", "--remove-label", "factory:running", "--add-label", "factory:pr-open"],
    ]
    claim = next(c for c in h.calls("gh") if c["args"] == expected)
    assert claim["worktrees"] == []
    factory = [c for c in h.calls() if c["name"] in {"bun", "just"}]
    assert [(c["name"], c["args"]) for c in factory] == [
        ("bun", ["install", "--frozen-lockfile"]),
        ("just", ["issue", "13"]),
    ]
    assert all(c["cwd"] == str(h.tree) and c["marker"] == "synthetic inherited environment" for c in factory)
    assert factory[1]["head"] == h.base and factory[1]["branch"] == "factory/issue-13"
    assert not factory[1]["local_only"]
    assert not h.tree.exists() and "factory/issue-13" not in h.git("branch", "--list")
    assert str(h.tree) not in h.git("worktree", "list", "--porcelain")
    logs = list((h.root / ".autoqueue/logs").glob("issue-13-*.log"))
    assert len(logs) == 1 and "error-looking text" in logs[0].read_text()
    assert "#13: OK" in result.stdout and comments(h) == []


@pytest.mark.parametrize("code", [1, 2, 17])
def test_failures_preserve_recovery_and_comment_once(harness, code):
    h = harness
    h.config["codes"] = {"13": code}
    result = h.run()
    assert result.returncode == 1
    assert (h.tree / "recovery.txt").read_text() == "uncommitted recovery"
    assert "factory/issue-13" in h.git("branch", "--list")
    assert gh_mutations(h)[1] == [
        "issue",
        "edit",
        "13",
        "--remove-label",
        "factory:running",
        "--add-label",
        "factory:needs-human",
        "--remove-assignee",
        "@me",
    ]
    assert len(comments(h)) == 1
    comment = comments(h)[0]
    assert str(h.tree) in comment and "factory:queued" in comment and "local branch" in comment
    assert "recovery command" in comment
    assert ("Last log lines" in comment) == (code != 1)
    if code != 1:
        assert "output-10" not in comment and "output-11" in comment and "output-29" in comment
        assert f"just issue 13 exited {code}" in comment
        assert "````text" in comment  # Embedded triple backticks cannot close the fence.
    # Canned ready label simulates a human re-adding it without removing recovery state.
    count = len(h.calls("just"))
    again = h.run()
    assert again.returncode == 0 and "leftover worktree" in again.stderr
    assert len(h.calls("just")) == count and len(comments(h)) == 1


def test_claim_failure_never_starts_or_comments(harness):
    h = harness
    h.config["reject"] = [["gh", "issue", "edit", "13"]]
    result = h.run()
    assert result.returncode == 1 and "FAILED claim" in result.stdout
    assert not h.tree.exists() and not (h.root / ".autoqueue/logs").exists()
    assert not h.calls("bun") and not h.calls("just") and not comments(h)


@pytest.mark.parametrize("stage", ["git", "bun", "spawn", "log"])
def test_setup_failures_include_tail_and_never_run_factory(harness, stage):
    h = harness
    if stage == "git":
        h.git("branch", "factory/issue-13")
    elif stage == "bun":
        h.config["bun_code"] = 9
    elif stage == "spawn":
        (h.bin / "bun").write_text("#!/no-such-interpreter\n")
    else:
        (h.root / ".autoqueue").mkdir()
        (h.root / ".autoqueue/logs").write_text("not a directory")
    result = h.run()
    assert result.returncode == 1 and h.calls("just") == []
    assert len(comments(h)) == 1 and "Last log lines" in comments(h)[0]
    assert str(h.tree) in comments(h)[0]
    assert "factory:needs-human" in gh_mutations(h)[1]
    if stage in {"bun", "spawn"}:
        assert h.tree.exists()


@pytest.mark.parametrize("failure", ["fetch", "prs", "invalid", "shape", "ceiling"])
def test_discovery_fails_closed_and_unlocks(harness, failure):
    h = harness
    if failure in {"fetch", "prs"}:
        h.config["reject"] = [["git", "fetch"] if failure == "fetch" else ["gh", "pr", "list"]]
    elif failure == "invalid":
        h.config["raw_prs"] = "not JSON"
    elif failure == "shape":
        h.config["raw_issues"] = '[{"number": 13}]'
    else:
        h.config["prs"] = [dict(number=n, body="") for n in range(10000)]
    result = h.run()
    assert result.returncode == 1 and "Traceback" not in result.stderr
    assert gh_mutations(h) == [] and not h.calls("just")
    assert (h.root / ".autoqueue/lock").read_text() == ""
    h.config.clear()
    h.config["issues"] = []
    assert h.run().returncode == 0


@pytest.mark.parametrize("failure", ["labels", "cleanup", "branch", "failure-labels", "comment"])
def test_finalization_failures_are_visible(harness, failure):
    h = harness
    prefixes = {
        "labels": ["gh", "issue", "edit", "13", "--remove-label"],
        "cleanup": ["git", "worktree", "remove"],
        "branch": ["git", "branch", "-D"],
        "failure-labels": ["gh", "issue", "edit", "13", "--remove-label"],
        "comment": ["gh", "issue", "comment"],
    }
    h.config["reject"] = [prefixes[failure]]
    if failure in {"failure-labels", "comment"}:
        h.config["codes"] = {"13": 1}
    result = h.run()
    assert result.returncode == 1 and "finalization" in result.stdout and "synthetic refusal" in result.stderr
    if failure in {"labels", "cleanup"}:
        assert h.tree.exists() and not comments(h)
        assert "factory succeeded" in result.stdout
    if failure in {"failure-labels", "comment"}:
        assert len(comments(h)) == 1  # Comment attempted independently of label update.


@pytest.mark.parametrize("maximum,expected", [(None, [2]), ("2", [2, 13]), ("10", [2, 13, 20])])
def test_max_numeric_order_and_sequential_batch(harness, maximum, expected):
    h = harness
    h.config.update(issues=[issue(20), issue(13), issue(2)], codes={"13": 1})
    result = h.run(*(["--max", maximum] if maximum else []))
    assert result.returncode == int(13 in expected)
    assert [int(c["args"][-1]) for c in h.calls("just")] == expected
    stages = [c["name"] for c in h.calls() if c["name"] in {"just", "bun"}]
    assert stages == ["bun", "just"] * len(expected)
    summaries = [line for line in result.stdout.splitlines() if line.startswith("#")]
    assert len(summaries) == len(expected)


def test_empty_and_invalid_args(harness):
    h = harness
    for args in [("--max", "0"), ("--max", "-1"), ("--max", "no"), ("cron", "61"), ("cron", "0")]:
        assert h.run(*args).returncode != 0
        assert not (h.root / ".autoqueue").exists() and h.calls() == []
    h.config["issues"] = []
    assert h.run().returncode == 0 and gh_mutations(h) == []


def test_live_nonholding_pid_is_reclaimed(harness):
    h = harness
    lock = h.root / ".autoqueue/lock"
    lock.parent.mkdir()
    value = str(os.getpid())
    lock.write_text(value)

    result = h.run("--dry-run")

    assert result.returncode == 0, result.stderr
    assert "would pick #13" in result.stdout
    assert "held by pid" not in result.stdout
    assert [call["args"][:2] for call in h.calls("gh")] == [["issue", "list"], ["pr", "list"]]
    assert gh_mutations(h) == []
    for call in h.calls("gh"):
        assert call["lock"] == str(call["parent_pid"])
        assert call["lock"] != value
    assert result.stderr.splitlines() == [f"autoqueue: taking over stale lock record {value!r}"]
    assert lock.read_text() == ""


def test_flock_held_by_child_skips_pass(harness):
    h = harness
    lock = h.root / ".autoqueue/lock"
    lock.parent.mkdir()
    child = subprocess.Popen(
        [
            sys.executable,
            "-c",
            """
import fcntl, os, sys
with open(sys.argv[1], "w") as lock:
    fcntl.flock(lock, fcntl.LOCK_EX)
    lock.write(str(os.getpid()))
    lock.flush()
    print("ready", flush=True)
    sys.stdin.read()
""",
            str(lock),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        text=True,
    )
    try:
        assert select.select([child.stdout], [], [], 10)[0], "lock holder did not signal readiness"
        assert child.stdout.readline().strip() == "ready"
        result = h.run("--dry-run")
        assert result.returncode == 0, result.stderr
        assert result.stdout.splitlines() == [f"autoqueue lock held by pid {child.pid}"]
        assert result.stderr == "" and h.calls() == []
        assert lock.read_text() == str(child.pid)
    finally:
        try:
            child.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            child.kill()
            child.communicate(timeout=10)
    assert child.returncode == 0
    result = h.run("--dry-run")
    assert result.returncode == 0, result.stderr
    assert "would pick #13" in result.stdout and h.calls("gh")
    assert result.stderr.splitlines() == [f"autoqueue: taking over stale lock record {str(child.pid)!r}"]
    assert lock.read_text() == ""


@pytest.mark.parametrize("holder", ["dead", "empty", "malformed"])
def test_pid_lock(harness, holder):
    h = harness
    lock = h.root / ".autoqueue/lock"
    lock.parent.mkdir()
    dead = subprocess.Popen([sys.executable, "-c", "pass"])
    dead.wait(timeout=10)
    value = {"dead": str(dead.pid), "empty": "", "malformed": "garbage"}[holder]
    lock.write_text(value)
    result = h.run("--dry-run")
    assert result.returncode == 0, result.stderr
    assert "would pick #13" in result.stdout
    assert h.calls()[0]["lock"].isdigit() and h.calls()[0]["lock"] != value
    assert lock.read_text() == ""
    assert result.stderr.splitlines() == ([f"autoqueue: taking over stale lock record {value!r}"] if value else [])


@pytest.mark.parametrize("minutes,schedule", [(None, "*/30"), ("7", "*/7"), ("60", "0")])
def test_cron_absolute_quoted_print_only_and_payload(harness, minutes, schedule):
    h = harness
    # Resolve every required executable from its own directory; retain symlink spelling.
    dirs = []
    for name in ("just", "uv", "bun", "gh", "git", "node", "pi"):
        directory = h.bin / f"{name}-dir"
        directory.mkdir()
        (directory / name).symlink_to(h.bin / name)
        dirs.append(str(directory))
    h.env["PATH"] = os.pathsep.join(dirs)
    result = h.run("cron", *([minutes] if minutes else []))
    assert result.returncode == 0, result.stderr
    assert not (h.root / ".autoqueue").exists() and h.calls() == []
    warning, line = result.stdout.splitlines()
    assert "GH_TOKEN in .env" in warning and "keyring" in warning
    assert line.startswith(f"{schedule} * * * * ")
    assert "\\%" in line and "< /dev/null" in line
    payload = line.split(" ", 5)[5].replace(r"\%", "%")
    # sh is invoked by the test, not cron generation. Only fake just is executed.
    result = subprocess.run(
        ["sh", "-c", payload],
        env={**h.env, "PATH": os.environ["PATH"]},
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, result.stderr
    assert [(c["name"], c["args"], c["cwd"]) for c in h.calls()] == [("just", ["autoqueue"], str(h.root))]
    assert (h.root / ".autoqueue/logs/cron.log").read_text() == "cron fake just\n"
    for directory in dirs:
        # shlex quoting can divide an apostrophe, so check via shell parsing below.
        rendered_path = next(token.removeprefix("PATH=") for token in shlex.split(payload) if token.startswith("PATH="))
        assert directory in rendered_path.split(os.pathsep)
    assert str(h.bin / "just-dir/just") in shlex.split(payload)


def test_cron_missing_executable_runs_nothing(harness):
    h = harness
    h.env["PATH"] = str(h.bin)
    (h.bin / "pi").unlink()
    result = h.run("cron")
    assert result.returncode == 1 and "'pi' not found" in result.stderr
    assert h.calls() == [] and not (h.root / ".autoqueue").exists()


@pytest.mark.skipif(not REAL_JUST, reason="just required for recipe wiring")
def test_real_just_recipes_pass_arguments_to_uv(harness):
    h = harness
    h.run("cron")  # Write shim config without executing tools.
    for args, expected in [
        (
            ["autoqueue", "--max", "2", "--dry-run"],
            ["run", "--no-project", "python", "scripts/autoqueue.py", "--max", "2", "--dry-run"],
        ),
        (["autoqueue-cron"], ["run", "--no-project", "python", "scripts/autoqueue.py", "cron", "30"]),
        (["autoqueue-cron", "15"], ["run", "--no-project", "python", "scripts/autoqueue.py", "cron", "15"]),
    ]:
        result = subprocess.run(
            [REAL_JUST, "--no-dotenv", "--justfile", str(ROOT / "justfile"), *args],
            cwd=h.root,
            env=h.env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        assert result.returncode == 0, result.stderr
        assert h.calls("uv")[-1]["args"] == expected
    assert not h.calls("gh") and not h.calls("just")


def test_only_allowed_authors_feed_the_factory(harness):
    h = harness
    h.config["issues"] = [issue(2, author="stranger"), issue(13)]
    result = h.run("--dry-run", "--max", "5")
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == ["would pick #13: Issue 13"]
    assert "skip #2: opened by stranger, not an allowed author" in result.stderr


def test_allowed_author_defaults_to_the_gh_user(harness):
    h = harness
    del h.env["FACTORY_AUTHORS"]
    h.config.update(issues=[issue(2, author="someone"), issue(13, author="me")], gh_user="me")
    result = h.run("--dry-run", "--max", "5")
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == ["would pick #13: Issue 13"]
    assert ["api", "user", "--jq", ".login"] in [c["args"] for c in h.calls("gh")]


# ---------- feedback lane: PRs labelled factory:revise ----------


def revise_pr(number=5, branch="factory/issue-1"):
    return dict(number=number, title=f"PR {number}", headRefName=branch)


@pytest.fixture
def pr_branch(harness):
    """origin has the factory branch for issue 1, the local clone does not (autoqueue deleted it after the PR)."""
    h = harness
    h.git("branch", "factory/issue-1", h.base)
    h.git("push", "origin", "factory/issue-1")
    h.git("branch", "-D", "factory/issue-1")
    return h.git("rev-parse", "origin/factory/issue-1")


def pr_mutations(h):
    return [c["args"] for c in h.calls("gh") if c["args"][:2] in (["pr", "edit"], ["pr", "comment"], ["issue", "edit"])]


def test_feedback_dry_run_lists_factory_prs_only(harness):
    h = harness
    h.config["revise_prs"] = [revise_pr(9, "someone/else"), revise_pr(5)]
    result = h.run("feedback", "--dry-run", "--max", "5")
    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == ["would revise PR #5: PR 5"]
    assert "skip PR #9: branch someone/else is not a factory branch" in result.stderr
    assert pr_mutations(h) == [] and h.calls("just") == []


def test_feedback_success_claims_revises_in_the_prs_branch_and_cleans_up(harness, pr_branch):
    h = harness
    h.config["revise_prs"] = [revise_pr()]
    result = h.run("feedback")
    assert result.returncode == 0, result.stderr
    assert pr_mutations(h) == [
        ["pr", "edit", "5", "--remove-label", "factory:revise"],
        ["issue", "edit", "1", "--add-label", "factory:revising", "--remove-label", "factory:pr-open"],
        ["issue", "edit", "1", "--remove-label", "factory:revising", "--add-label", "factory:pr-open"],
    ]
    just = [(c["args"], c["cwd"]) for c in h.calls("just")]
    tree = str(h.root / ".autoqueue/worktrees/pr-5")
    assert just == [(["pr-feedback", "5", "--check"], str(h.root)), (["pr-feedback", "5"], tree)]
    work = h.calls("just")[-1]
    assert work["branch"] == "factory/issue-1" and work["head"] == pr_branch
    assert not (h.root / ".autoqueue/worktrees/pr-5").exists()
    assert "factory/issue-1" not in h.git("branch", "--list")
    assert "PR #5: OK" in result.stdout


def test_feedback_with_nothing_new_drops_the_label_and_says_so(harness, pr_branch):
    h = harness
    h.config.update(revise_prs=[revise_pr()], check_code=3)
    result = h.run("feedback")
    assert result.returncode == 0, result.stderr
    muts = pr_mutations(h)
    assert muts[0] == ["pr", "edit", "5", "--remove-label", "factory:revise"]
    assert muts[1][:3] == ["pr", "comment", "5"] and "<!-- factory -->" in muts[1][-1]
    assert len(muts) == 2 and [c["args"] for c in h.calls("just")] == [["pr-feedback", "5", "--check"]]
    assert not (h.root / ".autoqueue/worktrees").exists()


def test_feedback_failure_keeps_the_worktree_and_comments_on_the_pr(harness, pr_branch):
    h = harness
    h.config.update(revise_prs=[revise_pr()], codes={"5": 1})
    result = h.run("feedback")
    assert result.returncode == 1
    tree = h.root / ".autoqueue/worktrees/pr-5"
    assert (tree / "recovery.txt").exists() and "factory/issue-1" in h.git("branch", "--list")
    muts = pr_mutations(h)
    assert muts[2] == ["issue", "edit", "1", "--remove-label", "factory:revising", "--add-label", "factory:needs-human"]
    body = muts[3][-1]
    assert muts[3][:3] == ["pr", "comment", "5"]
    assert body.startswith("<!-- factory -->") and "factory:revise" in body and str(tree) in body
    again = h.run("feedback")
    assert again.returncode == 0 and "skip PR #5: leftover worktree" in again.stderr


def test_the_factory_marker_matches_the_feedback_adw():
    adw = (ROOT / "adws/adw_pr_feedback.py").read_text(encoding="utf-8")
    assert 'FACTORY_MARK = "<!-- factory -->"' in adw
