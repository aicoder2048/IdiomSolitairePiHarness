"""Sequential, opt-in development issue runner (stdlib only; never installs cron).

Ported from OptionTradingPiHarness (its `auto:*` labels became `factory:*` here).
An issue enters the queue when a human labels it `factory:queued`; only issues
opened by an allowed author are taken (FACTORY_AUTHORS, comma-separated, or by
default the gh user running the queue), because an issue body becomes a prompt.

    factory:queued -> factory:running -> factory:pr-open      (just issue opened the PR)
                                      -> factory:needs-human  (worktree and branch kept; never retried)
"""

import argparse
import fcntl
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from collections import deque
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LIST_LIMIT = 10000
READY = "factory:queued"
RUNNING = "factory:running"
DONE = "factory:pr-open"
FAILED = "factory:needs-human"
BRANCH = "factory/issue-{number}"
CLOSING = re.compile(r"\b(?:close[sd]?|fix(?:es|ed)?|resolve[sd]?)\s+#(\d+)\b", re.IGNORECASE)


def diagnostic(message):
    print(message, file=sys.stderr)


@contextmanager
def pass_lock(root):
    """Keep the inode: unlinking a flock file would permit two simultaneous owners."""
    path = root / ".autoqueue/lock"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as lock:
        lock.seek(0)
        holder = lock.read().strip()
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            print(f"autoqueue lock held by pid {holder or 'unknown'}")
            yield False
            return
        # The flock is authoritative; recorded PIDs are diagnostic metadata only.
        if holder:
            diagnostic(f"autoqueue: taking over stale lock record {holder!r}")
        lock.seek(0)
        lock.truncate()
        lock.write(str(os.getpid()))
        lock.flush()
        try:
            yield True
        finally:
            lock.seek(0)
            lock.truncate()
            lock.flush()
            fcntl.flock(lock, fcntl.LOCK_UN)


def capture(root, args):
    result = subprocess.run(args, cwd=root, stdin=subprocess.DEVNULL, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError(f"{shlex.join(args)} exited {result.returncode}: {result.stderr.strip()}")
    return result.stdout


def mutation(root, args):
    try:
        capture(root, args)
        return True
    except (OSError, RuntimeError) as exc:
        diagnostic(str(exc))
        return False


def listing(root, args):
    data = json.loads(capture(root, [*args, "--limit", str(LIST_LIMIT)]))
    if not isinstance(data, list) or any(not isinstance(item, dict) for item in data):
        raise ValueError("GitHub list must be an array of objects")
    if len(data) >= LIST_LIMIT:
        raise ValueError(f"GitHub list reached --limit {LIST_LIMIT}; refusing incomplete discovery")
    return data


def allowed_authors(root):
    """Who may feed the factory: FACTORY_AUTHORS, else the gh user running the queue."""
    configured = os.environ.get("FACTORY_AUTHORS", "")
    authors = {name.strip() for name in configured.split(",") if name.strip()}
    if not authors:
        authors = {capture(root, ["gh", "api", "user", "--jq", ".login"]).strip()}
    if not all(authors):
        raise ValueError("could not determine the allowed issue authors")
    return authors


def candidates(root, maximum):
    authors = allowed_authors(root)
    issues = listing(
        root,
        ["gh", "issue", "list", "--state", "open", "--label", READY, "--json", "number,title,labels,assignees,author"],
    )
    prs = listing(root, ["gh", "pr", "list", "--state", "open", "--json", "number,body"])
    closed = {int(n) for pr in prs for n in CLOSING.findall(pr["body"] or "")}
    # Validate everything before claiming even the first issue.
    for issue in issues:
        if (
            type(issue["number"]) is not int
            or issue["number"] <= 0
            or not isinstance(issue["title"], str)
            or not isinstance(issue["assignees"], list)
            or not isinstance(issue["labels"], list)
            or any(not isinstance(label["name"], str) for label in issue["labels"])
            or not isinstance(issue.get("author"), dict)
            or not isinstance(issue["author"].get("login"), str)
        ):
            raise ValueError("Malformed GitHub issue")
    trees = capture(root, ["git", "worktree", "list", "--porcelain", "-z"])
    registered = {entry.removeprefix("worktree ") for entry in trees.split("\0") if entry.startswith("worktree ")}
    selected = []
    for issue in sorted(issues, key=lambda item: item["number"]):
        number = issue["number"]
        path = root / f".autoqueue/worktrees/issue-{number}"
        if issue["author"]["login"] not in authors:
            reason = f"opened by {issue['author']['login']}, not an allowed author"
        elif issue["assignees"]:
            reason = "already assigned"
        elif number in closed:
            reason = "closed by an open PR"
        elif os.path.lexists(path) or str(path) in registered:
            reason = f"leftover worktree {path}"
        elif len(selected) >= maximum:
            reason = "deferred by --max"
        else:
            selected.append(issue)
            continue
        diagnostic(f"skip #{number}: {reason}")
    return selected


def tee(args, cwd, log, tail):
    def emit(line):
        print(line, end="", flush=True)
        log.write(line)
        log.flush()
        tail.append(line)

    emit(f"$ {shlex.join(args)}\n")
    try:
        with subprocess.Popen(
            args,
            cwd=cwd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
        ) as child:
            for line in child.stdout:
                emit(line)
            code = child.wait()
            if code:
                emit(f"{shlex.join(args)} exited {code}\n")
            return code
    except OSError as exc:
        emit(f"Could not run {args[0]}: {exc}\n")
        return 127


def failure_comment(path, branch, stage, code, tail, include_tail):
    body = (
        f"Autoqueue failed at {stage} (exit {code}).\n\n"
        f"Preserved worktree (intended path; may not exist if setup failed): {path}\n\n"
        "Human recovery: open this worktree and follow the factory progress comment's recovery command. "
        "Or deliberately discard the failed worktree AND local branch "
        f"`{branch}`, then re-add `{READY}` to retry. "
        f"The runner never retries automatically; a leftover worktree will be skipped even with `{READY}`."
    )
    if include_tail:
        text = "".join(tail)
        fence = "`" * max(3, 1 + max((len(s) for s in re.findall(r"`+", text)), default=0))
        body += f"\n\nLast log lines:\n{fence}text\n{text}\n{fence}"
    return body


def process_issue(root, issue):
    number = str(issue["number"])
    edit = ["gh", "issue", "edit", number]
    claim = [*edit, "--add-label", RUNNING, "--remove-label", READY, "--add-assignee", "@me"]
    if any(label["name"] == FAILED for label in issue["labels"]):
        claim += ["--remove-label", FAILED]
    if not mutation(root, claim):
        print(f"#{number}: FAILED claim; no work started")
        return False

    relative = f".autoqueue/worktrees/issue-{number}"
    path = root / relative
    branch = BRANCH.format(number=number)
    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S.%fZ")
    log_path = root / f".autoqueue/logs/issue-{number}-{stamp}.log"
    tail = deque(maxlen=20)
    stage, code = "log setup", 127
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with log_path.open("w", encoding="utf-8") as log:
            for next_stage, args, cwd in [
                ("git worktree add", ["git", "worktree", "add", "-b", branch, relative, "origin/main"], root),
                ("bun install", ["bun", "install", "--frozen-lockfile"], path),
                ("just issue", ["just", "issue", number], path),
            ]:
                stage = next_stage
                code = tee(args, cwd, log, tail)
                if code:
                    break
    except OSError as exc:
        code = 127
        tail.append(f"{stage}: {exc}\n")
        diagnostic(tail[-1].strip())

    if code == 0:
        finalized = mutation(root, [*edit, "--remove-label", RUNNING, "--add-label", DONE])
        # Do not delete recovery state if the GitHub update failed.
        if finalized:
            finalized = mutation(root, ["git", "worktree", "remove", "--force", str(path)])
        if finalized:
            finalized = mutation(root, ["git", "branch", "-D", branch])
        outcome = "OK just issue exit 0" if finalized else "FAILED finalization (factory succeeded)"
        print(f"#{number}: {outcome}; log {log_path}; worktree {path}")
        return finalized

    labels_ok = mutation(root, [*edit, "--remove-label", RUNNING, "--add-label", FAILED, "--remove-assignee", "@me"])
    comment = failure_comment(path, branch, stage, code, tail, not (stage == "just issue" and code == 1))
    comment_ok = mutation(root, ["gh", "issue", "comment", number, "--body", comment])
    suffix = "" if labels_ok and comment_ok else "; finalization FAILED"
    print(f"#{number}: FAILED {stage} exit {code}; log {log_path}; kept worktree {path}{suffix}")
    return False


def render_cron(root, minutes):
    executables = {}
    for name in ("just", "uv", "bun", "gh", "git", "node", "pi"):
        found = shutil.which(name)
        if not found:
            raise ValueError(f"Executable '{name}' not found on PATH")
        executables[name] = os.path.abspath(found)  # Keep stable symlinks, not versioned targets.
    directories = [str(Path(p).parent) for p in executables.values()] + ["/usr/local/bin", "/usr/bin", "/bin"]
    path = os.pathsep.join(dict.fromkeys(directories))
    logs = root / ".autoqueue/logs"

    def q(value):
        return shlex.quote(str(value))

    command = (
        f"cd {q(root)} && mkdir -p {q(logs)} && PATH={q(path)} {q(executables['just'])} autoqueue"
        f" < /dev/null >> {q(logs / 'cron.log')} 2>&1"
    )
    schedule = "0 * * * *" if minutes == 60 else f"*/{minutes} * * * *"
    print("# Print only. gh authentication must be cron-reachable; macOS keyring may not be; GH_TOKEN in .env works.")
    print(schedule + " " + command.replace("%", r"\%"))


def positive(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    parser = argparse.ArgumentParser(description=__doc__)
    cron = bool(argv and argv[0] == "cron")
    if cron:
        parser.add_argument("minutes", nargs="?", type=positive, default=30)
        args = parser.parse_args(argv[1:])
        if args.minutes > 60:
            parser.error("minutes must be between 1 and 60")
    else:
        parser.add_argument("--max", type=positive, default=1)
        parser.add_argument("--dry-run", action="store_true")
        args = parser.parse_args(argv)
    try:
        if cron:
            render_cron(ROOT, args.minutes)
            return 0
        with pass_lock(ROOT) as acquired:
            if not acquired:
                return 0
            capture(ROOT, ["git", "fetch", "origin"])
            selected = candidates(ROOT, args.max)
            failed = False
            for issue in selected:
                if args.dry_run:
                    print(f"would pick #{issue['number']}: {issue['title']}")
                elif not process_issue(ROOT, issue):
                    failed = True
            return int(failed)
    except (OSError, RuntimeError, ValueError, KeyError, TypeError, OverflowError) as exc:
        diagnostic(f"autoqueue: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
