import { expect, test } from "bun:test";
import { summarizeRecords, upsertRecord, type GameRecord } from "../../src/engine/records.ts";

const draw: GameRecord = { id: "a", endedAt: "2026-01-01T00:00:00.000Z", mode: "normal",
  rounds: 1, scores: { human: 2, bot: 2 }, winner: "draw" };

test("战绩统计：空集与含负分的胜负平，平局计入胜率分母", () => {
  expect(summarizeRecords([])).toEqual({ total: 0, wins: 0, losses: 0, draws: 0, winRate: 0 });
  expect(summarizeRecords([draw,
    { ...draw, id: "b", scores: { human: 2, bot: 0 }, winner: "human" },
    { ...draw, id: "c", scores: { human: -1, bot: 0 }, winner: "bot" },
  ])).toEqual({ total: 3, wins: 1, losses: 1, draws: 1, winRate: 1 / 3 });
});

test("upsert 追加或按 id 覆盖，不修改输入或其它行", () => {
  const other = { ...draw, id: "b" };
  const records = [draw, other];
  const snapshot = structuredClone(records);
  const replacement = { ...draw, rounds: 2 };
  expect(upsertRecord(records, replacement)).toEqual([replacement, other]);
  expect(upsertRecord(records, { ...draw, id: "c" })).toEqual([...records, { ...draw, id: "c" }]);
  expect(records).toEqual(snapshot);
});
