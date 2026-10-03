#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pydantic", "python-dotenv", "pyyaml", "rich"]
# ///
"""ADW Issue — a GitHub issue, sorted by its label, through the simple SDLC and into a pull request.

Usage:
    uv run adws/adw_issue.py <number> [--kind bug|feature|chore|docs] [--no-pr] [--dry-run]
                             [--base main] [--config adws/adw_sssf_config/sssf.config.yaml] [--adw-id a1b2c3d4]

Phases: code(issue: gh issue view -> type label -> kind template -> requests/issue-<N>-<slug>.md)
        -> adw_simple_sdlc (planner -> builder -> tests -> reviewer -> documenter, three commits)
        -> code(pr: git push -u origin HEAD, gh pr create titled after the issue, "Closes #<N>")

The sorting is code, not a prompt. Exactly one of the repository's type labels
(bug, enhancement, chore, documentation) picks the template in
adws/adw_data/prompt_engineering/issue/, which gives the chain the constraints
that kind of work carries — a bug starts with a failing test, a chore changes no
behaviour. An issue with none or two of them stops here, before a token is spent,
unless --kind says which it is.

Two refusals come before GitHub is even asked: the current branch must not be the
base (the chain commits where it stands, and a PR needs a branch of its own), and
the tree must be clean (commit_all would sweep stray edits into the plan commit).
scripts/autoqueue.py runs this in a fresh worktree of origin/main, where both hold by construction.

The request file is written before the chain starts and is part of its first
commit, like every other file under requests/. A failed chain leaves the plan
committed and the code uncommitted, as adw_simple_sdlc does; the recovery command
is printed, and no PR is opened for it.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from adw_modules import git_helper, utils
from adw_modules.runner import Run

DEFAULT_CONFIG = "adws/adw_sssf_config/sssf.config.yaml"
TEMPLATES = Path("adws/adw_data/prompt_engineering/issue")
REQUESTS = Path("requests")

# The repository's type labels, and the kind of work each one means.
LABELS = {"bug": "bug", "enhancement": "feature", "chore": "chore", "documentation": "docs"}
KINDS = tuple(LABELS.values())

ISSUE_FIELDS = "number,title,body,url,labels,comments"


class IssueError(Exception):
    """A refusal before any work starts: the message says why."""


@dataclass(frozen=True)
class Issue:
    number: int
    title: str
    body: str
    url: str
    labels: list[str]
    comments: list[tuple[str, str]]  # (author login, body)

    @classmethod
    def from_gh(cls, data: dict) -> Issue:
        return cls(
            number=int(data["number"]),
            title=str(data.get("title") or "").strip(),
            body=str(data.get("body") or "").strip(),
            url=str(data.get("url") or ""),
            labels=[str(label["name"]) for label in data.get("labels") or []],
            comments=[
                (str((c.get("author") or {}).get("login") or "?"), str(c.get("body") or "").strip())
                for c in data.get("comments") or []
            ],
        )


def classify(labels: list[str], override: str | None = None) -> str:
    """The kind of work an issue is, from its one type label — or from --kind, which needs no label."""
    if override is not None:
        if override not in KINDS:
            raise IssueError(f"unknown kind {override!r}; one of {', '.join(KINDS)}")
        return override
    found = [label for label in labels if label in LABELS]
    if not found:
        raise IssueError(f"no type label: add exactly one of {', '.join(LABELS)}, or pass --kind")
    if len(found) > 1:
        raise IssueError(f"more than one type label ({', '.join(found)}): keep one, or pass --kind")
    return LABELS[found[0]]


def fetch_issue(number: int) -> Issue:
    result = subprocess.run(
        ["gh", "issue", "view", str(number), "--json", ISSUE_FIELDS], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise IssueError(f"gh issue view {number} failed: {result.stderr.strip() or result.stdout.strip()}")
    return Issue.from_gh(json.loads(result.stdout))


def template(kind: str) -> str:
    path = TEMPLATES / f"{kind}.md"
    if not path.is_file():
        raise IssueError(f"no template for kind {kind!r}: expected {path}")
    return path.read_text(encoding="utf-8")


def render(issue: Issue, text: str) -> str:
    comments = "\n\n".join(f"@{login}: {body}" for login, body in issue.comments) or "(no comments)"
    fields = {
        "number": str(issue.number),
        "title": issue.title,
        "url": issue.url,
        "body": issue.body or "(no description)",
        "comments": comments,
    }
    for name, value in fields.items():
        text = text.replace("{{" + name + "}}", value)
    return text


def request_path(issue: Issue) -> Path:
    """requests/issue-<N>-<first four ascii words of the title>.md; just the number when there are none."""
    words = re.findall(r"[a-z0-9]+", issue.title.lower())[:4]
    slug = "-".join(words)
    return REQUESTS / (f"issue-{issue.number}-{slug}.md" if slug else f"issue-{issue.number}.md")


def run_chain(prompt: str, config: str, adw_id: str) -> int:
    """The simple SDLC, in this process: it commits where it stands and returns its exit code."""
    import adw_simple_sdlc  # the chain's own dependencies load only when a run actually starts

    return adw_simple_sdlc.main(prompt, config, adw_id)


def git_push() -> None:
    subprocess.run(["git", "push", "-u", "origin", "HEAD"], check=True)


def open_pr(issue: Issue, kind: str, request: Path, adw_id: str) -> str:
    """A pull request titled after the issue; `Closes #N` links and closes it on merge. Returns its URL."""
    body = (
        f"Closes #{issue.number}\n\n"
        f"Built by SSSF run `{adw_id}` (adw_issue, kind: {kind}) from `{request}`. "
        f"Plan, code and write-up are its three commits."
    )
    result = subprocess.run(
        ["gh", "pr", "create", "--title", issue.title, "--body", body], capture_output=True, text=True
    )
    if result.returncode != 0:
        raise IssueError(f"gh pr create failed: {result.stderr.strip() or result.stdout.strip()}")
    return result.stdout.strip().splitlines()[-1]


class Progress:
    """One comment on the issue, edited as the chain goes: the phases so far, then the PR or the failure.

    The board shows an issue as In progress from the moment the worker is assigned; this is the only
    place that says which phase the factory is in. One comment, edited in place rather than one per
    phase, and edited by the id its first post returned: `gh issue comment --edit-last` edits the
    gh user's LAST comment, and the run posts as the person — a comment they write on the issue
    mid-run would be overwritten. Nothing here may fail the run: every gh error is printed and
    swallowed, and after one (or a post that returns no comment id) the reporter goes quiet.
    """

    MARK = {"success": "✅", "fail": "❌"}

    def __init__(self, issue: Issue, kind: str, adw_id: str, branch: str, request: Path):
        self.issue = issue
        self.head = f"🏭 SSSF run `{adw_id}` — {kind}, from `{request}`, on `{branch}`"
        self.phases: list[str] = []
        self.tail = "_running…_"
        self.quiet = False
        self.comment_id: str | None = None

    def render(self) -> str:
        return "\n".join([self.head, "", *self.phases, "", self.tail])

    def start(self) -> None:
        out = self._post(["gh", "issue", "comment", str(self.issue.number), "--body", self.render()])
        found = re.search(r"issuecomment-(\d+)", out or "")
        if found:
            self.comment_id = found.group(1)
        elif not self.quiet:
            self.quiet = True
            print("adw_issue: the progress comment's id was not returned, going quiet", file=sys.stderr)

    def phase(self, phase) -> None:
        mark = self.MARK.get(phase.status, "•")
        line = f"- {mark} {phase.params.name} ({phase.params.owner})"
        if phase.status == "fail" and phase.error:
            line += f": {phase.error.splitlines()[0][:200]}"
        self.phases.append(line)
        self._edit()

    def finish(self, tail: str) -> None:
        self.tail = tail
        self._edit()

    def _edit(self) -> None:
        if self.comment_id is None:
            return
        # {owner}/{repo} are filled in by gh from the current repository.
        path = f"repos/{{owner}}/{{repo}}/issues/comments/{self.comment_id}"
        self._post(["gh", "api", "-X", "PATCH", path, "-f", f"body={self.render()}"])

    def _post(self, argv: list[str]) -> str | None:
        if self.quiet:
            return None
        result = subprocess.run(argv, capture_output=True, text=True)
        if result.returncode != 0:
            self.quiet = True
            print(f"adw_issue: progress comment failed, going quiet: {result.stderr.strip()[:300]}", file=sys.stderr)
            return None
        return result.stdout


def _refuse(message: str) -> int:
    print(f"adw_issue: {message}", file=sys.stderr)
    return 2


def main(
    number: int,
    config: str = DEFAULT_CONFIG,
    adw_id: str | None = None,
    kind: str | None = None,
    no_pr: bool = False,
    dry_run: bool = False,
    no_comment: bool = False,
    base: str = "main",
) -> int:
    branch = git_helper.current_branch()
    if branch == base:
        return _refuse(
            f"refusing to run on {base}: the chain commits to the current branch and a PR needs its own — create a branch first"
        )
    if git_helper.is_dirty():
        return _refuse(
            "the working tree has uncommitted changes; commit or stash them first (the plan commit would sweep them in)"
        )

    try:
        issue = fetch_issue(number)
        work = classify(issue.labels, kind)
        text = render(issue, template(work))
    except IssueError as e:
        return _refuse(str(e))

    request = request_path(issue)
    request.parent.mkdir(parents=True, exist_ok=True)
    request.write_text(text, encoding="utf-8")
    print(f"issue #{issue.number} is a {work}: request written to {request}")
    if dry_run:
        return 0

    adw_id = adw_id or utils.new_id()
    progress = None if no_comment else Progress(issue, work, adw_id, branch, request)
    if progress:
        progress.start()
        Run.listeners.append(progress.phase)
    try:
        rc = run_chain(text, config, adw_id)
    except Exception as e:  # the chain raises on a failed gate or an unavailable model
        print(f"adw_issue: the chain stopped: {e}", file=sys.stderr)
        rc = 1
    finally:
        if progress and progress.phase in Run.listeners:
            Run.listeners.remove(progress.phase)
    if rc != 0:
        resume = f"uv run adws/adw_build_review.py --adw-id {adw_id} --config {config} {request}"
        print(
            f"adw_issue: SSSF run {adw_id} did not land; no PR opened. Inspect: just phases {adw_id}\n"
            f"  resume without re-planning: {resume}\n"
            f"  (that neither tests nor commits: run the suites, commit, then\n"
            f"   uv run adws/adw_document.py --adw-id {adw_id} --config {config} {request}, commit, push, gh pr create)",
            file=sys.stderr,
        )
        if progress:
            progress.finish(f"❌ The run did not land; no PR. Resume without re-planning: `{resume}`")
        return 1
    if no_pr:
        if progress:
            progress.finish("✅ The run landed on the branch; no PR asked for (`--no-pr`).")
        return 0

    try:
        git_push()
        url = open_pr(issue, work, request, adw_id)
    except (IssueError, subprocess.CalledProcessError) as e:
        print(f"adw_issue: the code landed on {branch} but the PR did not: {e}", file=sys.stderr)
        if progress:
            progress.finish(f"⚠️ The run landed on `{branch}` but the PR did not open: {str(e)[:300]}")
        return 1
    print(f"pull request: {url}")
    if progress:
        progress.finish(f"✅ Pull request: {url}")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("number", type=int, help="the GitHub issue number")
    parser.add_argument("--kind", choices=KINDS, default=None, help="override the label: what kind of work it is")
    parser.add_argument("--no-pr", action="store_true", help="stop after the chain: no push, no pull request")
    parser.add_argument("--dry-run", action="store_true", help="write the request file and stop")
    parser.add_argument("--no-comment", action="store_true", help="no progress comment on the issue")
    parser.add_argument("--base", default="main", help="the branch the PR merges into (never run on it)")
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--adw-id", default=None, help="pin the session id (printed on failure for recovery)")
    args = parser.parse_args()
    sys.exit(
        main(
            args.number,
            config=args.config,
            adw_id=args.adw_id,
            kind=args.kind,
            no_pr=args.no_pr,
            dry_run=args.dry_run,
            no_comment=args.no_comment,
            base=args.base,
        )
    )
