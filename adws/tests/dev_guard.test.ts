import assert from "node:assert/strict";
import { homedir } from "node:os";
import { test } from "node:test";
import { guardDevToolCall } from "../adw_data/harness_engineering/dev_guard.ts";

const bash = (command: string) => guardDevToolCall("bash", { command });

test("bash: secrets and credentials are blocked, templates are not", () => {
  for (const cmd of ["cat .env", "source ./.env", "cp .env.local /tmp", `cat ${homedir()}/.pi/agent/auth.json`, "ls ~/.config/gh/", "cat ~/.ssh/id_ed25519"])
    assert.ok(bash(cmd), cmd);
  for (const cmd of ["cat .env.example", "cp .env.sample .env.example.bak", "grep -rn environment src"]) assert.equal(bash(cmd), null, cmd);
});

test("bash: gh and history-moving git are the factory's, read-only git is fine", () => {
  for (const cmd of ["gh pr create", "cd x && gh issue list", "git commit -m x", "git push", "git -C . checkout main", "FOO=1 git reset --hard", "true; git stash"])
    assert.ok(bash(cmd), cmd);
  for (const cmd of ["git status", "git diff --stat", "git log --oneline -5", "git show HEAD:src/engine/game.ts", "bun test", "just check", "echo gh", "grep -rn 'git push' docs"])
    assert.equal(bash(cmd), null, cmd);
});

test("file tools: secrets never, the codebase freely", () => {
  assert.ok(guardDevToolCall("read", { path: ".env" }));
  assert.ok(guardDevToolCall("write", { path: `${process.cwd()}/.env.deepseek` }));
  assert.ok(guardDevToolCall("read", { path: `${homedir()}/.pi/agent/auth.json` }));
  assert.equal(guardDevToolCall("read", { path: ".env.example" }), null);
  assert.equal(guardDevToolCall("edit", { path: "src/engine/game.ts" }), null);
  assert.equal(guardDevToolCall("write", { path: "src/extension/index.ts" }), null);
});
