import { afterEach, beforeEach, expect, test } from "bun:test";
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import type { GameRecord } from "../../src/engine/records.ts";
import { readRecords, recordsFilePath, saveRecord } from "../../src/extension/records-store.ts";

let dir: string;
beforeEach(() => { dir = mkdtempSync(join(tmpdir(), "idiom-store-")); });
afterEach(() => rmSync(dir, { recursive: true, force: true }));
const row: GameRecord = { id: "a", endedAt: "2026-01-01T00:00:00.000Z", mode: "normal",
  rounds: 1, scores: { human: 2, bot: 2 }, winner: "draw" };

test("路径：注入 home 的默认值与非空环境变量覆盖", () => {
  expect(recordsFilePath({}, "/fake-home")).toBe("/fake-home/.pi/agent/idiom-solitaire/records.json");
  expect(recordsFilePath({ IDIOM_RECORDS_FILE: "relative.json" }, "/fake-home")).toBe("relative.json");
  expect(recordsFilePath({ IDIOM_RECORDS_FILE: "" }, "/fake-home")).toBe(recordsFilePath({}, "/fake-home"));
});

test("缺失文件为空；首次保存建目录，后续追加和覆盖", () => {
  const path = join(dir, "nested", "records.json");
  expect(readRecords(path)).toEqual([]);
  expect(existsSync(path)).toBe(false);
  saveRecord(row, path);
  expect(JSON.parse(readFileSync(path, "utf8"))).toEqual([row]);
  const other = { ...row, id: "b" };
  saveRecord(other, path);
  const replacement = { ...row, rounds: 2 };
  saveRecord(replacement, path);
  expect(readRecords(path)).toEqual([replacement, other]);
});

for (const value of ["broken", "{}", "[null]", JSON.stringify([row, row]),
  ...[{ id: "" }, { mode: "unknown" }, { winner: "unknown" }, { winner: "human" },
    { endedAt: "yesterday" }, { endedAt: "2026-02-30T00:00:00.000Z" }, { rounds: 0 }, { rounds: 1.5 },
    { scores: { human: "2", bot: 2 } }, { scores: { human: null, bot: 2 } }]
    .map((patch) => JSON.stringify([{ ...row, ...patch }]))]) {
  test(`损坏/无效结构不覆盖：${value}`, () => {
    const path = join(dir, "records.json");
    writeFileSync(path, value);
    expect(() => readRecords(path)).toThrow();
    expect(() => saveRecord(row, path)).toThrow();
    expect(readFileSync(path, "utf8")).toBe(value);
  });
}

test("文件充当目录或目录充当文件，读写异常上抛", () => {
  const parent = join(dir, "file");
  writeFileSync(parent, "untouched");
  for (const path of [dir, join(parent, "records.json")]) {
    expect(() => readRecords(path)).toThrow();
    expect(() => saveRecord(row, path)).toThrow();
  }
  expect(readFileSync(parent, "utf8")).toBe("untouched");
});
