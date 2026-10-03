import { beforeEach, expect, test } from "bun:test";
import { BOT_SYSTEM_PROMPT, SUBMIT_TOOL } from "../../src/engine/prompts.ts";
import { createIdiomExtension } from "../../src/extension/index.ts";
import { FakeClock, FakeLLM, type ScriptItem } from "../fakes.ts";
import { FakePi } from "./fake-pi.ts";

let pi: FakePi;
let llm: FakeLLM;

async function setup(opts: { hints?: ScriptItem[]; judge?: (idiom: string) => boolean } = {}) {
  pi = new FakePi();
  llm = new FakeLLM(opts);
  const clock = new FakeClock();
  createIdiomExtension({ llm, clock: clock.read })(pi.api);
  await pi.emit("session_start", { reason: "startup" });
}

beforeEach(() => setup());

// ---------- 启动 ----------

test("启动时只激活 submit_idiom，并画出仪表盘", () => {
  expect(pi.activeTools).toEqual([SUBMIT_TOOL]);
  expect(pi.widgets.get("idiom-board")?.[1]).toContain("请接「心」");
});

// ---------- Harness：input 拦截 ----------

test("合法作答被改写成回合 prompt 交给 Bot", async () => {
  const res = await pi.input("心想事成");
  expect(res.action).toBe("transform");
  expect(res.text).toContain("「成」");
  expect(pi.lastNotice()).toContain("心想事成");
});

test("无效作答被挡下，不启动 Bot", async () => {
  await setup({ judge: () => false });
  const res = await pi.input("心花乱飞");
  expect(res.action).toBe("handled");
  expect(pi.notices.at(-1)?.type).toBe("warning");
});

test("扩展自己发出的消息直接放行", async () => {
  expect((await pi.input("[接龙字] 「心」", "extension")).action).toBe("continue");
});

test("未知斜杠命令不进模型", async () => {
  expect((await pi.input("/fly")).action).toBe("handled");
  expect(llm.calls).toEqual([]);
});

test("Bot 思考期间的输入被挡回", async () => {
  await pi.input("心想事成");
  expect((await pi.input("成竹在胸")).action).toBe("handled");
  expect(pi.lastNotice()).toContain("Bot 正在接龙");
});

// ---------- Prompt 与 Context ----------

test("每次 agent 启动都换成 Bot 的系统提示", async () => {
  const systemPromptOptions: { customPrompt?: string } = {};
  await pi.emit("before_agent_start", { prompt: "x", systemPromptOptions });
  expect(systemPromptOptions.customPrompt).toBe(BOT_SYSTEM_PROMPT);
});

test("context 只保留本回合的消息", async () => {
  const messages = [
    { role: "user", content: "第 1 轮" },
    { role: "assistant", content: [] },
    { role: "toolResult", content: "候选无效" },
    { role: "user", content: "第 2 轮" },
    { role: "assistant", content: [] },
  ];
  const res = (await pi.emit("context", { messages })) as { messages: unknown[] };
  expect(res.messages).toEqual(messages.slice(3));
});

// ---------- Loop：submit_idiom ----------

test("无效候选返回错误结果，不结束本轮", async () => {
  await pi.input("心想事成");
  const res = await pi.submit("一马当先");
  expect(res.isError).toBe(true);
  expect(res.terminate).toBeUndefined();
  expect(res.content[0].text).toContain("接不上");
});

test("合规候选结算本轮、terminate，并留下回合卡片", async () => {
  await pi.input("心想事成");
  await pi.submit("一马当先");
  const res = await pi.submit("成竹在胸");
  expect(res.terminate).toBe(true);
  expect(res.content[0].text).toContain("通过");
  const card = pi.cards().at(-1)!;
  expect(card.join("\n")).toContain("Bot：成竹在胸");
  expect(card.join("\n")).toContain("✗ 一马当先");
  expect(pi.widgets.get("idiom-board")?.[1]).toContain("请接「胸」");
});

test("本轮结算后再提交是 stale，也要求停止", async () => {
  await pi.input("心想事成");
  await pi.submit("成竹在胸");
  const res = await pi.submit("胸有成竹");
  expect(res.terminate).toBe(true);
  expect(res.content[0].text).toContain("不计");
});

test("Bot 不调工具就想结束：先催一次，再不交判放弃", async () => {
  await pi.input("心想事成");
  const first = await pi.settle();
  expect(first.continue).toBe(true);
  expect(first.entries[0].customType).toBe("idiom-nudge");

  expect(await pi.settle()).toBeUndefined();
  expect(pi.cards().at(-1)!.join("\n")).toContain("Bot 放弃");
});

test("被中断的 Bot 回合直接判放弃", async () => {
  await pi.input("心想事成");
  await pi.settle("aborted");
  expect(pi.cards().at(-1)!.join("\n")).toContain("回合被中断");
  expect((await pi.input("成竹在胸")).action).toBe("transform");
});

test("agent_settled 兜底：仍在等 Bot 就判放弃", async () => {
  await pi.input("心想事成");
  await pi.emit("agent_settled");
  expect(pi.cards().at(-1)!.join("\n")).toContain("Bot 放弃");
});

test("非 Bot 回合时 settle 不做任何事", async () => {
  expect(await pi.settle()).toBeUndefined();
  expect(pi.cards()).toEqual([]);
});

// ---------- 斜杠命令（给人用）----------

test("确定性命令 0 token", async () => {
  for (const [name, args] of [
    ["difficulty", "hard"],
    ["rounds", "5"],
    ["timer", "60"],
    ["undo", ""],
    ["restart", "天"],
    ["status", ""],
    ["help", ""],
  ] as const) {
    await pi.command(name, args);
  }
  expect(llm.calls).toEqual([]);
});

test("/pass 开新回合并把回合 prompt 发给 Bot", async () => {
  await pi.command("pass");
  expect(pi.userMessages).toHaveLength(1);
  expect(pi.userMessages[0]).toContain("「心」");
});

test("/hint 显示候选并转 Bot", async () => {
  await setup({ hints: [{ candidates: ["心想事成", "心旷神怡"] }] });
  await pi.command("hint");
  expect(pi.cards().at(-1)![0]).toBe("提示：心想事成、心旷神怡");
  expect(pi.userMessages).toHaveLength(1);
});

test("/difficulty 的参数补全", () => {
  const complete = pi.commands.get("difficulty").getArgumentCompletions;
  expect(complete("e").map((i: { value: string }) => i.value)).toEqual(["easy", "extreme"]);
});

test("/status 与 /help 写成卡片，不发给模型", async () => {
  await pi.command("status");
  await pi.command("help");
  expect(pi.entries.map((e) => e.data.title)).toEqual(["📊 状态", "📖 成语接龙"]);
  expect(pi.userMessages).toEqual([]);
});

test("最后一轮结束时追加终局卡片", async () => {
  await pi.command("rounds", "1");
  await pi.input("心想事成");
  await pi.submit("成竹在胸");
  expect(pi.cards().at(-1)![0]).toContain("对局结束");
});
