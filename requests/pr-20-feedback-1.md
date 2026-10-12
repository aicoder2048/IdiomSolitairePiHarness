Address review feedback on pull request #20: "TUI 截屏引擎：scripts/tui_capture.py" (https://github.com/aicoder2048/IdiomSolitairePiHarness/pull/20). The factory opened it; you are on its branch, and its earlier commits are the factory's own plan (under specs/), code and write-up. The feedback is quoted in full at the end of this request (agents cannot run `gh`; this copy is all there is).

This is a REVISION of work under review:
- Address every point below. Where a point is a question, or you think the change would be wrong, change nothing for it and answer it in your report's summary: the reply to the reviewer is built from that summary.
- Change only what the feedback asks for. Existing tests keep passing; feedback that changes behaviour comes with tests that describe it.
- An inline point names its file and line; read the code around it before editing.

Where: the files the feedback names; otherwise the module that owns the behaviour, found before editing. AGENTS.md rules apply.
Done means: every point below is either handled in code or answered in the report; `just test` passes.
Out of scope: anything the feedback does not ask for, including cleanups the reviewer did not mention.

## Pull request description

Closes #19

Built by SSSF run `2b935869` (adw_issue, kind: feature) from `requests/issue-19-tui-scripts-tui-capture.md`. Plan, code and write-up are its three commits.

# SSSF 证据包 · run `2b935869`

## 1. 结论

✅ 已接受

- workflow：`adw_simple_sdlc`
- kind：feature

## 2. 版本

- run：`2b935869`
- branch：`factory/issue-19`
- 基线：`3fd998d`
- HEAD：`2fb79ae`

## 3. 改了什么

```text
 AGENTS.md                                    |   3 +-
 README.md                                    |  23 +-
 adws/tests/test_quality_gate.py              |   2 +-
 app_docs/2b935869_tui-capture-engine.md      |  22 ++
 justfile                                     |   9 +
 requests/issue-19-tui-scripts-tui-capture.md |  92 ++++++
 scripts/tui_capture.py                       | 277 ++++++++++++++++++
 scripts/tui_scenes.example.json              |  15 +
 specs/2b935869_tui-capture-engine.md         | 107 +++++++
 tests/test_tui_capture.py                    | 407 +++++++++++++++++++++++++++
 10 files changed, 954 insertions(+), 3 deletions(-)
```

## 4. 怎么验证的

| 检查 | 命令 | 退出码 | 耗时 | 摘要 |
| :-- | :-- | :-: | --: | :-- |
| ✅ test | `just test` | 0 | 66.4s | 188 passed in 14.83s; ℹ tests 3; ℹ pass 3; ℹ fail 0; 61 passed in 50.64s; 55 passed in 0.09s; 210 pass; 0 fail; 1091 expect() calls; Ran 210 tests across 9 files. [77.00ms] |
| ✅ lint | `just lint` | 0 | 0.1s | All checks passed!; 49 files already formatted |

## 5. 红绿证明

基线 `3fd998d`，只记录，不拦截。

| 测试文件 | 基线 | HEAD | 判定 |
| :-- | :-: | :-: | :-- |
| `adws/tests/test_quality_gate.py` | exit 1 🔴 | exit 0 🟢 | ✅ 红→绿 |
| `tests/test_tui_capture.py` | exit 2 🔴 | exit 0 🟢 | ✅ 红→绿 |

<details><summary><code>uv run --no-project --with pytest --with pydantic --with pyyaml --with python-dotenv --with rich pytest -q adws/tests/test_quality_gate.py</code> 的输出</summary>

基线：

```text
.F                                                                       [100%]
=================================== FAILURES ===================================
_______________________ test_just_test_runs_every_suite ________________________

    def test_just_test_runs_every_suite():
        """The recipe the gate calls names every suite, so the gate does too."""
        justfile = (ROOT / "justfile").read_text(encoding="utf-8")
        recipe = re.search(r"^test:\n((?:    .*\n)+)", justfile, re.M)
        assert recipe, "no `test:` recipe in the justfile"
        lines = [line.strip() for line in recipe.group(1).splitlines()]
>       assert lines == ["just typecheck", "bun test", "just test-adws", "just test-autoqueue", "just test-tui-capture"]
E       AssertionError: assert ['just typech...st-autoqueue'] == ['just typech...-tui-capture']
E         
E         Right contains one more item: 'just test-tui-capture'
E         Use -v to get more diff

adws/tests/test_quality_gate.py:39: AssertionError
=========================== short test summary info ============================
FAILED adws/tests/test_quality_gate.py::test_just_test_runs_every_suite - Ass...
1 failed, 1 passed in 0.05s
```

HEAD：

```text
..                                                                       [100%]
2 passed in 0.04s
```

</details>

<details><summary><code>uv run --no-project --with pytest pytest -q tests/test_tui_capture.py</code> 的输出</summary>

基线：

```text

==================================== ERRORS ====================================
__________________ ERROR collecting tests/test_tui_capture.py __________________
tests/test_tui_capture.py:15: in <module>
    spec.loader.exec_module(capture)
<frozen importlib._bootstrap_external>:995: in exec_module
    ???
<frozen importlib._bootstrap_external>:1132: in get_code
    ???
<frozen importlib._bootstrap_external>:1190: in get_data
    ???
E   FileNotFoundError: [Errno 2] No such file or directory: '/private/var/folders/3z/t97nk5bd40b4cyggsfzd2syc0000gn/T/sssf-baseline-pgah4f3k/tree/scripts/tui_capture.py'
=========================== short test summary info ============================
ERROR tests/test_tui_capture.py - FileNotFoundError: [Errno 2] No such file o...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.05s
```

HEAD：

```text
.......................................................                  [100%]
55 passed in 0.29s
```

</details>

## 6. 测试完整性

- 用例数没有比较（没有改动计数器覆盖的测试文件，或无法解析）
- 没有发现改弱测试

## 7. 新增的测试

- test_masks_preserve_width_rows_whitespace_and_literal_replacement
- test_isolation_argv_environment_polling_and_artifacts
- test_locale_and_fallbacks
- test_invalid_document_is_preflight_failure
- test_invalid_json
- test_cli_preflight
- test_timeout_continues_and_is_reproducible
- test_success_reproducibility_and_exit_status_not_stdout
- test_command_failure_cleanup_and_continuation
- test_cleanup_failure_is_reported_without_hiding_original
- test_interruption_still_cleans_up
- test_example
- test_empty_text_is_noop_and_unrelated_files_survive
- test_artifact_write_failure_returns_one_and_cleans_all_scenes
- test_already_exited_server_is_not_cleanup_failure
- test_poll_client_timeout_is_bounded_by_remaining_deadline

## 8. Reviewer 逐条核对

✅ 通过：20 of 20 requirements met: the stdlib-only capture engine, example scenes, offline tests, recipes, and docs match the issue and plan, with only the human-run real-Pi capture left unverified.

| 需求 | 满足 | 证据 |
| :-- | :-: | :-- |
| New scripts/tui_capture.py using only the standard library | ✅ | scripts/tui_capture.py:3-19 — imports are argparse/json/math/os/re/shutil/subprocess/sys/tempfile/time/unicodedata/uuid/pathlib only |
| CLI --repo/--scenes/--out with exit 2 for bad arguments, bad scene file, or missing tmux | ✅ | scripts/tui_capture.py:250-273 — argparse SystemExit code returned; load_scenes and shutil.which('tmux') run before out.mkdir, so invalid input creates no artifacts |
| Each scene writes <name>.txt under --out, then manifest.json | ✅ | scripts/tui_capture.py:227-241; confirmed by a live end-to-end run producing screen-a.txt/screen-b.txt + manifest.json |
| Full preflight validation of the scene document before any capture | ✅ | load_scenes scripts/tui_capture.py:35-76 — required/optional key sets, nonempty launch/ready, two positive non-bool ints, finite positive non-bool timeout, regexes compiled, nonempty scenes, unique [a-z0-9_-]+ names, exactly-one-action steps |
| Commit scripts/tui_scenes.example.json with exactly the issue's example | ✅ | scripts/tui_scenes.example.json byte-matches the issue JSON; asserted in tests/test_tui_capture.py:392-407 |
| Isolation: a new tmux server per scene on a unique -L socket with -u, -f temp config, fixed -x/-y and cwd --repo | ✅ | scripts/tui_capture.py:127,180-200; tests assert distinct sockets, ['-d','-s','capture','-x','100','-y','30','-c',repo,'env'] |
| Temp tmux config containing set -g extended-keys on and extended-keys-format csi-u | ✅ | scripts/tui_capture.py:178 — config written and read back by the fake runner |
| Pane started with env -i allowing only PATH/HOME/TERM/LANG\|LC_ALL plus the four PI_* overrides; no API keys or user Pi config | ✅ | pane_environment scripts/tui_capture.py:78-94 and launch argv :184-201; test seeds DEEPSEEK_API_KEY/OTHER_TOKEN/TMUX/PI_* and asserts set(env) is exactly the eight allowed keys |
| Wait for ready, run steps, poll wait_for every 0.2s with no fixed waiting sleeps, per-wait timeout including the last screen, then one 0.3s settle and capture-pane -p | ✅ | scripts/tui_capture.py:165-176,209-210; tests assert capture times [0,0.2,0.4], exactly one 0.3s sleep after steps, and the last screen embedded in timeout errors |
| Masks: repo absolute path and its ~/ spelling first, then declared masks in order; replace is literal; otherwise # (## for W/F) preserving width; never delete rows or characters | ✅ | normalize_screen scripts/tui_capture.py:97-116 with MULTILINE and Path.relative_to (not string prefixes); tests cover digits, W/F, mask ordering, $ within a multi-line capture, spaces/quotes, paths outside HOME, preserved blank lines/trailing spaces/line count |
| kill-server on the unique socket in try/finally on success, failure, timeout and interruption; temp config/agent dirs removed | ✅ | scripts/tui_capture.py:212-219; assert_cleaned is invoked by every failure test including KeyboardInterrupt and an already-exited server |
| manifest.json: ordered {name,file,ok,error}, no timestamps or durations, byte-reproducible | ✅ | scripts/tui_capture.py:238-241; two-run byte equality asserted for success and for mixed failure/success; my own two real-tmux runs were byte-identical under diff -r |
| One failed scene must not stop the others; the manifest is still written; failed scenes store the normalized last screen (empty if none) | ✅ | scripts/tui_capture.py:227-241; test pre-creates a stale first.txt and proves it is overwritten with an empty screen while scene two still runs |
| Exit codes: 0 all-success, 1 scene failure, 2 argument/scene-file/tmux problems | ✅ | scripts/tui_capture.py:243 (any scene or manifest failure -> 1) and :272 (preflight -> 2); covered by the parsing, timeout and cleanup tests |
| just tui-capture scenes out repo="." for real runs, not part of just test | ✅ | justfile:31-33 with set positional-arguments; test: only gains 'just test-tui-capture' |
| Offline tests in tests/test_tui_capture.py wired into just test like the test-autoqueue recipe | ✅ | justfile:64-66 mirrors test-autoqueue's uv run --no-project --with pytest invocation; adws/tests/test_quality_gate.py:39 updated so the gate enumerates the new suite |
| Fake tmux runner tests: masks, argv/env, parsing, waiting/timeout, cleanup, manifest determinism — no real tmux/Pi/network | ✅ | tests/test_tui_capture.py covers all seven plan groups; which is patched and the runner is scripted; I re-ran it: 55 passed, exit 0 |
| Docs updated in the same change: README usage/outputs/exit codes/whitelist/masks/human gate and AGENTS structure + testing rule | ✅ | README.md:40-63; AGENTS.md:13 and :17 |
| Out of scope respected: no ADW/evidence integration, no before/after diff, no /hint or Bot-turn scenes, no src/ changes | ✅ | git status shows storage/feature changes only — src/ untouched; the example scenes are status and help only |
| just test passes | ✅ | recorded session quality/05_test/command.log shows '$ just test / exit: 0'; I independently re-ran the new suite (55 passed, exit 0) and git diff --check is clean |

## 9. 未验证项

- 未运行 `just smoke`（会调用 DeepSeek，按量计费；工厂不跑）
- Reviewer：Real Pi capture of scripts/tui_scenes.example.json producing status.txt/help.txt without an extended-keys warning and three runs byte-identical: needs the Pi CLI and the example's launch command, and the plan makes this a pre-merge human gate the factory does not run. My substitute /bin/sh TUI run exercised the same engine path but not Pi's rendering.
- 这些测试文件的用例数没有比较，只查了跳过标记和删除：adws/tests/test_quality_gate.py, tests/test_tui_capture.py
- 红绿证明只做了记录、没有拦截（kind 为 feature，不是 bug）

## 10. 成本

1,359,291 tokens · $2.6152

## Feedback since the factory's last reply

### 1. @aicoder2048 · review

人工验收：`just tui-capture scripts/tui_scenes.example.json <out>` 真实跑了 3 次，`status.txt`、`help.txt`、`manifest.json` 逐字节相同，屏幕上没有 extended-keys 警告。引擎本身没问题，有两处要改：

1. **分支名掩码在真实画面上匹配不到。** 路径和分支名太长时，Pi 会截断底栏，实际截到的是 `<repo> (factory/iss...`，没有右括号，`scripts/tui_scenes.example.json` 里那条 `(?<=<repo> \()[^)]*(?=\)$)` 就匹配不上了。在基线树和 HEAD 树上，分支名和截断位置都不一样，这一行会产生假 diff。请把例子改成从 `<repo> ` 后面一直匹配到行尾，统一替换成 `(<branch>)`，例如 `{"pattern": "(?<=<repo> )\\(.*$", "replace": "(<branch>)"}`。同时更新 README 和测试里的例子，并加一条测试：被截断、没有右括号的底栏也能掩码。

2. **tmux 的 socket 文件会一直留在 `/tmp/tmux-<uid>/`。** 跑完 3 次后，那里多了 10 个 `tui-capture-<uuid>=`。server 已经 `kill-server` 了，但在 macOS 上 socket 文件不会被删掉。请改用 `-S <场景临时目录>/tmux.sock`，不要再用 `-L`，这样 socket 跟着临时目录一起删掉，也就不会去碰 `/tmp/tmux-<uid>/`。argv 测试和清理测试也一起改，要断言 socket 路径在临时目录里，而且清理后临时目录不存在。
