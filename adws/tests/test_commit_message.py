"""The code commit is named by the pass that built the change, not the last repair.

Run 3a963635 committed a 13-file rename under the revise pass's message,
"Fix remaining engine CLI reference in environment example".
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adw_modules import git_helper  # noqa: E402
from adw_modules.data_types import BuildOutput  # noqa: E402


def build(message: str = "", summary: str = "did it") -> BuildOutput:
    return BuildOutput(status="success", summary=summary, commit_message=message)


def test_single_pass_uses_its_own_message():
    assert git_helper.build_commit_message([build("Rename the CLI")], "abcd1234") == "Rename the CLI"


def test_repairs_do_not_replace_the_subject():
    passes = [build("Rename the CLI"), build("Fix lint in cli.py"), build("Fix the .env.example reference")]
    message = git_helper.build_commit_message(passes, "abcd1234")
    subject, _, body = message.partition("\n\n")
    assert subject == "Rename the CLI"
    assert "- Fix lint in cli.py" in body
    assert "- Fix the .env.example reference" in body


def test_missing_messages_fall_back_to_summaries():
    passes = [build(summary="Renamed everything"), build(summary="Closed the review finding")]
    message = git_helper.build_commit_message(passes, "abcd1234")
    assert message.startswith("sssf(abcd1234): Renamed everything\n\n")
    assert "- Closed the review finding" in message
