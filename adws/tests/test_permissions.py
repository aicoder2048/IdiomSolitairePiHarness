"""Write permissions against the real roster: what each agent may change in the repo.

The prompts and extensions under adws/adw_data/ steer and constrain the agents,
so no agent may edit them — not through the session-runtime exemption, and not
through a broad glob like the documenter's `**/*.md`.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adw_modules import agents, permissions  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def cfg():
    return agents.load_config(str(ROOT / "adws/adw_sssf_config/sssf.config.yaml"))


def allowed(cfg, agent_name: str, path: str) -> bool:
    agent = next(a for a in cfg.agents if a.name == agent_name)
    return permissions.permitted(path, agent, cfg)


@pytest.mark.parametrize("agent", ["planner", "builder", "scout", "reviewer", "documenter"])
@pytest.mark.parametrize(
    "path",
    [
        "adws/adw_data/harness_engineering/dev_guard.ts",
        "adws/adw_data/prompt_engineering/builder/system.md",
        "adws/adw_data/prompt_engineering/documenter/user.md",
        "adws/adw_modules/gates.py",
        "adws/adw_sssf_config/sssf.config.yaml",
        "adws/adw_build.py",
    ],
)
def test_no_agent_may_edit_the_factory(cfg, agent, path):
    assert not allowed(cfg, agent, path)


@pytest.mark.parametrize("agent", ["planner", "builder", "scout", "reviewer", "documenter"])
def test_every_agent_may_write_its_session_runtime(cfg, agent):
    assert allowed(cfg, agent, "adws/adw_data/sessions/abcd1234/context_handoff/findings.md")


def test_documenter_still_writes_docs(cfg):
    assert allowed(cfg, "documenter", "README.md")
    assert allowed(cfg, "documenter", "app_docs/x_y.md")
    assert allowed(cfg, "documenter", "docs/specs/z.md")
    assert not allowed(cfg, "documenter", "src/engine/game.ts")


def test_builder_still_writes_the_codebase(cfg):
    assert allowed(cfg, "builder", "src/engine/game.ts")
    assert allowed(cfg, "builder", "src/extension/index.ts")
    assert allowed(cfg, "builder", "package.json")


def test_explicitly_named_directory_unlocks_a_protected_path(cfg):
    agent = next(a for a in cfg.agents if a.name == "builder").model_copy(
        update={"writes": ["adws/adw_data/prompt_engineering/"]}
    )
    assert permissions.permitted("adws/adw_data/prompt_engineering/builder/system.md", agent, cfg)
