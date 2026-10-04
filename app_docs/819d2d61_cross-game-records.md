# Cross-game records and `/records`

Completed games now persist a local JSON history, and `/records` presents lifetime totals plus the ten most recent results. This makes results available across sessions without adding model calls or changing the existing final-settlement presentation.

## Where it lives

- `src/engine/records.ts` defines the record shape and pure `summarizeRecords` / `upsertRecord` operations.
- `src/extension/records-store.ts` resolves the path, validates JSON, reads records and writes an ID-based upsert. Its default is `~/.pi/agent/idiom-solitaire/records.json`; a nonempty `IDIOM_RECORDS_FILE` overrides it. Missing files mean empty history, and writes create parent directories. Invalid or unreadable history throws rather than being replaced.
- `src/extension/index.ts` assigns a game ID and saves completed results. New sessions and successful `/restart` get new IDs; undo and continuing with more rounds retain the ID, so a later completion replaces that result. Read/write errors become warnings and do not stop gameplay.
- `src/extension/view.ts` registers `/records` in the shared command table and formats the player card. It shows wins, losses, draws, win rate (wins divided by all games), and recent dates, difficulty, scores and verdicts. The command displays a card in all modes and does not call the model.

`README.md` describes player usage and storage configuration; `AGENTS.md` records the implementation and test-isolation rule. The pure operations, storage boundary, formatting, command behavior, lifecycle cases and failure handling have coverage in `tests/engine/records.test.ts`, `tests/extension/records-store.test.ts`, `tests/extension/view.test.ts` and `tests/extension/extension.test.ts`.

## Use and verify

Run `/records` to view history. To choose a different local file, set `IDIOM_RECORDS_FILE` when starting the extension, for example:

```sh
IDIOM_RECORDS_FILE="$HOME/my-games/records.json" just play
```

Run `just test` to check the full offline suite; the focused feature tests can be run with:

```sh
bun test tests/engine/records.test.ts tests/extension/records-store.test.ts tests/extension/view.test.ts tests/extension/extension.test.ts
```
