"""A throwaway checkout of the commit a run started from.

Evidence about a change is often a comparison: this test failed before and
passes now. "Before" needs a tree of its own, so this checks the baseline out
as a detached git worktree and removes it again, whatever happens inside.

Two placements are deliberate. The tree lives OUTSIDE the repo, because a test
runner started in the repo (`bun test`) scans the whole directory and would
run the baseline's copy of every test as well. And it shares the repo's
`node_modules` through a symlink instead of a fresh install, which is cheap but
means a change that adds a dependency is judged with HEAD's dependencies; the
symlink is removed before the tree, so cleanup can never reach the original.
"""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

SHARED = ["node_modules"]


def _git(repo: Path, *args: str) -> None:
    result = subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {result.stderr.strip()}")


@contextmanager
def checkout(run, sha: str) -> Iterator[Path]:
    """Yield a detached worktree of `sha` outside the repo; remove it on the way out."""
    repo = Path(run.repo_root)
    parent = Path(tempfile.mkdtemp(prefix="sssf-baseline-"))
    tree = parent / "tree"
    try:
        _git(repo, "worktree", "add", "--detach", str(tree), sha)
        for name in SHARED:
            if (repo / name).is_dir():
                (tree / name).symlink_to(repo / name, target_is_directory=True)
        yield tree
    finally:
        for name in SHARED:
            if (tree / name).is_symlink():
                (tree / name).unlink()
        subprocess.run(["git", "worktree", "remove", "--force", str(tree)], cwd=repo, capture_output=True)
        subprocess.run(["git", "worktree", "prune"], cwd=repo, capture_output=True)
        shutil.rmtree(parent, ignore_errors=True)
