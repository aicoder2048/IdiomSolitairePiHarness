/**
 * dev_guard — the harness for SSSF development agents in this repo.
 *
 * SSSF launches pi with --no-extensions, so the game extension (src/extension)
 * never loads into planner/builder/reviewer. Agents may edit the game freely;
 * what they must never touch is narrower:
 *
 *   1. secrets      — .env / .env.<name> (the .example/.sample templates are fine),
 *                     and the operator's credentials outside the repo: pi's
 *                     auth.json (subscription tokens), gh's config, ssh keys
 *   2. GitHub and git history — `gh`, and git commands that move refs or
 *                     rewrite the tree (commit, push, checkout, reset …).
 *                     Code owns commits, pushes and PRs (adw_issue, autoqueue);
 *                     an agent proposes, code disposes.
 *
 * Read-only git (status, diff, log, show) stays available for orientation.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import * as path from "node:path";

// A path token starts at the beginning, after whitespace/quote/=/:/redirect, or after "./".
const START = String.raw`(?:^|[\s'"=:<>(])(?:\./)?`;
const SECRET = new RegExp(`${START}\\.env(?!\\.(?:example|sample)(?![\\w.-]))(?:\\.[\\w-]+)?(?![\\w.-])`);
const CREDENTIALS = /\.pi\/agent\/auth\.json|\.config\/gh(?:\/|\b)|\.ssh\//;
// A command word starts the line or follows a separator, so `--debug` or `echo gh` do not count.
const CMD = String.raw`(?:^|[;&|(\n]|\$\()\s*(?:\w+=\S*\s+)*`;
const GH = new RegExp(`${CMD}gh(?:\\s|$)`);
const GIT_WRITE = new RegExp(
  `${CMD}git\\s+(?:-C\\s+\\S+\\s+)?(?:commit|push|pull|fetch|checkout|switch|reset|rebase|merge|cherry-pick|revert|stash|branch|tag|worktree|remote|config|clean|restore|am|apply)\\b`,
);

export function guardDevToolCall(toolName: string, input: Record<string, unknown> | undefined): string | null {
  const inp = input ?? {};
  if (toolName === "bash") {
    const cmd = String(inp.command ?? "");
    if (SECRET.test(cmd) || CREDENTIALS.test(cmd)) return "dev_guard: secrets and credentials are off-limits to development agents";
    if (GH.test(cmd)) return "dev_guard: GitHub is the factory's job, not an agent's — report what you need in your envelope";
    if (GIT_WRITE.test(cmd))
      return "dev_guard: git history is the factory's job (it commits, pushes and opens the PR) — read-only git (status, diff, log, show) is fine";
    return null;
  }
  if (toolName === "read" || toolName === "write" || toolName === "edit") {
    const raw = String(inp.path ?? inp.file_path ?? "");
    const rel = path.isAbsolute(raw) ? path.relative(process.cwd(), raw) : raw;
    if (SECRET.test(rel) || CREDENTIALS.test(raw)) return `dev_guard: ${raw} holds secrets`;
  }
  return null;
}

export default function (pi: ExtensionAPI) {
  pi.on("tool_call", async (event) => {
    const reason = guardDevToolCall(event.toolName, event.input as Record<string, unknown>);
    return reason ? { block: true, reason } : undefined;
  });
}
