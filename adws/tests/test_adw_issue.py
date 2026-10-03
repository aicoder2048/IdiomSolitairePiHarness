"""adw_issue: a GitHub issue becomes an SSSF request by its label, and a PR when the chain lands.

Classification is code, not prompt: the label table decides which template the
chain reads, and an issue that is unlabelled or carries two kinds stops before a
single token is spent.
"""

from __future__ import annotations

import json
import os
import stat
import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import adw_issue  # noqa: E402

ISSUE = {
    "number": 7,
    "title": "justfile: give `just test` a description",
    "body": "## What\n\n`test:` has no comment line.\n",
    "url": "https://github.com/o/r/issues/7",
    "labels": [{"name": "chore"}],
    "comments": [{"author": {"login": "sean"}, "body": "Keep it one line."}],
}


# --- classify --------------------------------------------------------------------------------------


@pytest.mark.parametrize(
    "label, kind",
    [("bug", "bug"), ("enhancement", "feature"), ("chore", "chore"), ("documentation", "docs")],
)
def test_each_type_label_maps_to_its_kind(label, kind):
    assert adw_issue.classify([label, "help wanted"]) == kind


def test_unlabelled_issue_is_refused():
    with pytest.raises(adw_issue.IssueError, match="no type label"):
        adw_issue.classify(["help wanted"])


def test_two_type_labels_are_refused():
    with pytest.raises(adw_issue.IssueError, match="bug, enhancement"):
        adw_issue.classify(["bug", "enhancement"])


def test_kind_override_wins_over_labels():
    assert adw_issue.classify([], override="bug") == "bug"
    assert adw_issue.classify(["bug", "chore"], override="docs") == "docs"


def test_unknown_override_is_refused():
    with pytest.raises(adw_issue.IssueError, match="unknown kind"):
        adw_issue.classify(["bug"], override="refactor")


# --- the request file -------------------------------------------------------------------------------


def test_request_path_is_issue_number_and_title_slug():
    issue = adw_issue.Issue.from_gh(ISSUE)
    assert adw_issue.request_path(issue) == Path("requests/issue-7-justfile-give-just-test.md")


def test_request_path_without_ascii_words_falls_back_to_the_number():
    issue = adw_issue.Issue.from_gh({**ISSUE, "title": "持仓面板：显示希腊字母"})
    assert adw_issue.request_path(issue) == Path("requests/issue-7.md")


def test_render_fills_every_placeholder():
    issue = adw_issue.Issue.from_gh(ISSUE)
    text = adw_issue.render(issue, 'Fix #{{number}} "{{title}}" ({{url}})\n\n{{body}}\n\n{{comments}}\n')
    assert text.startswith('Fix #7 "justfile: give `just test` a description" (https://github.com/o/r/issues/7)')
    assert "`test:` has no comment line." in text
    assert "@sean: Keep it one line." in text
    assert "{{" not in text


def test_render_without_comments_says_so():
    issue = adw_issue.Issue.from_gh({**ISSUE, "comments": []})
    assert "(no comments)" in adw_issue.render(issue, "{{comments}}")


def test_every_kind_has_a_template_with_the_four_line_shape():
    for kind in adw_issue.KINDS:
        text = adw_issue.template(kind)
        for line in ("Where:", "Done means:", "Out of scope:"):
            assert line in text, f"{kind} template lacks '{line}'"
        assert "{{body}}" in text


# --- gh ---------------------------------------------------------------------------------------------


def fake_gh(bin_dir: Path, *, issue: dict | None = ISSUE, pr_url: str = "https://github.com/o/r/pull/9") -> Path:
    """A `gh` on PATH that answers `issue view` with `issue` (or fails when None) and records every call, one line each."""
    log = bin_dir / "gh.log"
    script = bin_dir / "gh"
    script.write_text(
        "#!/bin/sh\n"
        f"printf '%s' \"$*\" | tr '\\n' ' ' >> \"{log}\"; echo >> \"{log}\"\n"
        'case "$1 $2" in\n'
        + (
            f"  'issue view') cat <<'JSON'\n{json.dumps(issue)}\nJSON\n;;\n"
            if issue is not None
            else "  'issue view') echo 'GraphQL: Could not resolve to an Issue' >&2; exit 1 ;;\n"
        )
        + f"  'pr create') echo '{pr_url}' ;;\n"
        + "  'issue comment') echo 'https://github.com/o/r/issues/7#issuecomment-4242' ;;\n"
        "esac\n"
    )
    script.chmod(script.stat().st_mode | stat.S_IEXEC)
    return log


@pytest.fixture
def gh_path(tmp_path, monkeypatch):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    return bin_dir


def test_fetch_issue_parses_gh_json(gh_path):
    fake_gh(gh_path)
    issue = adw_issue.fetch_issue(7)
    assert (issue.number, issue.title, issue.labels) == (7, ISSUE["title"], ["chore"])
    assert issue.comments == [("sean", "Keep it one line.")]


def test_fetch_issue_reports_gh_failure(gh_path):
    fake_gh(gh_path, issue=None)
    with pytest.raises(adw_issue.IssueError, match="Could not resolve"):
        adw_issue.fetch_issue(7)


# --- main -------------------------------------------------------------------------------------------


@pytest.fixture
def repo(tmp_path, monkeypatch, gh_path):
    """A git repo on a feature branch with the issue templates in place, as cwd."""
    root = tmp_path / "repo"
    root.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "main"], cwd=root, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "--allow-empty", "-m", "root"],
        cwd=root,
        check=True,
    )
    subprocess.run(["git", "checkout", "-q", "-b", "office/test"], cwd=root, check=True)
    templates = root / "adws/adw_data/prompt_engineering/issue"
    templates.mkdir(parents=True)
    for kind in adw_issue.KINDS:
        (templates / f"{kind}.md").write_text(
            f"{kind} #{{{{number}}}}\nWhere:\nDone means:\nOut of scope:\n\n{{{{body}}}}\n"
        )
    # Committed, as they are in the real repo: an untracked file would count as a dirty tree.
    subprocess.run(["git", "add", "-A"], cwd=root, check=True)
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "templates"], cwd=root, check=True
    )
    monkeypatch.chdir(root)
    return root


def test_dry_run_writes_the_request_and_touches_nothing_else(repo, gh_path, monkeypatch, capsys):
    log = fake_gh(gh_path)
    monkeypatch.setattr(adw_issue, "run_chain", lambda *a, **k: pytest.fail("the chain must not run on --dry-run"))
    assert adw_issue.main(7, dry_run=True) == 0
    request = repo / "requests/issue-7-justfile-give-just-test.md"
    assert request.read_text().startswith("chore #7\n")
    assert str(request.relative_to(repo)) in capsys.readouterr().out
    assert log.read_text().splitlines() == ["issue view 7 --json number,title,body,url,labels,comments"]


def test_refuses_on_the_base_branch_before_calling_gh(repo, gh_path, capsys):
    log = fake_gh(gh_path)
    subprocess.run(["git", "checkout", "-q", "main"], cwd=repo, check=True)
    assert adw_issue.main(7, dry_run=True) == 2
    assert "on main" in capsys.readouterr().err
    assert not log.exists()


def test_refuses_a_dirty_tree(repo, gh_path, capsys):
    fake_gh(gh_path)
    (repo / "stray.txt").write_text("x")
    assert adw_issue.main(7, dry_run=True) == 2
    assert "uncommitted" in capsys.readouterr().err


def test_unlabelled_issue_exits_2_without_writing(repo, gh_path, capsys):
    fake_gh(gh_path, issue={**ISSUE, "labels": []})
    assert adw_issue.main(7, dry_run=True) == 2
    assert "no type label" in capsys.readouterr().err
    assert not (repo / "requests").exists()


def test_chain_failure_prints_the_recovery_command(repo, gh_path, monkeypatch, capsys):
    fake_gh(gh_path)
    monkeypatch.setattr(adw_issue, "run_chain", lambda *a, **k: 1)
    monkeypatch.setattr(adw_issue, "open_pr", lambda *a, **k: pytest.fail("no PR for a failed chain"))
    assert adw_issue.main(7, adw_id="cafe1234") == 1
    err = capsys.readouterr().err
    assert "adw_build_review.py --adw-id cafe1234" in err


def test_success_pushes_then_opens_a_pr_titled_after_the_issue(repo, gh_path, monkeypatch, capsys):
    log = fake_gh(gh_path)
    calls: list[list[str]] = []
    monkeypatch.setattr(adw_issue, "run_chain", lambda *a, **k: 0)
    monkeypatch.setattr(adw_issue, "git_push", lambda: calls.append(["push"]))
    assert adw_issue.main(7, adw_id="cafe1234") == 0
    pr = [line for line in log.read_text().splitlines() if line.startswith("pr create")]
    assert calls == [["push"]]
    assert len(pr) == 1
    assert "--title justfile: give `just test` a description" in pr[0]
    assert "Closes #7" in pr[0]
    assert "cafe1234" in pr[0]
    assert "https://github.com/o/r/pull/9" in capsys.readouterr().out


def test_no_pr_skips_push_and_pr(repo, gh_path, monkeypatch):
    log = fake_gh(gh_path)
    monkeypatch.setattr(adw_issue, "run_chain", lambda *a, **k: 0)
    monkeypatch.setattr(adw_issue, "git_push", lambda: pytest.fail("no push with --no-pr"))
    assert adw_issue.main(7, no_pr=True) == 0
    assert not any(line.startswith("pr create") for line in log.read_text().splitlines())


# --- the progress comment ---------------------------------------------------------------------------

from types import SimpleNamespace  # noqa: E402

from adw_modules.runner import Run  # noqa: E402


def phase(name: str, owner: str, status: str = "success", error: str | None = None) -> SimpleNamespace:
    return SimpleNamespace(params=SimpleNamespace(name=name, owner=owner), status=status, error=error)


def chain_with_phases(*phases):
    """A fake chain that ends the given phases, as the real one would through Run.listeners."""

    def run_chain(*a, **k):
        for p in phases:
            for listener in list(Run.listeners):
                listener(p)
        return 0

    return run_chain


def comments(log: Path) -> list[str]:
    """The progress comment's posts: created with `issue comment`, then edited by its id through `api`."""
    return [line for line in log.read_text().splitlines() if line.startswith(("issue comment", "api "))]


def test_progress_is_one_comment_edited_per_phase_and_closed_with_the_pr(repo, gh_path, monkeypatch):
    log = fake_gh(gh_path)
    monkeypatch.setattr(adw_issue, "run_chain", chain_with_phases(phase("plan", "planner"), phase("build", "builder")))
    monkeypatch.setattr(adw_issue, "git_push", lambda: None)
    assert adw_issue.main(7, adw_id="cafe1234") == 0
    posted = comments(log)
    assert posted[0].startswith("issue comment 7 --body ") and "--edit-last" not in posted[0]
    # Edited by the id the first post returned, never `--edit-last`: the runner posts as the
    # user, so "my last comment" could be one the user wrote on the issue mid-run.
    edit = "api -X PATCH repos/{owner}/{repo}/issues/comments/4242 -f body="
    assert all(p.startswith(edit) for p in posted[1:])
    assert not any("--edit-last" in p for p in posted)
    assert len(posted) == 1 + 2 + 1  # start, two phases, the PR
    assert "cafe1234" in posted[0] and "office/test" in posted[0]
    assert "✅ plan (planner)" in posted[-1] and "✅ build (builder)" in posted[-1]
    assert "https://github.com/o/r/pull/9" in posted[-1]
    assert Run.listeners == []


def test_a_failed_phase_and_chain_are_reported_on_the_issue(repo, gh_path, monkeypatch):
    log = fake_gh(gh_path)

    def run_chain(*a, **k):
        for listener in list(Run.listeners):
            listener(phase("build", "builder", "fail", "gate diff_matches_claims: src/x.py changed but not claimed"))
        return 1

    monkeypatch.setattr(adw_issue, "run_chain", run_chain)
    assert adw_issue.main(7, adw_id="cafe1234") == 1
    last = comments(log)[-1]
    assert "❌ build (builder): gate diff_matches_claims" in last
    assert "did not land" in last and "adw_build_review.py --adw-id cafe1234" in last


def test_no_comment_posts_nothing(repo, gh_path, monkeypatch):
    log = fake_gh(gh_path)
    monkeypatch.setattr(adw_issue, "run_chain", chain_with_phases(phase("plan", "planner")))
    monkeypatch.setattr(adw_issue, "git_push", lambda: None)
    assert adw_issue.main(7, adw_id="cafe1234", no_comment=True) == 0
    assert comments(log) == []


def test_a_broken_comment_channel_never_fails_the_run(repo, gh_path, monkeypatch):
    log = fake_gh(gh_path)
    gh = gh_path / "gh"
    gh.write_text(
        gh.read_text().replace(
            'case "$1 $2" in\n', "case \"$1 $2\" in\n  'issue comment') echo 'HTTP 502' >&2; exit 1 ;;\n"
        )
    )
    monkeypatch.setattr(adw_issue, "run_chain", chain_with_phases(phase("plan", "planner"), phase("build", "builder")))
    monkeypatch.setattr(adw_issue, "git_push", lambda: None)
    assert adw_issue.main(7, adw_id="cafe1234") == 0
    assert len(comments(log)) == 1  # the first failure silences the reporter
    assert any(line.startswith("pr create") for line in log.read_text().splitlines())


def test_no_comment_id_means_no_edits(repo, gh_path, monkeypatch):
    log = fake_gh(gh_path)
    gh = gh_path / "gh"
    gh.write_text(gh.read_text().replace("issues/7#issuecomment-4242", "issues/7"))
    monkeypatch.setattr(adw_issue, "run_chain", chain_with_phases(phase("plan", "planner")))
    monkeypatch.setattr(adw_issue, "git_push", lambda: None)
    assert adw_issue.main(7, adw_id="cafe1234") == 0
    assert [p.split(" ")[0:2] for p in comments(log)] == [["issue", "comment"]]
