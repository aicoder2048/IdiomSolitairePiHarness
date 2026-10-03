import { expect, test } from "bun:test";
import { IdiomGame, type GameOptions, type Outcome, type BotSubmitResult } from "../../src/engine/game.ts";
import { FakeClock, FakeLLM, type ScriptItem } from "../fakes.ts";

function make(
  opts: { hints?: ScriptItem[]; judge?: (idiom: string) => boolean } & Omit<GameOptions, "llm" | "clock"> = {},
) {
  const { hints, judge, ...rest } = opts;
  const llm = new FakeLLM({ hints, judge });
  const clock = new FakeClock();
  const game = new IdiomGame({ llm, clock: clock.read, ...rest });
  return { game, llm, clock };
}

function expectKind<K extends Outcome["kind"]>(out: Outcome, kind: K): Extract<Outcome, { kind: K }> {
  expect(out.kind).toBe(kind);
  return out as Extract<Outcome, { kind: K }>;
}

function expectRound(res: BotSubmitResult): Extract<BotSubmitResult, { kind: "round" }> {
  expect(res.kind).toBe("round");
  return res as Extract<BotSubmitResult, { kind: "round" }>;
}

// ---------- 正常回合：人类入账 → Bot 提交 → 结算 ----------

test("合法回合双方得分，轮次推进", async () => {
  const { game } = make();
  const started = expectKind(await game.submitHuman("心想事成"), "bot_turn");
  expect(started.human.idiom).toBe("心想事成");
  expect(game.awaitingBot).toBe(true);
  expect(game.scores).toEqual({ human: 2, bot: 0 });

  const done = expectRound(await game.submitBot("成竹在胸"));
  expect(game.scores).toEqual({ human: 2, bot: 2 });
  expect(game.lastChar).toBe("胸");
  expect(game.currentRound).toBe(2);
  expect(game.awaitingBot).toBe(false);
  expect([done.record.human.idiom, done.record.bot.idiom]).toEqual(["心想事成", "成竹在胸"]);
});

test("交给 Bot 的回合 prompt 含接龙字与最新的接龙链", async () => {
  const { game } = make();
  const started = expectKind(await game.submitHuman("心想事成"), "bot_turn");
  expect(started.prompt).toContain("「成」");
  expect(started.prompt).toContain("心想事成");
});

test("简单模式人类得分翻倍", async () => {
  const { game } = make();
  game.setMode("easy");
  await game.submitHuman("心想事成");
  await game.submitBot("成竹在胸");
  expect(game.scores).toEqual({ human: 4, bot: 2 });
});

test("普通模式允许人类谐音", async () => {
  const { game } = make();
  expectKind(await game.submitHuman("新官上任"), "bot_turn");
  expect(game.scores.human).toBe(1);
});

test("困难模式拒绝人类谐音", async () => {
  const { game } = make();
  game.setMode("hard");
  const out = expectKind(await game.submitHuman("新官上任"), "invalid");
  expect(out.message).toContain("谐音");
});

test("无效作答不推进、不唤起 Bot", async () => {
  const { game } = make({ judge: () => false });
  expectKind(await game.submitHuman("心花乱飞"), "invalid");
  expect([game.currentRound, game.scores, game.lastChar, game.awaitingBot]).toEqual([
    1,
    { human: 0, bot: 0 },
    "心",
    false,
  ]);
});

test("Bot 思考期间人类输入被挡回，不调用裁判", async () => {
  const { game, llm } = make();
  await game.submitHuman("心想事成");
  const calls = llm.calls.length;
  expectKind(await game.submitHuman("成竹在胸"), "busy");
  expect(llm.calls.length).toBe(calls);
});

test("达到总轮数后对局结束", async () => {
  const { game } = make({ maxRounds: 1 });
  await game.submitHuman("心想事成");
  const done = expectRound(await game.submitBot("成竹在胸"));
  expect(done.gameOver).toBe(true);
  expect(game.gameOver).toBe(true);
  expectKind(await game.submitHuman("胸有成竹"), "info");
});

test("空输入是 noop", async () => {
  const { game } = make();
  expectKind(await game.submitHuman("   "), "noop");
});

// ---------- Bot 的思考循环：每次 submit_idiom 都是一次尝试，受预算约束 ----------

test("Bot 首次提交即通过：人类一次裁判 + Bot 一次裁判", async () => {
  const { game, llm } = make();
  await game.submitHuman("心想事成");
  const done = expectRound(await game.submitBot("成竹在胸"));
  expect(done.record.bot.attempts.length).toBe(1);
  expect(llm.roles()).toEqual(["judge", "judge"]);
});

test("无效候选被拒，Observation 带候选与原因，剩余次数减一", async () => {
  const { game } = make();
  await game.submitHuman("心想事成");
  const rejected = await game.submitBot("一马当先");
  expect(rejected.kind).toBe("rejected");
  if (rejected.kind !== "rejected") return;
  expect(rejected.observation).toContain("一马当先");
  expect(rejected.observation).toContain("接不上");
  expect(rejected.attemptsLeft).toBe(2);

  const done = expectRound(await game.submitBot("成竹在胸"));
  expect(done.record.bot.status).toBe("success");
  expect(done.record.bot.attempts.length).toBe(2);
});

test("规则不过的候选不触发裁判调用", async () => {
  const { game, llm } = make();
  game.pass();
  await game.submitBot("一马当先");
  await game.submitBot("心想事成");
  expect(llm.roles()).toEqual(["judge"]);
});

test("本局用过的成语被拒", async () => {
  const { game } = make();
  await game.submitHuman("心想事成");
  const rejected = await game.submitBot("心想事成");
  expect(rejected.kind === "rejected" && rejected.observation).toContain("用过");
});

test("预算用尽 Bot 放弃，末字保持人类的", async () => {
  const { game } = make({ botMaxRetries: 3 });
  await game.submitHuman("心想事成");
  await game.submitBot("一二三四");
  await game.submitBot("五六七八");
  const done = expectRound(await game.submitBot("九十百千"));
  expect([done.record.bot.status, done.record.bot.idiom, done.record.bot.attempts.length]).toEqual(["failed", "", 3]);
  expect(game.scores).toEqual({ human: 2, bot: 0 });
  expect(game.lastChar).toBe("成");
});

test("Bot 没有提交就结束时按放弃结算", async () => {
  const { game } = make();
  await game.submitHuman("心想事成");
  const done = expectRound(game.forfeitBot("没有调用 submit_idiom"));
  expect(done.record.bot.status).toBe("failed");
  expect(done.record.bot.attempts.at(-1)?.reason).toContain("submit_idiom");
  expect(game.currentRound).toBe(2);
});

test("Bot 候选先规范化", async () => {
  const { game } = make();
  await game.submitHuman("心想事成");
  const done = expectRound(await game.submitBot(" 成竹在胸。"));
  expect(done.record.bot.idiom).toBe("成竹在胸");
});

test("没有待接的 Bot 回合时提交是 stale", async () => {
  const { game } = make();
  expect((await game.submitBot("心想事成")).kind).toBe("stale");
  expect(game.forfeitBot("x").kind).toBe("stale");
});

// ---------- 命令（0 token）----------

test("确定性命令不调用模型", async () => {
  const { game, llm } = make();
  game.setMode("hard");
  game.setRounds("5");
  game.setTimer("60");
  game.undo();
  game.restart("天");
  expect(llm.calls).toEqual([]);
});

test("未知难度报错且不改模式", () => {
  const { game } = make();
  expectKind(game.setMode("insane"), "error");
  expect(game.mode).toBe("normal");
});

test("难度参数不分大小写", () => {
  const { game } = make();
  game.setMode("Hard");
  expect(game.mode).toBe("hard");
});

test("跳过扣 1 分并转 Bot", async () => {
  const { game } = make();
  const started = expectKind(game.pass(), "bot_turn");
  expect(started.human.kind).toBe("pass");
  await game.submitBot("心想事成");
  expect(game.scores).toEqual({ human: -1, bot: 2 });
  expect([game.lastChar, game.currentRound]).toEqual(["成", 2]);
});

test("提示给出候选、本轮 0 分并转 Bot", async () => {
  const { game } = make({ hints: [{ candidates: ["心想事成", "心旷神怡"] }] });
  const started = expectKind(await game.hint(), "bot_turn");
  expect(started.hints).toEqual(["心想事成", "心旷神怡"]);
  expect(started.human.kind).toBe("hint");
  await game.submitBot("心花怒放");
  expect(game.scores).toEqual({ human: 0, bot: 2 });
});

test("拿不到提示不消耗本轮", async () => {
  const { game } = make({ hints: [{ candidates: [] }] });
  expectKind(await game.hint(), "error");
  expect([game.currentRound, game.awaitingBot]).toEqual([1, false]);
});

test("提示经规则过滤：只留原字开头、未用过、去重", async () => {
  const { game } = make({
    hints: [{ candidates: ["心想事成", "心想事成", "一马当先", "心花怒放", "心旷神怡", "心平气和"] }],
  });
  game.pass();
  await game.submitBot("心花怒放");
  expect(await game.suggestHints("心", 3)).toEqual(["心想事成", "心旷神怡", "心平气和"]);
});

test("提示模型出错时返回空列表", async () => {
  const { game } = make({ hints: [new Error("down")] });
  expect(await game.suggestHints("心")).toEqual([]);
});

test("Bot 思考期间改状态的命令被挡回", async () => {
  const { game } = make();
  await game.submitHuman("心想事成");
  for (const out of [game.undo(), game.restart(), game.setMode("hard"), game.pass(), await game.hint()]) {
    expect(out.kind).toBe("busy");
  }
});

test("/rounds 校验参数", () => {
  const { game } = make();
  expectKind(game.setRounds("5"), "command");
  expect(game.maxRounds).toBe(5);
  expectKind(game.setRounds("abc"), "error");
  expectKind(game.setRounds("0"), "error");
});

test("调大轮数可恢复已结束的对局", async () => {
  const { game } = make({ maxRounds: 1 });
  await game.submitHuman("心想事成");
  await game.submitBot("成竹在胸");
  game.setRounds("3");
  expect(game.gameOver).toBe(false);
});

// ---------- /undo 与 /restart ----------

test("悔棋整轮回滚，撤销后同一成语可再用", async () => {
  const { game } = make();
  await game.submitHuman("心想事成");
  await game.submitBot("成竹在胸");
  expectKind(game.undo(), "command");
  expect([game.currentRound, game.scores, game.lastChar]).toEqual([1, { human: 0, bot: 0 }, "心"]);
  expect([game.chain.turns, game.roundLog]).toEqual([[], []]);
  expectKind(await game.submitHuman("心想事成"), "bot_turn");
});

test("没有回合可撤销", () => {
  const { game } = make();
  expectKind(game.undo(), "error");
});

test("悔棋可恢复已结束的对局", async () => {
  const { game } = make({ maxRounds: 1 });
  await game.submitHuman("心想事成");
  await game.submitBot("成竹在胸");
  game.undo();
  expect(game.gameOver).toBe(false);
});

test("重新开局清空状态但保留设置", async () => {
  const { game } = make();
  game.setMode("hard");
  await game.submitHuman("心想事成");
  await game.submitBot("成竹在胸");
  game.restart("天");
  expect([game.currentRound, game.scores, game.lastChar, game.mode]).toEqual([1, { human: 0, bot: 0 }, "天", "hard"]);
  expect(game.chain.turns).toEqual([]);
});

test("重新开局拒绝非单个汉字的首字", () => {
  const { game } = make();
  expectKind(game.restart("ab"), "error");
});

// ---------- 倒计时熔断 ----------

test("超时按跳过处理", async () => {
  const { game, clock } = make({ timerSeconds: 30 });
  clock.now += 31;
  const started = expectKind(await game.submitHuman("心花怒放"), "bot_turn");
  expect(started.human.kind).toBe("timeout");
  expect(game.scores.human).toBe(-1);
});

test("时限内作答正常", async () => {
  const { game, clock } = make({ timerSeconds: 30 });
  clock.now += 29;
  expect(expectKind(await game.submitHuman("心想事成"), "bot_turn").human.kind).toBe("idiom");
});

test("每轮结算后重置倒计时", async () => {
  const { game, clock } = make({ timerSeconds: 30 });
  clock.now += 20;
  await game.submitHuman("心想事成");
  await game.submitBot("成竹在胸");
  clock.now += 20;
  expect(expectKind(await game.submitHuman("胸有成竹"), "bot_turn").human.kind).toBe("idiom");
});

test("倒计时为 0 时关闭", async () => {
  const { game, clock } = make();
  game.setTimer("0");
  clock.now += 9999;
  expect(expectKind(await game.submitHuman("心想事成"), "bot_turn").human.kind).toBe("idiom");
  expect(game.secondsLeft()).toBeNull();
});

test("剩余秒数", () => {
  const { game, clock } = make({ timerSeconds: 30 });
  clock.now += 12;
  expect(game.secondsLeft()).toBe(18);
});

test("胜负判定", async () => {
  const { game } = make();
  expect(game.winner()).toBe("draw");
  await game.submitHuman("心想事成");
  expect(game.winner()).toBe("human");
});
