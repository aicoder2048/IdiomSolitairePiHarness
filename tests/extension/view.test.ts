import { expect, test } from "bun:test";
import { IdiomGame } from "../../src/engine/game.ts";
import { boardLines, helpLines, statusLines } from "../../src/extension/view.ts";
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
  for (const name of ["/hint", "/pass", "/undo", "/difficulty", "/rounds", "/timer", "/restart", "/status"]) {
    expect(text).toContain(name);
  }
});
