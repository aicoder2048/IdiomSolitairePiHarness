/** 纯展示：把对局状态变成要显示的文字行。不碰 Pi，方便测试，也方便以后换成带主题色的组件。 */

import { MODE_CONFIGS, MODE_LABELS, PASS_PENALTY, type HumanMove, type IdiomGame, type RoundRecord } from "../engine/game.ts";
import type { UsageTotals } from "./llm-client.ts";

/** 斜杠命令：名字 → [参数提示, 说明]。注册命令与 /help 共用这一张表。 */
export const COMMANDS: Record<string, [args: string, description: string]> = {
  hint: ["", "求助：给出候选成语，本轮 0 分并转 Bot"],
  pass: ["", `跳过本轮：${PASS_PENALTY} 分并转 Bot`],
  undo: ["", "悔棋：撤销上一整轮"],
  difficulty: ["<easy|normal|hard|extreme>", "切换难度"],
  rounds: ["<N>", "设置总轮数"],
  timer: ["<秒>", "设置每轮倒计时，0 为关闭"],
  restart: ["[首字]", "重新开局"],
  status: ["", "详细状态面板"],
  help: ["", "查看命令与规则"],
};

const CHAIN_WIDGET_LEN = 6;

function signed(n: number): string {
  return n > 0 ? `+${n}` : `${n}`;
}

/** 编辑器上方的简版仪表盘。 */
export function boardLines(game: IdiomGame): string[] {
  const round = Math.min(game.currentRound, game.maxRounds);
  let clock = "";
  if (game.gameOver) clock = " · 对局结束";
  else if (game.awaitingBot) clock = " · Bot 思考中…";
  else {
    const left = game.secondsLeft();
    if (left !== null) clock = left > 0 ? ` · ⏱ ${left}s` : " · ⏱ 已超时（作答按跳过计）";
  }
  const lines = [
    `🀄 成语接龙 · 第 ${round}/${game.maxRounds} 轮 · ${MODE_LABELS[game.mode]}${clock}`,
    `你 ${game.scores.human} : ${game.scores.bot} Bot` + (game.gameOver || game.awaitingBot ? "" : ` · 请接「${game.lastChar}」`),
  ];
  const chain = game.chain.turns.map((t) => t.idiom);
  if (chain.length > 0) {
    const shown = chain.slice(-CHAIN_WIDGET_LEN).join(" → ");
    lines.push(`链：${chain.length > CHAIN_WIDGET_LEN ? "… → " : ""}${shown}`);
  }
  return lines;
}

export function describeHumanMove(move: HumanMove): string {
  switch (move.kind) {
    case "idiom":
      return `你：${move.idiom}（${signed(move.gained)}）`;
    case "pass":
      return `你跳过本轮（${signed(move.gained)}）`;
    case "timeout":
      return `超时，按跳过计（${signed(move.gained)}）`;
    case "hint":
      return "你使用了提示（本轮 0 分）";
  }
}

export function describeBot(record: RoundRecord): string {
  const { bot, botGained } = record;
  if (bot.status === "success") {
    const retries = bot.attempts.length > 1 ? `，自检 ${bot.attempts.length} 次` : "";
    return `Bot：${bot.idiom}（${signed(botGained)}${retries}）`;
  }
  return `Bot 放弃：${bot.attempts.at(-1)?.reason ?? "没有给出合规成语"}`;
}

/** 一回合结束后在对话流里留一张卡片。 */
export function roundCardLines(record: RoundRecord): string[] {
  const lines = [`第 ${record.roundNo} 轮 · 接「${record.targetChar}」`, describeHumanMove(record.human), describeBot(record)];
  for (const a of record.bot.attempts.filter((a) => !a.ok)) {
    lines.push(`  ✗ ${a.candidate || "（无候选）"}：${a.reason}`);
  }
  return lines;
}

export function finalLines(game: IdiomGame): string[] {
  const verdict = { human: "你赢了！🎉", bot: "Bot 获胜。", draw: "平局。" }[game.winner()];
  return ["🏁 对局结束", `你 ${game.scores.human} : ${game.scores.bot} Bot · ${verdict}`, "输入 /restart 再来一局，或 /rounds 加轮数继续。"];
}

export function statusLines(game: IdiomGame, usage?: UsageTotals): string[] {
  const human = MODE_CONFIGS[game.mode].human;
  const bot = MODE_CONFIGS[game.mode].bot;
  const left = game.secondsLeft();
  const lines = [
    `难度：${MODE_LABELS[game.mode]}（${game.mode}）`,
    `  你：×${human.multiplier} · ${human.allowHomophone ? "允许" : "不允许"}谐音 · ${human.dictLevel} 词库`,
    `  Bot：×${bot.multiplier} · ${bot.allowHomophone ? "允许" : "不允许"}谐音 · ${bot.dictLevel} 词库`,
    `轮次：${Math.min(game.currentRound, game.maxRounds)}/${game.maxRounds}${game.gameOver ? "（已结束）" : ""}`,
    `倒计时：${game.timerSeconds === 0 ? "关闭" : `${game.timerSeconds} 秒，本轮剩 ${left ?? 0} 秒`}`,
    `比分：你 ${game.scores.human} : ${game.scores.bot} Bot`,
    `接龙链（${game.chain.turns.length}）：${game.chain.turns.map((t) => t.idiom).join(" → ") || "（空）"}`,
  ];
  for (const r of game.roundLog) lines.push(`  第 ${r.roundNo} 轮：${describeHumanMove(r.human)} / ${describeBot(r)}`);
  if (usage) {
    lines.push(`裁判/提示调用：${usage.calls} 次 · 输入 ${usage.input} · 输出 ${usage.output} tokens · $${usage.cost.toFixed(4)}`);
  }
  return lines;
}

export function helpLines(): string[] {
  return [
    "规则：用上一个成语的末字开头接龙。原字 2 分、谐音 1 分（看难度），再乘难度倍率；至少 4 字，本局不可重复。",
    "直接输入成语作答；Bot 由模型扮演，只能通过 submit_idiom 工具出词，和你用同一个裁判。",
    "命令（都不花 token，/hint 除外）：",
    ...Object.entries(COMMANDS).map(([name, [args, desc]]) => `  /${name}${args ? ` ${args}` : ""} — ${desc}`),
    "  /quit — 退出（Pi 内置）",
  ];
}

export function usageStatus(usage: UsageTotals): string {
  return `裁判/提示 ${usage.calls} 次 · ${usage.input + usage.output} tokens`;
}
