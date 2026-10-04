/** 本地 JSON 战绩。异常由扩展边界转为警告，损坏历史绝不当作空数组覆盖。 */
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { homedir } from "node:os";
import { dirname, join } from "node:path";
import { MODES } from "../engine/game.ts";
import { upsertRecord, type GameRecord } from "../engine/records.ts";

export function recordsFilePath(env: Record<string, string | undefined> = process.env, home = homedir()): string {
  return env.IDIOM_RECORDS_FILE || join(home, ".pi", "agent", "idiom-solitaire", "records.json");
}

function isRecord(value: unknown): value is GameRecord {
  if (typeof value !== "object" || value === null) return false;
  const r = value as GameRecord;
  if (typeof r.id !== "string" || !r.id.trim() || typeof r.endedAt !== "string" ||
      !Number.isFinite(Date.parse(r.endedAt)) || new Date(r.endedAt).toISOString() !== r.endedAt ||
      !MODES.includes(r.mode) || !Number.isInteger(r.rounds) || r.rounds <= 0 ||
      !r.scores || !Number.isFinite(r.scores.human) || !Number.isFinite(r.scores.bot)) return false;
  const winner = r.scores.human > r.scores.bot ? "human" : r.scores.human < r.scores.bot ? "bot" : "draw";
  return r.winner === winner;
}

export function readRecords(path = recordsFilePath()): GameRecord[] {
  let text: string;
  try { text = readFileSync(path, "utf8"); }
  catch (error) {
    if ((error as NodeJS.ErrnoException).code === "ENOENT") return [];
    throw error;
  }
  const records: unknown = JSON.parse(text);
  if (!Array.isArray(records) || !records.every(isRecord) ||
      new Set(records.map((r) => r.id)).size !== records.length) {
    throw new Error("战绩文件格式无效");
  }
  return records;
}

export function saveRecord(record: GameRecord, path = recordsFilePath()): void {
  const records = upsertRecord(readRecords(path), record);
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(records, null, 2) + "\n", "utf8");
}
