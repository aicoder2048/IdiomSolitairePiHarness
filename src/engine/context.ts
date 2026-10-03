/**
 * 【Context Engineering】接龙链：一份完整历史，两种视图。
 *
 *   usedIdioms()   基于完整历史，供确定性规则判重（记录系统）
 *   recentIdioms() 只取最近 N 个，进 Bot 的回合 prompt（模型视野，Compaction）
 *
 * 压缩只作用于视野，不作用于规则：Bot 说出 20 轮前用过的成语，判重照样拦下。
 */

export type Player = "human" | "bot";

export interface Turn {
  player: Player;
  idiom: string;
  score: number;
}

export class ChainHistory {
  readonly turns: Turn[] = [];

  constructor(readonly maxHistoryTurns = 10) {}

  addTurn(player: Player, idiom: string, score: number): void {
    this.turns.push({ player, idiom, score });
  }

  usedIdioms(): Set<string> {
    return new Set(this.turns.map((t) => t.idiom));
  }

  recentIdioms(): string[] {
    return this.turns.slice(-this.maxHistoryTurns).map((t) => t.idiom);
  }

  truncate(length: number): void {
    this.turns.length = Math.min(this.turns.length, length);
  }

  clear(): void {
    this.turns.length = 0;
  }
}
