/**
 * 【Harness Engineering】对局状态机：包在模型外面的确定性外壳，不依赖 Pi。
 *
 * 记录系统   scores / roundLog / 快照栈（/undo 整轮回滚）/ 接龙链
 * 反馈闭环   同一个 Verifier 判人类答案与 Bot 候选
 * 护栏       模式矩阵、倒计时、总轮数、Bot 重试预算
 *
 * 与 Python 版的区别：Bot 的出词由 Pi 的 agent loop 驱动，是异步、分多次到达的，
 * 所以一回合拆成两段：
 *   startRound()  人类这一步入账（压快照），进入「等 Bot」状态，产出给 Bot 的回合 prompt
 *   submitBot()   Bot 每调用一次 submit_idiom 就是一次尝试；通过或预算用尽时结算本回合
 * 写账只发生在这两处，模型只能「提议」候选，永远碰不到账本。
 */

import { ChainHistory, type Player } from "./context.ts";
import type { LLMClient } from "./llm.ts";
import { buildHintMessages, buildObservation, buildRoundPrompt, type DictLevel } from "./prompts.ts";
import { checkRules, normalizeIdiom } from "./rules.ts";
import { Verifier } from "./verifier.ts";

export type Mode = "easy" | "normal" | "hard" | "extreme";

export interface PlayerConfig {
  multiplier: number;
  allowHomophone: boolean;
  dictLevel: DictLevel;
}

/** 难度模式配置矩阵（四阶难度，宽松/严格两档词库）。 */
export const MODE_CONFIGS: Record<Mode, Record<Player, PlayerConfig>> = {
  easy: { human: { multiplier: 2, allowHomophone: true, dictLevel: "lax" }, bot: botConfig() },
  normal: { human: { multiplier: 1, allowHomophone: true, dictLevel: "lax" }, bot: botConfig() },
  hard: { human: { multiplier: 1, allowHomophone: false, dictLevel: "lax" }, bot: botConfig() },
  extreme: { human: { multiplier: 1, allowHomophone: false, dictLevel: "strict" }, bot: botConfig() },
};
export const MODES = Object.keys(MODE_CONFIGS) as Mode[];
export const MODE_LABELS: Record<Mode, string> = { easy: "简单", normal: "普通", hard: "困难", extreme: "极限" };

function botConfig(): PlayerConfig {
  return { multiplier: 1, allowHomophone: false, dictLevel: "strict" };
}

export const DEFAULT_START_CHAR = "心";
export const PASS_PENALTY = -1;
export const MAX_ROUNDS_LIMIT = 99;
export const TIMER_RANGE = [5, 600] as const;
const SINGLE_CJK = /^[一-鿿]$/;
const DIGITS = /^\d+$/;

export interface HumanMove {
  kind: "idiom" | "pass" | "hint" | "timeout";
  idiom: string;
  gained: number;
  reason: string;
}

export interface Attempt {
  candidate: string;
  ok: boolean;
  reason: string;
}

export interface BotResult {
  status: "success" | "failed";
  idiom: string;
  score: number; // 基础分，未乘模式倍率
  attempts: Attempt[];
}

export interface RoundRecord {
  roundNo: number;
  targetChar: string;
  human: HumanMove;
  bot: BotResult;
  botGained: number;
}

export type Outcome =
  | { kind: "noop" }
  | { kind: "info"; message: string }
  | { kind: "busy"; message: string }
  | { kind: "invalid"; message: string }
  | { kind: "error"; message: string }
  | { kind: "command"; message: string }
  | { kind: "bot_turn"; human: HumanMove; prompt: string; hints: string[] };

export type BotSubmitResult =
  | { kind: "rejected"; observation: string; attemptsLeft: number }
  | { kind: "round"; record: RoundRecord; gameOver: boolean }
  | { kind: "stale"; message: string };

export interface GameOptions {
  llm: LLMClient;
  clock?: () => number; // 秒
  startChar?: string;
  maxRounds?: number;
  timerSeconds?: number;
  botMaxRetries?: number;
  maxHistoryTurns?: number;
}

interface Snapshot {
  scores: Record<Player, number>;
  currentRound: number;
  lastChar: string;
  historyLen: number;
  logLen: number;
}

interface PendingBotTurn {
  targetChar: string; // 本回合开始时人类要接的字（记账用）
  human: HumanMove;
  attempts: Attempt[];
}

const BUSY: Outcome = { kind: "busy", message: "Bot 正在接龙，请稍等。" };
const GAME_OVER_HINT = "游戏已结束！输入 /restart 重新开局，或 /rounds 增加轮数继续。";

export class IdiomGame {
  readonly verifier: Verifier;
  readonly chain: ChainHistory;
  mode: Mode = "normal";
  maxRounds: number;
  timerSeconds: number;
  readonly botMaxRetries: number;

  startChar = DEFAULT_START_CHAR;
  lastChar = DEFAULT_START_CHAR;
  currentRound = 1;
  scores: Record<Player, number> = { human: 0, bot: 0 };
  roundLog: RoundRecord[] = [];
  private snapshots: Snapshot[] = [];
  private pending: PendingBotTurn | null = null;
  private turnStartedAt = 0;

  private readonly llm: LLMClient;
  private readonly clock: () => number;

  constructor(opts: GameOptions) {
    this.llm = opts.llm;
    this.clock = opts.clock ?? (() => performance.now() / 1000);
    this.verifier = new Verifier(opts.llm);
    this.chain = new ChainHistory(opts.maxHistoryTurns ?? 10);
    this.maxRounds = opts.maxRounds ?? 9;
    this.timerSeconds = opts.timerSeconds ?? 30;
    this.botMaxRetries = opts.botMaxRetries ?? 3;
    this.reset(opts.startChar ?? DEFAULT_START_CHAR);
  }

  // ------------------------------------------------------------------ 状态

  get gameOver(): boolean {
    return this.currentRound > this.maxRounds;
  }

  get awaitingBot(): boolean {
    return this.pending !== null;
  }

  /** 当前 Bot 回合已用掉的尝试（UI 展示用）。 */
  get pendingAttempts(): readonly Attempt[] {
    return this.pending?.attempts ?? [];
  }

  config(player: Player): PlayerConfig {
    return MODE_CONFIGS[this.mode][player];
  }

  /** 本轮剩余秒数；倒计时关闭时返回 null。 */
  secondsLeft(): number | null {
    if (this.timerSeconds <= 0) return null;
    return Math.max(0, Math.trunc(this.timerSeconds - (this.clock() - this.turnStartedAt)));
  }

  winner(): Player | "draw" {
    const { human, bot } = this.scores;
    return human > bot ? "human" : bot > human ? "bot" : "draw";
  }

  private reset(startChar: string): void {
    this.startChar = startChar;
    this.lastChar = startChar;
    this.currentRound = 1;
    this.scores = { human: 0, bot: 0 };
    this.roundLog = [];
    this.snapshots = [];
    this.pending = null;
    this.chain.clear();
    this.restartTimer();
  }

  private restartTimer(): void {
    this.turnStartedAt = this.clock();
  }

  private timedOut(): boolean {
    return this.timerSeconds > 0 && this.clock() - this.turnStartedAt > this.timerSeconds;
  }

  // ------------------------------------------------------------------ 人类这一步

  async submitHuman(raw: string, signal?: AbortSignal): Promise<Outcome> {
    const text = raw.trim();
    if (!text) return { kind: "noop" };
    if (this.pending) return BUSY;
    if (this.gameOver) return { kind: "info", message: GAME_OVER_HINT };
    if (this.timedOut()) {
      return this.startRound({ kind: "timeout", idiom: "", gained: PASS_PENALTY, reason: "超时未作答" });
    }

    const idiom = normalizeIdiom(text);
    const cfg = this.config("human");
    const verdict = await this.verifier.verify(
      this.lastChar,
      idiom,
      cfg.allowHomophone,
      cfg.dictLevel,
      this.chain.usedIdioms(),
      signal,
    );
    if (this.pending) return BUSY; // 等裁判期间已经有别的输入开了回合
    if (!verdict.isValid) return { kind: "invalid", message: verdict.reason };
    return this.startRound({ kind: "idiom", idiom, gained: verdict.score * cfg.multiplier, reason: verdict.reason });
  }

  pass(): Outcome {
    if (this.pending) return BUSY;
    if (this.gameOver) return { kind: "info", message: GAME_OVER_HINT };
    return this.startRound({ kind: "pass", idiom: "", gained: PASS_PENALTY, reason: "主动跳过" });
  }

  async hint(n = 3, signal?: AbortSignal): Promise<Outcome> {
    if (this.pending) return BUSY;
    if (this.gameOver) return { kind: "info", message: GAME_OVER_HINT };
    const hints = await this.suggestHints(this.lastChar, n, signal);
    if (this.pending) return BUSY;
    if (hints.length === 0) return { kind: "error", message: "暂时没拿到可用的提示，本轮不计，请继续作答或 /pass。" };
    return this.startRound({ kind: "hint", idiom: "", gained: 0, reason: "使用提示" }, hints);
  }

  /** 给人类的提示：LLM 出候选，确定性规则过滤（只留原字开头、未用过、去重）。 */
  async suggestHints(targetChar: string, n = 3, signal?: AbortSignal): Promise<string[]> {
    const used = this.chain.usedIdioms();
    let response: Record<string, unknown>;
    try {
      response = await this.llm.completeJson(buildHintMessages(targetChar, n + 2, [...used].sort()), signal);
    } catch {
      return []; // 调用方把「没拿到提示」作为 error outcome 告诉玩家
    }
    const raw = response.candidates;
    if (!Array.isArray(raw)) return [];

    const hints: string[] = [];
    for (const item of raw) {
      const idiom = normalizeIdiom(String(item));
      if (checkRules(targetChar, idiom, false, used).ok && !hints.includes(idiom)) hints.push(idiom);
    }
    return hints.slice(0, n);
  }

  private startRound(human: HumanMove, hints: string[] = []): Outcome {
    this.snapshots.push({
      scores: { ...this.scores },
      currentRound: this.currentRound,
      lastChar: this.lastChar,
      historyLen: this.chain.turns.length,
      logLen: this.roundLog.length,
    });
    const targetChar = this.lastChar;
    this.scores.human += human.gained;
    if (human.idiom) {
      this.chain.addTurn("human", human.idiom, human.gained);
      this.lastChar = lastCharOf(human.idiom);
    }
    this.pending = { targetChar, human, attempts: [] };

    const cfg = this.config("bot");
    const prompt = buildRoundPrompt(this.lastChar, cfg.allowHomophone, cfg.dictLevel, this.chain.recentIdioms());
    return { kind: "bot_turn", human, prompt, hints };
  }

  // ------------------------------------------------------------------ Bot 这一步

  /** Bot 每次调用 submit_idiom 都走这里：校验、计预算，通过或用尽时结算本回合。 */
  async submitBot(raw: string, signal?: AbortSignal): Promise<BotSubmitResult> {
    const pending = this.pending;
    if (!pending) return { kind: "stale", message: "现在不是 Bot 的回合，本次提交不计。" };

    const candidate = normalizeIdiom(raw);
    const cfg = this.config("bot");
    const verdict = await this.verifier.verify(
      this.lastChar,
      candidate,
      cfg.allowHomophone,
      cfg.dictLevel,
      this.chain.usedIdioms(),
      signal,
    );
    if (this.pending !== pending) return { kind: "stale", message: "本回合已经结算，本次提交不计。" };

    pending.attempts.push({ candidate, ok: verdict.isValid, reason: verdict.reason });
    if (verdict.isValid) {
      return this.finishRound({ status: "success", idiom: candidate, score: verdict.score, attempts: pending.attempts });
    }
    const attemptsLeft = this.botMaxRetries - pending.attempts.length;
    if (attemptsLeft <= 0) return this.finishRound(failed(pending.attempts));
    return { kind: "rejected", observation: buildObservation(candidate, verdict.reason, attemptsLeft), attemptsLeft };
  }

  /** Bot 没有合规提交就停下（不调工具、被中断）时，按放弃结算。 */
  forfeitBot(reason: string): BotSubmitResult {
    const pending = this.pending;
    if (!pending) return { kind: "stale", message: "现在不是 Bot 的回合。" };
    pending.attempts.push({ candidate: "", ok: false, reason });
    return this.finishRound(failed(pending.attempts));
  }

  private finishRound(bot: BotResult): BotSubmitResult {
    const pending = this.pending!;
    this.pending = null;

    const botGained = bot.score * this.config("bot").multiplier;
    if (bot.status === "success") {
      this.scores.bot += botGained;
      this.chain.addTurn("bot", bot.idiom, botGained);
      this.lastChar = lastCharOf(bot.idiom);
    }
    const record: RoundRecord = {
      roundNo: this.currentRound,
      targetChar: pending.targetChar,
      human: pending.human,
      bot,
      botGained,
    };
    this.roundLog.push(record);
    this.currentRound += 1;
    this.restartTimer();
    return { kind: "round", record, gameOver: this.gameOver };
  }

  // ------------------------------------------------------------------ 命令（0 token）

  setMode(arg: string): Outcome {
    if (this.pending) return BUSY;
    const mode = arg.trim().toLowerCase();
    if (!isMode(mode)) return { kind: "error", message: `未知难度「${mode}」！可选：${MODES.join(", ")}` };
    this.mode = mode;
    return { kind: "command", message: `已切换到 [${mode.toUpperCase()} · ${MODE_LABELS[mode]}] 难度，下一步起生效。` };
  }

  setRounds(arg: string): Outcome {
    const text = arg.trim();
    if (!DIGITS.test(text)) return { kind: "error", message: "用法：/rounds <N>，N 为正整数" };
    const n = Number(text);
    const played = this.currentRound - 1;
    const lo = Math.max(1, played);
    if (n < lo || n > MAX_ROUNDS_LIMIT) {
      return { kind: "error", message: `总轮数需在 ${lo}~${MAX_ROUNDS_LIMIT} 之间（已进行 ${played} 轮）` };
    }
    this.maxRounds = n;
    return { kind: "command", message: `总轮数已调整为 ${n} 轮。` };
  }

  setTimer(arg: string): Outcome {
    const [lo, hi] = TIMER_RANGE;
    const text = arg.trim();
    const n = Number(text);
    if (!DIGITS.test(text) || !(n === 0 || (n >= lo && n <= hi))) {
      return { kind: "error", message: `用法：/timer <秒>，0 关闭，或 ${lo}~${hi} 秒` };
    }
    this.timerSeconds = n;
    this.restartTimer();
    return { kind: "command", message: n === 0 ? "倒计时已关闭。" : `每轮倒计时 ${n} 秒。` };
  }

  undo(): Outcome {
    if (this.pending) return BUSY;
    const snap = this.snapshots.pop();
    if (!snap) return { kind: "error", message: "没有可以撤销的回合。" };
    const undone = this.roundLog[snap.logLen];
    this.scores = { ...snap.scores };
    this.currentRound = snap.currentRound;
    this.lastChar = snap.lastChar;
    this.chain.truncate(snap.historyLen);
    this.roundLog.length = snap.logLen;
    this.restartTimer();
    const what = undone ? `第 ${undone.roundNo} 轮` : "上一轮";
    return { kind: "command", message: `已撤销${what}，回到接「${this.lastChar}」。` };
  }

  restart(arg = ""): Outcome {
    if (this.pending) return BUSY;
    const start = arg.trim() || DEFAULT_START_CHAR;
    if (!SINGLE_CJK.test(start)) return { kind: "error", message: "首字必须是单个汉字，例如：/restart 天" };
    this.reset(start);
    return { kind: "command", message: `新的一局开始！首字「${start}」，共 ${this.maxRounds} 轮。` };
  }
}

function isMode(value: string): value is Mode {
  return Object.hasOwn(MODE_CONFIGS, value);
}

function lastCharOf(idiom: string): string {
  return Array.from(idiom).at(-1)!;
}

function failed(attempts: Attempt[]): BotResult {
  return { status: "failed", idiom: "", score: 0, attempts };
}
