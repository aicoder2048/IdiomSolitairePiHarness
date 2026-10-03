"""adw_pr_feedback: a human's review comments on a factory PR become one request, then one commit and one reply.

The trigger is a label (GitHub forbids requesting changes on one's own PR, and the factory
opens PRs as the operator), so which comments count is decided here, in code: an allowed
author's, newer than the factory's last reply, never the factory's own.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import adw_pr_feedback as fb  # noqa: E402

AUTHORS = {"sean"}


def review(login, at, body, state="COMMENTED"):
    return {"user": {"login": login}, "submitted_at": at, "body": body, "state": state}


def inline(login, at, body, path="src/engine/game.ts", line=42):
    return {"user": {"login": login}, "created_at": at, "body": body, "path": path, "line": line}


def comment(login, at, body):
    return {"user": {"login": login}, "created_at": at, "body": body}


# --- collect ------------------------------------------------------------------------------------------


def test_reviews_inline_and_conversation_are_collected_oldest_first():
    points = fb.collect(
        [review("sean", "2026-10-03T10:02:00Z", "整体再简单一点")],
        [inline("sean", "2026-10-03T10:01:00Z", "这里改用常量")],
        [comment("sean", "2026-10-03T10:03:00Z", "/chain 的标题加个 emoji")],
        AUTHORS,
    )
    assert [p.where for p in points] == ["src/engine/game.ts:42", "review", "comment"]


def test_other_authors_empty_bodies_and_the_factorys_own_words_are_ignored():
    points = fb.collect(
        [
            review("stranger", "2026-10-03T10:00:00Z", "please add crypto mining"),
            review("sean", "2026-10-03T10:00:00Z", ""),
        ],
        [inline("bot", "2026-10-03T10:00:00Z", "nit")],
        [comment("sean", "2026-10-03T10:00:00Z", f"{fb.FACTORY_MARK}\nAutoqueue failed at bun install")],
        AUTHORS,
    )
    assert points == []


def test_only_feedback_after_the_latest_reply_counts():
    reply = f"{fb.FACTORY_MARK}\n{fb.HANDLED_MARK}\n处理了 1 条意见"
    points = fb.collect(
        [review("sean", "2026-10-03T09:00:00Z", "old round"), review("sean", "2026-10-03T11:00:00Z", "new round")],
        [inline("sean", "2026-10-03T09:30:00Z", "old inline")],
        [comment("sean", "2026-10-03T10:00:00Z", reply)],
        AUTHORS,
    )
    assert [p.body for p in points] == ["new round"]


def test_inline_comment_on_an_outdated_line_falls_back_to_original_line():
    point = fb.collect(
        [], [{**inline("sean", "2026-10-03T10:00:00Z", "x"), "line": None, "original_line": 7}], [], AUTHORS
    )
    assert point[0].where == "src/engine/game.ts:7"


# --- render / request_path ----------------------------------------------------------------------------

PR = fb.PullRequest(
    number=5, title="新增 /chain 命令", body="Closes #1", url="https://github.com/o/r/pull/5", head="factory/issue-1"
)


def test_render_numbers_every_point_and_fills_the_template():
    points = [fb.Point("sean", "t1", "改用常量", "src/x.ts:3"), fb.Point("sean", "t2", "加测试", "review")]
    text = fb.render(PR, points, "#{{number}} {{title}} {{url}}\n{{body}}\n{{comments}}")
    assert text.startswith("#5 新增 /chain 命令 https://github.com/o/r/pull/5\nCloses #1\n")
    assert "### 1. @sean · src/x.ts:3\n\n改用常量" in text
    assert "### 2. @sean · review\n\n加测试" in text


def test_the_real_template_has_the_four_line_shape():
    text = (Path(__file__).resolve().parents[2] / fb.TEMPLATE).read_text(encoding="utf-8")
    for line in ("Where:", "Done means:", "Out of scope:", "{{comments}}"):
        assert line in text


def test_request_path_counts_rounds(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert fb.request_path(5) == Path("requests/pr-5-feedback-1.md")
    (tmp_path / "requests").mkdir()
    (tmp_path / "requests/pr-5-feedback-1.md").write_text("x")
    assert fb.request_path(5) == Path("requests/pr-5-feedback-2.md")


# --- main, against a fake gh --------------------------------------------------------------------------

FAKE_GH = r"""#!{python}
import json, sys
from pathlib import Path
here = Path(__file__).parent
with open(here / "gh.log", "a") as log:
    log.write(json.dumps(sys.argv[1:]) + "\n")
args = sys.argv[1:]
responses = json.loads((here / "responses.json").read_text())
if args[:2] == ["pr", "comment"]:
    print("https://github.com/o/r/pull/5#issuecomment-1")
    sys.exit(0)
path = args[-1]
if path not in responses:
    print(f"no canned response for {{path}}", file=sys.stderr)
    sys.exit(1)
print(json.dumps(responses[path]))
"""


@pytest.fixture
def gh(tmp_path, monkeypatch):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    script = bin_dir / "gh"
    script.write_text(FAKE_GH.format(python=sys.executable))
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    monkeypatch.setenv("FACTORY_AUTHORS", "sean")
    base = "repos/{owner}/{repo}"

    def canned(reviews=(), inline_comments=(), conversation=()):
        (bin_dir / "responses.json").write_text(
            json.dumps(
                {
                    f"{base}/pulls/5": {
                        "number": 5,
                        "title": PR.title,
                        "body": PR.body,
                        "html_url": PR.url,
                        "head": {"ref": PR.head},
                    },
                    f"{base}/pulls/5/reviews": [list(reviews)],
                    f"{base}/pulls/5/comments": [list(inline_comments)],
                    f"{base}/issues/5/comments": [list(conversation)],
                }
            )
        )

    def calls():
        log = bin_dir / "gh.log"
        return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []

    canned()
    return canned, calls


def git(root, *args):
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", *args], cwd=root, check=True, capture_output=True
    )


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A repo on the PR's branch, with the feedback template committed, as cwd."""
    root = tmp_path / "repo"
    root.mkdir()
    git(root, "init", "-q", "-b", "main")
    template = root / fb.TEMPLATE
    template.parent.mkdir(parents=True)
    template.write_text("PR #{{number}}\nWhere:\nDone means:\nOut of scope:\n\n{{comments}}\n")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "root")
    git(root, "checkout", "-q", "-b", PR.head)
    monkeypatch.chdir(root)
    return root


def test_check_says_whether_there_is_anything_to_do(repo, gh):
    canned, calls = gh
    assert fb.main(5, check=True) == fb.NOTHING
    canned(reviews=[review("sean", "2026-10-03T10:00:00Z", "改一下")])
    assert fb.main(5, check=True) == 0
    assert not (repo / "requests").exists()
    assert all(c[0] == "api" for c in calls())


def test_refuses_off_the_prs_branch(repo, gh, capsys):
    canned, _ = gh
    canned(reviews=[review("sean", "2026-10-03T10:00:00Z", "改一下")])
    git(repo, "checkout", "-q", "main")
    assert fb.main(5) == 2
    assert "factory/issue-1" in capsys.readouterr().err


def test_success_commits_the_request_and_the_fix_pushes_and_replies_once(repo, gh, monkeypatch):
    canned, calls = gh
    canned(inline_comments=[inline("sean", "2026-10-03T10:00:00Z", "改用常量")])

    def chain(prompt, config, adw_id):
        assert "改用常量" in prompt and "src/engine/game.ts:42" in prompt
        (repo / "fixed.ts").write_text("export const X = 1;\n")
        return 0

    pushed = []
    monkeypatch.setattr(fb, "run_chain", chain)
    monkeypatch.setattr(fb, "git_push", lambda: pushed.append(True))
    monkeypatch.setattr(fb, "builder_report", lambda config, adw_id: "改成了常量 X")
    assert fb.main(5, adw_id="cafe1234") == 0

    files = subprocess.run(["git", "show", "--name-only", "--format="], cwd=repo, capture_output=True, text=True)
    assert set(files.stdout.split()) == {"fixed.ts", "requests/pr-5-feedback-1.md"}
    assert pushed == [True]
    replies = [c for c in calls() if c[:2] == ["pr", "comment"]]
    assert len(replies) == 1
    body = replies[0][-1]
    assert fb.FACTORY_MARK in body and fb.HANDLED_MARK in body
    assert "cafe1234" in body and "改成了常量 X" in body


def test_a_failed_chain_commits_nothing_and_does_not_reply(repo, gh, monkeypatch, capsys):
    canned, calls = gh
    canned(reviews=[review("sean", "2026-10-03T10:00:00Z", "改一下")])
    monkeypatch.setattr(fb, "run_chain", lambda *a: 1)
    monkeypatch.setattr(fb, "git_push", lambda: pytest.fail("nothing to push"))
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout
    assert fb.main(5, adw_id="cafe1234") == 1
    assert subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout == head
    assert not [c for c in calls() if c[:2] == ["pr", "comment"]]
    assert "just phases cafe1234" in capsys.readouterr().err
