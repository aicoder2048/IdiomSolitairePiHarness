/** 跨局战绩的纯数据操作；时间、身份与文件 IO 由扩展负责。 */
import type { Mode } from "./game.ts";

export interface GameRecord {
  id: string;
  endedAt: string;
  mode: Mode;
  rounds: number;
  scores: { human: number; bot: number };
  winner: "human" | "bot" | "draw";
}

export interface RecordsSummary {
  total: number;
  wins: number;
  losses: number;
  draws: number;
  winRate: number;
}

export function summarizeRecords(records: readonly GameRecord[]): RecordsSummary {
  const wins = records.filter((r) => r.winner === "human").length;
  const losses = records.filter((r) => r.winner === "bot").length;
  return { total: records.length, wins, losses, draws: records.length - wins - losses,
    winRate: records.length === 0 ? 0 : wins / records.length };
}

export function upsertRecord(records: readonly GameRecord[], record: GameRecord): GameRecord[] {
  return records.some((r) => r.id === record.id)
    ? records.map((r) => r.id === record.id ? record : r)
    : [...records, record];
}
