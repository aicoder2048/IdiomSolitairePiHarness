#!/usr/bin/env -S uv run
# /// script
# dependencies = ["pydantic", "python-dotenv", "pyyaml", "rich"]
# ///
"""ADW PR Feedback — review comments on a factory PR, through build + test, back onto the PR.

Usage:
    uv run adws/adw_pr_feedback.py <pr-number> [--check] [--dry-run] [--no-push]
                                   [--config adws/adw_sssf_config/sssf.config.yaml] [--adw-id a1b2c3d4]

Phases: code(feedback: gh api -> every review, inline and conversation comment by an allowed
        author since the factory's last reply -> requests/pr-<N>-feedback-<k>.md)
        -> adw_build_test (builder -> code(test+lint) -> bounded fix loop)
        -> code(commit, git push, one PR comment that answers the reviewer)

The factory opens its PRs under the operator's own GitHub account, and GitHub does not let
anyone request changes on their own PR, so "Request changes" cannot be the trigger. The
human comments as usual and labels the PR `factory:revise`; scripts/autoqueue.py runs this
in a worktree of the PR's branch.

Every comment the factory posts carries FACTORY_MARK, so its own words are never read back
as feedback; the reply also carries HANDLED_MARK, and only feedback newer than the latest
reply counts. `--check` answers "is there anything to address?" with exit 0 (yes) or 3 (no)
and touches nothing, which is how the queue decides before it builds a worktree.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

from adw_modules import git_helper, utils

DEFAULT_CONFIG = "adws/adw_sssf_config/sssf.config.yaml"
TEMPLATE = Path("adws/adw_data/prompt_engineering/issue/feedback.md")
REQUESTS = Path("requests")
FACTORY_MARK = "<!-- factory -->"
HANDLED_MARK = "<!-- factory:feedback-handled -->"
NOTHING = 3  # --check / main: no unaddressed feedback


class FeedbackError(Exception):
    """A refusal before any work starts: the message says why."""


@dataclass(frozen=True)
class Point:
    author: str
    at: str  # ISO 8601, UTC — compares as text
    body: str
    where: str  # "review", "comment", or "path:line"


@dataclass(frozen=True)
class PullRequest:
    number: int
    title: str
    body: str
    url: str
    head: str


def gh_json(path: str, paginate: bool = False):
    argv = ["gh", "api", *(["--paginate", "--slurp"] if paginate else []), path]
    result = subprocess.run(argv, capture_output=True, text=True)
    if result.returncode != 0:
        raise FeedbackError(f"gh api {path} failed: {result.stderr.strip() or result.stdout.strip()}")
    data = json.loads(result.stdout)
    return [item for page in data for item in page] if paginate else data


def allowed_authors() -> set[str]:
    """Same rule as the queue: FACTORY_AUTHORS, else the gh user running it."""
    configured = {name.strip() for name in os.environ.get("FACTORY_AUTHORS", "").split(",") if name.strip()}
    if configured:
        return configured
    result = subprocess.run(["gh", "api", "user", "--jq", ".login"], capture_output=True, text=True)
    login = result.stdout.strip()
    if result.returncode != 0 or not login:
        raise FeedbackError(f"could not determine the allowed authors: {result.stderr.strip()}")
    return {login}


def fetch(number: int) -> tuple[PullRequest, list[dict], list[dict], list[dict]]:
    base = f"repos/{{owner}}/{{repo}}/pulls/{number}"
    pr = gh_json(base)
    return (
        PullRequest(
            number=int(pr["number"]),
            title=str(pr.get("title") or "").strip(),
            body=str(pr.get("body") or "").strip(),
            url=str(pr.get("html_url") or ""),
            head=str(pr["head"]["ref"]),
        ),
        gh_json(f"{base}/reviews", paginate=True),
        gh_json(f"{base}/comments", paginate=True),
        gh_json(f"repos/{{owner}}/{{repo}}/issues/{number}/comments", paginate=True),
    )


def collect(reviews: list[dict], inline: list[dict], conversation: list[dict], authors: set[str]) -> list[Point]:
    """Every point by an allowed author after the factory's latest reply, oldest first."""
    handled = [c["created_at"] for c in conversation if HANDLED_MARK in (c.get("body") or "")]
    cutoff = max(handled, default="")

    def by_human(item: dict, body: str) -> bool:
        return (item.get("user") or {}).get("login") in authors and bool(body) and FACTORY_MARK not in body

    points: list[Point] = []
    for review in reviews:
        body = (review.get("body") or "").strip()
        at = review.get("submitted_at") or ""
        if by_human(review, body) and at > cutoff:
            points.append(Point(review["user"]["login"], at, body, "review"))
    for comment in inline:
        body = (comment.get("body") or "").strip()
        if by_human(comment, body) and comment["created_at"] > cutoff:
            line = comment.get("line") or comment.get("original_line") or "?"
            points.append(Point(comment["user"]["login"], comment["created_at"], body, f"{comment['path']}:{line}"))
    for comment in conversation:
        body = (comment.get("body") or "").strip()
        if by_human(comment, body) and comment["created_at"] > cutoff:
            points.append(Point(comment["user"]["login"], comment["created_at"], body, "comment"))
    return sorted(points, key=lambda p: p.at)


def render(pr: PullRequest, points: list[Point], text: str) -> str:
    feedback = "\n\n".join(f"### {i}. @{p.author} · {p.where}\n\n{p.body}" for i, p in enumerate(points, 1))
    fields = {
        "number": str(pr.number),
        "title": pr.title,
        "url": pr.url,
        "body": pr.body or "(no description)",
        "comments": feedback,
    }
    for name, value in fields.items():
        text = text.replace("{{" + name + "}}", value)
    return text


def request_path(number: int) -> Path:
    """requests/pr-<N>-feedback-<k>.md, k counting this PR's earlier rounds."""
    k = len(list(REQUESTS.glob(f"pr-{number}-feedback-*.md"))) + 1
    return REQUESTS / f"pr-{number}-feedback-{k}.md"


def run_chain(prompt: str, config: str, adw_id: str) -> int:
    """Builder, then the suite with a bounded fix loop. It does not commit; this script does."""
    import adw_build_test  # the chain's own dependencies load only when a run actually starts

    return adw_build_test.main(prompt, config, adw_id)


def builder_report(config: str, adw_id: str) -> str:
    """The builder's summary from its envelope — where it answers the reviewer's questions."""
    from adw_modules import agents

    path = Path(agents.load_config(config).defaults.data_dir) / "sessions" / adw_id / "builder" / "envelope.json"
    try:
        return str(json.loads(path.read_text(encoding="utf-8")).get("summary") or "").strip()
    except (OSError, ValueError):
        return ""


def git_push() -> None:
    subprocess.run(["git", "push", "origin", "HEAD"], check=True)


def reply(pr: PullRequest, points: list[Point], sha: str, adw_id: str, report: str) -> None:
    stat = subprocess.run(["git", "diff", "--stat", "HEAD~1", "HEAD"], capture_output=True, text=True).stdout.strip()
    body = "\n".join(
        [
            FACTORY_MARK,
            HANDLED_MARK,
            f"🏭 SSSF run `{adw_id}` 处理了 {len(points)} 条意见，提交 {sha}。",
            "",
            "**Builder 的说明**",
            "",
            report or "（builder 没有留下说明）",
            "",
            "```text",
            stat or "(no diff)",
            "```",
            "",
            "需要再改：继续留言，然后重新打上 `factory:revise`。",
        ]
    )
    result = subprocess.run(["gh", "pr", "comment", str(pr.number), "--body", body], capture_output=True, text=True)
    if result.returncode != 0:
        raise FeedbackError(f"gh pr comment failed: {result.stderr.strip()}")


def _refuse(message: str) -> int:
    print(f"adw_pr_feedback: {message}", file=sys.stderr)
    return 2


def main(
    number: int,
    config: str = DEFAULT_CONFIG,
    adw_id: str | None = None,
    check: bool = False,
    dry_run: bool = False,
    no_push: bool = False,
) -> int:
    try:
        pr, reviews, inline, conversation = fetch(number)
        points = collect(reviews, inline, conversation, allowed_authors())
    except FeedbackError as e:
        return _refuse(str(e))
    if not points:
        print(f"PR #{number}: no feedback since the factory's last reply")
        return NOTHING
    print(f"PR #{number}: {len(points)} point(s) to address")
    if check:
        return 0

    branch = git_helper.current_branch()
    if branch != pr.head:
        return _refuse(f"on {branch}, but PR #{number} is {pr.head}: check out its branch first")
    if git_helper.is_dirty():
        return _refuse("the working tree has uncommitted changes; commit or stash them first")
    if not TEMPLATE.is_file():
        return _refuse(f"no template: expected {TEMPLATE}")

    text = render(pr, points, TEMPLATE.read_text(encoding="utf-8"))
    request = request_path(number)
    request.parent.mkdir(parents=True, exist_ok=True)
    request.write_text(text, encoding="utf-8")
    print(f"request written to {request}")
    if dry_run:
        return 0

    adw_id = adw_id or utils.new_id()
    try:
        rc = run_chain(text, config, adw_id)
    except Exception as e:  # the chain raises on a failed gate or an unavailable model
        print(f"adw_pr_feedback: the chain stopped: {e}", file=sys.stderr)
        rc = 1
    if rc != 0:
        print(
            f"adw_pr_feedback: SSSF run {adw_id} did not land; nothing committed. Inspect: just phases {adw_id}",
            file=sys.stderr,
        )
        return 1

    sha = git_helper.commit_all(
        f"sssf({adw_id}): address review feedback on #{number}\n\n{len(points)} point(s), {request}"
    )
    if no_push:
        return 0
    try:
        git_push()
        reply(pr, points, sha, adw_id, builder_report(config, adw_id))
    except (FeedbackError, subprocess.CalledProcessError) as e:
        print(f"adw_pr_feedback: committed {sha} on {branch} but did not deliver it: {e}", file=sys.stderr)
        return 1
    print(f"PR #{number}: pushed {sha} and replied")
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("number", type=int, help="the pull request number")
    parser.add_argument("--check", action="store_true", help="exit 0 if there is feedback to address, 3 if not")
    parser.add_argument("--dry-run", action="store_true", help="write the request file and stop")
    parser.add_argument("--no-push", action="store_true", help="commit but do not push or reply")
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--adw-id", default=None, help="pin the session id")
    args = parser.parse_args()
    sys.exit(
        main(
            args.number,
            config=args.config,
            adw_id=args.adw_id,
            check=args.check,
            dry_run=args.dry_run,
            no_push=args.no_push,
        )
    )
