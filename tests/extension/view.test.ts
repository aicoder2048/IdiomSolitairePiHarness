import { expect, test } from "bun:test";
import { IdiomGame } from "../../src/engine/game.ts";
import { boardLines, chainLines, finalLines, helpLines, recordsLines, statusLines } from "../../src/extension/view.ts";
import { FakeClock, FakeLLM } from "../fakes.ts";

function make(timerSeconds = 30) {
  const clock = new FakeClock();
  return { game: new IdiomGame({ llm: new FakeLLM(), clock: clock.read, timerSeconds }), clock };
}

test("仪表盘：轮次、难度、倒计时、比分、接龙字", () => {
  const { game, clock } = make();
  clock.now += 12;
  const [title, score] = boardLines(game);
  expect(title).toContain("第 1/9 轮");
  expect(title).toContain("普通");
  expect(title).toContain("18s");
  expect(score).toContain("请接「心」");
});

test("仪表盘：Bot 思考时不显示倒计时与接龙字", async () => {
  const { game } = make();
  await game.submitHuman("心想事成");
  const [title, score, chain] = boardLines(game);
  expect(title).toContain("Bot 思考中");
  expect(score).not.toContain("请接");
  expect(chain).toBe("链：心想事成");
});

test("仪表盘：超时提示", () => {
  const { game, clock } = make();
  clock.now += 31;
  expect(boardLines(game)[0]).toContain("已超时");
});

test("仪表盘：接龙链只显示最后几个", async () => {
  const { game } = make(0);
  const idioms = ["心想事成", "成竹在胸", "胸有成竹", "竹报平安", "安居乐业", "业精于勤", "勤能补拙"];
  for (let i = 0; i < idioms.length; i += 2) {
    await game.submitHuman(idioms[i]!);
    const next = idioms[i + 1];
    if (next) await game.submitBot(next);
    else game.forfeitBot("test");
  }
  const chain = boardLines(game)[2]!;
  expect(chain.startsWith("链：… → ")).toBe(true);
  expect(chain).not.toContain("心想事成");
  expect(chain).toContain("勤能补拙");
});

test("状态面板含难度配置与用量", () => {
  const { game } = make();
  const text = statusLines(game, { calls: 2, input: 100, output: 20, cost: 0.001 }).join("\n");
  expect(text).toContain("lax 词库");
  expect(text).toContain("2 次");
});

test("帮助列出全部命令", () => {
  const text = helpLines().join("\n");
  for (const name of ["/hint", "/pass", "/undo", "/difficulty", "/rounds", "/timer", "/restart", "/status", "/chain", "/records"]) {
    expect(text).toContain(name);
  }
});


test("接龙链：空链提示", () => {
  expect(chainLines(make().game)).toEqual(["还没有成语"]);
});

test("接龙链：包含待 Bot 接龙的人类出词，完成后按顺序显示双方", async () => {
  const { game } = make();
  await game.submitHuman("心想事成");
  expect(game.awaitingBot).toBe(true);
  expect(game.roundLog).toEqual([]);
  expect(chainLines(game)).toEqual(["1. 你：心想事成（+2）"]);
  await game.submitBot("成竹在胸");
  expect(chainLines(game)).toEqual(["1. 你：心想事成（+2）", "2. Bot：成竹在胸（+2）"]);
});

test("接龙链：完整历史超过仪表盘和模型视野，角色取自节点", () => {
  const { game } = make();
  const idioms = ["心想事成", "成竹在胸", "胸有成竹", "竹报平安", "安居乐业", "业精于勤",
    "勤能补拙", "拙嘴笨舌", "舌战群儒", "儒雅风流", "流连忘返", "返老还童"];
  idioms.forEach((idiom, i) => game.chain.addTurn(i < 3 ? "bot" : "human", idiom, 2));
  expect(chainLines(game)).toEqual(idioms.map((idiom, i) => `${i + 1}. ${i < 3 ? "Bot" : "你"}：${idiom}（+2）`));
});

test("接龙链：步分始终带符号", () => {
  const { game } = make();
  // 负数与零是展示边界 fixture，不改变合法成语的计分规则。
  game.chain.addTurn("human", "心想事成", 4);
  game.chain.addTurn("bot", "成竹在胸", -1);
  game.chain.addTurn("human", "胸有成竹", 0);
  expect(chainLines(game)).toEqual(["1. 你：心想事成（+4）", "2. Bot：成竹在胸（-1）", "3. 你：胸有成竹（+0）"]);
});

test("接龙链：切换难度不重算历史步分", async () => {
  const { game } = make();
  game.setMode("easy");
  await game.submitHuman("心想事成");
  await game.submitBot("成竹在胸");
  game.setMode("normal");
  expect(chainLines(game)).toEqual(["1. 你：心想事成（+4）", "2. Bot：成竹在胸（+2）"]);
});

test("接龙链：纯展示不改动链或对局状态", async () => {
  const { game } = make();
  await game.submitHuman("心想事成");
  const snapshot = () => structuredClone({
    turns: game.chain.turns, scores: game.scores, roundLog: game.roundLog,
    currentRound: game.currentRound, lastChar: game.lastChar, mode: game.mode,
    awaitingBot: game.awaitingBot, pendingAttempts: game.pendingAttempts,
    gameOver: game.gameOver, secondsLeft: game.secondsLeft(),
  });
  const before = snapshot();
  const lines = chainLines(game);
  expect(chainLines(game)).toEqual(lines);
  expect(snapshot()).toEqual(before);
});


test("结算：完整历史含跳过、提示、超时和 Bot 放弃，读取不改变状态或历史分数", async () => {
  const { game, clock } = make();
  game.setRounds("4");
  await game.submitHuman("心想事成");
  await game.submitBot("成竹在胸");
  game.pass();
  game.forfeitBot("回合被中断");
  await game.submitHint("胸有成竹");
  await game.submitBot("竹报平安");
  clock.now += 31;
  await game.submitHuman("安居乐业");
  game.forfeitBot("模型调用出错");
  expect(game.gameOver).toBe(true);
  const expected = [
    "🏁 对局结束", "你 2 : 4 Bot · Bot 获胜。",
    "第 1 轮：你：心想事成（+2） / Bot：成竹在胸（+2）",
    "第 2 轮：你跳过本轮（-1） / Bot 放弃：回合被中断（本轮 0 分）",
    "第 3 轮：你：胸有成竹（+2，使用提示） / Bot：竹报平安（+2）",
    "第 4 轮：超时，按跳过计（-1） / Bot 放弃：模型调用出错（本轮 0 分）",
    "输入 /restart 再来一局，或 /rounds 加轮数继续。",
  ];
  expect(finalLines(game)).toEqual(expected);
  game.setMode("easy");
  const snapshot = () => structuredClone({ scores: game.scores, chain: game.chain.turns,
    log: game.roundLog, round: game.currentRound, hints: game.hintsRemaining,
    awaitingBot: game.awaitingBot, secondsLeft: game.secondsLeft() });
  const before = snapshot();
  expect(finalLines(game)).toEqual(expected);
  expect(finalLines(game)).toEqual(expected);
  expect(finalLines(game)).toHaveLength(game.roundLog.length + 3);
  expect(snapshot()).toEqual(before);
});

for (const forfeit of [false, true]) {
  test(`结算：${forfeit ? "人类胜出与无放弃原因" : "平局"}`, async () => {
    const { game } = make();
    game.setRounds("1");
    await game.submitHuman("心想事成");
    if (forfeit) {
      game.forfeitBot("test");
      // 仅用于展示边界：没有尝试记录的失败。
      game.roundLog[0]!.bot.attempts = [];
    } else await game.submitBot("成竹在胸");
    expect(finalLines(game)).toEqual([
      "🏁 对局结束",
      forfeit ? "你 2 : 0 Bot · 你赢了！🎉" : "你 2 : 2 Bot · 平局。",
      "第 1 轮：你：心想事成（+2） / " + (forfeit
        ? "Bot 放弃：没有给出合规成语（本轮 0 分）" : "Bot：成竹在胸（+2）"),
      "输入 /restart 再来一局，或 /rounds 加轮数继续。",
    ]);
  });
}


test("战绩卡片：空记录与胜负平、中文难度、负分、单小数胜率", () => {
  expect(recordsLines([])).toEqual(["还没有战绩"]);
  const base = { endedAt: "2026-01-01T00:00:00.000Z", rounds: 1 };
  expect(recordsLines([
    { ...base, id: "a", mode: "easy", scores: { human: 4, bot: 2 }, winner: "human" },
    { ...base, id: "b", mode: "normal", scores: { human: -1, bot: 2 }, winner: "bot" },
    { ...base, id: "c", mode: "extreme", scores: { human: 0, bot: 0 }, winner: "draw" },
  ])).toEqual([
    "总场次：3 · 胜 1 / 负 1 / 平 1", "胜率：33.3%", "最近 10 局：",
    "2026-01-01 · 简单 · 你 4 : 2 Bot · 胜",
    "2026-01-01 · 普通 · 你 -1 : 2 Bot · 负",
    "2026-01-01 · 极限 · 你 0 : 0 Bot · 平",
  ]);
});

test("战绩卡片：全量统计，只显示最近十局，排序不修改输入", () => {
  const records = [3, 1, 12, 2, 5, 11, 4, 10, 8, 7, 6, 9].map((day) => ({
    id: String(day), endedAt: `2026-01-${String(day).padStart(2, "0")}T00:00:00.000Z`,
    mode: "hard" as const, rounds: 1, scores: { human: 2, bot: 2 }, winner: "draw" as const,
  }));
  const before = structuredClone(records);
  const lines = recordsLines(records);
  expect(lines.slice(0, 3)).toEqual(["总场次：12 · 胜 0 / 负 0 / 平 12", "胜率：0.0%", "最近 10 局："]);
  expect(lines.slice(3)).toEqual(Array.from({ length: 10 }, (_, i) =>
    `2026-01-${String(12 - i).padStart(2, "0")} · 困难 · 你 2 : 2 Bot · 平`));
  expect(records).toEqual(before);
});
