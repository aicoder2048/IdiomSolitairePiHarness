import { afterEach, beforeEach, expect, spyOn, test } from "bun:test";
import { stripTerminalSequences, visibleWidth } from "@earendil-works/pi-tui";
import type { ExtensionContext } from "@earendil-works/pi-coding-agent";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join } from "node:path";
import { readRecords } from "../../src/extension/records-store.ts";
import { IdiomGame } from "../../src/engine/game.ts";
import { statusLines } from "../../src/extension/view.ts";
import { BOT_SYSTEM_PROMPT, SUBMIT_TOOL } from "../../src/engine/prompts.ts";
import { createIdiomExtension } from "../../src/extension/index.ts";
import { FakeClock, FakeLLM, type ScriptItem } from "../fakes.ts";
import { fakeTheme, FakePi } from "./fake-pi.ts";

let pi: FakePi;
let llm: FakeLLM;
let clock: FakeClock;

async function setup(opts: { hints?: ScriptItem[]; judge?: (idiom: string) => boolean; mode?: ExtensionContext["mode"] } = {}) {
  await pi?.emit("session_shutdown");
  pi = new FakePi(opts.mode);
  llm = new FakeLLM({ hints: opts.hints, judge: opts.judge });
  clock = new FakeClock();
  createIdiomExtension({ llm, clock: clock.read })(pi.api);
  await pi.emit("session_start", { reason: "startup" });
}

let recordsDir: string;
let recordsPath: string;
let previousRecordsPath: string | undefined;
beforeEach(async () => {
  previousRecordsPath = process.env.IDIOM_RECORDS_FILE;
  recordsDir = mkdtempSync(join(tmpdir(), "idiom-extension-"));
  recordsPath = join(recordsDir, "nested", "records.json");
  process.env.IDIOM_RECORDS_FILE = recordsPath;
  await setup();
});
afterEach(async () => {
  try { await pi.emit("session_shutdown"); }
  finally {
    if (previousRecordsPath === undefined) delete process.env.IDIOM_RECORDS_FILE;
    else process.env.IDIOM_RECORDS_FILE = previousRecordsPath;
    rmSync(recordsDir, { recursive: true, force: true });
  }
});

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
    ["chain", ""],
    ["records", ""],
    ["help", ""],
  ] as const) {
    await pi.command(name, args);
  }
  expect(llm.calls).toEqual([]);
  expect(pi.userMessages).toEqual([]);
});

test("/pass 开新回合并把回合 prompt 发给 Bot", async () => {
  await pi.command("pass");
  expect(pi.userMessages).toHaveLength(1);
  expect(pi.userMessages[0]).toContain("「心」");
});

test("/hint 显示编号候选，输入编号才转 Bot", async () => {
  await setup({ hints: [{ candidates: ["心想事成", "心旷神怡"] }] });
  await pi.command("hint");
  expect(pi.cards().at(-1)![0]).toBe("1. 心想事成");
  expect(pi.userMessages).toEqual([]);
  expect((await pi.input("2")).text).toContain("「怡」");
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

for (const mode of [undefined, "rpc", "json", "print"] as const) {
  for (const hasUI of [true, false]) {
    test(`/status ${mode ?? "默认 fake"} hasUI=${hasUI} 保留卡片且 0 token`, async () => {
      await setup({ mode });
      pi.ctx.hasUI = hasUI;
      await pi.command("status");
      expect(pi.entries).toEqual([{
        customType: "idiom-card",
        data: { title: "📊 状态", lines: statusLines(new IdiomGame({ llm, clock: clock.read })) },
      }]);
      expect(pi.customCalls).toEqual([]);
      expect(llm.calls).toEqual([]);
      expect(pi.userMessages).toEqual([]);
    });
  }
}

test("TUI /status 只开居中浮层，原样显示状态，任意键关闭且 0 token", async () => {
  await setup({ mode: "tui" });
  let finished = false;
  const command = pi.command("status").then(() => { finished = true; });
  await flush();
  expect(pi.customCalls).toHaveLength(1);
  expect(pi.customCalls[0]!.options?.overlay).toBe(true);
  expect(pi.customCalls[0]!.completed).toBe(false);
  expect(finished).toBe(false);
  expect(pi.entries).toEqual([]);
  const panel = await hintPanel(0, 200);
  const options = hintOptions();
  expect(options).toMatchObject({ anchor: "center", margin: 1 });
  const text = panel.render(options.width as number).map(stripTerminalSequences).join("\n");
  for (const line of ["📊 状态", ...statusLines(new IdiomGame({ llm, clock: clock.read })), "按任意键关闭"]) {
    expect(text).toContain(line);
  }
  expect(options.visible!(30, 10)).toBe(true);
  expect(options.width as number).toBeLessThanOrEqual(30);
  for (const line of panel.render(options.width as number)) expect(visibleWidth(line)).toBeLessThanOrEqual(30);
  panel.handleInput!("x");
  await command;
  expect(finished).toBe(true);
  expect(pi.customCalls[0]!.completed).toBe(true);
  expect(pi.entries).toEqual([]);
  expect(llm.calls).toEqual([]);
  expect(pi.userMessages).toEqual([]);
});

test("TUI /status 可重复查看已完成回合，不累积卡片或模型调用", async () => {
  async function playRound() {
    await pi.command("rounds", "5");
    await pi.input("心想事成");
    await pi.submit("成竹在胸");
  }
  await playRound();
  await pi.command("status");
  const expected = pi.cards().at(-1)!;
  await setup({ mode: "tui" });
  await playRound();
  const entries = [...pi.entries];
  const calls = [...llm.calls];
  const messages = [...pi.userMessages];
  for (let i = 0; i < 2; i++) {
    const command = pi.command("status");
    await flush();
    expect(pi.customCalls).toHaveLength(i + 1);
    expect(pi.customCalls[i]!.options?.overlay).toBe(true);
    const panel = await hintPanel(i, 200);
    const text = panel.render(200).map(stripTerminalSequences).join("\n");
    for (const line of expected) expect(text).toContain(line);
    panel.handleInput!(i ? "\x1b" : "x");
    await command;
    expect(pi.customCalls[i]!.completed).toBe(true);
    expect(pi.entries).toEqual(entries);
    expect(llm.calls).toEqual(calls);
    expect(pi.userMessages).toEqual(messages);
  }
});

for (const failure of ["throw", "reject"] as const) {
  test(`TUI /status custom ${failure} 只通知，不写卡片或调用模型`, async () => {
    await setup({ mode: "tui" });
    const spy = failure === "throw" ? spyOn(pi.ctx.ui, "custom").mockImplementation(() => {
      throw new Error("UI unavailable");
    }) : undefined;
    try {
      const command = pi.command("status");
      await flush();
      if (failure === "reject") pi.customCalls[0]!.reject(new Error("UI unavailable"));
      await command;
      expect(pi.notices.at(-1)).toEqual({ message: "状态面板显示失败，请重新 /status。", type: "error" });
      expect(pi.entries).toEqual([]);
      expect(llm.calls).toEqual([]);
      expect(pi.userMessages).toEqual([]);
    } finally { spy?.mockRestore(); }
  });
}

test("TUI /help 与 /chain 仍写卡片，不调用 custom 或模型", async () => {
  await setup({ mode: "tui" });
  await pi.command("help");
  await pi.command("chain");
  expect(pi.entries.map((entry) => entry.data.title)).toEqual(["📖 成语接龙", "📜 接龙链"]);
  expect(pi.customCalls).toEqual([]);
  expect(llm.calls).toEqual([]);
  expect(pi.userMessages).toEqual([]);
});

test("最后一轮结束时追加终局卡片", async () => {
  await pi.command("rounds", "1");
  await pi.input("心想事成");
  await pi.submit("成竹在胸");
  expect(pi.cards().at(-1)![0]).toContain("对局结束");
});


test("/chain 空链只追加一张卡片，不调用模型或发送消息", async () => {
  await pi.command("chain");
  expect(pi.entries).toEqual([{
    customType: "idiom-card", data: { title: "📜 接龙链", lines: ["还没有成语"] },
  }]);
  expect(llm.calls).toEqual([]);
  expect(pi.userMessages).toEqual([]);
});

test("/chain 非空链逐行显示，查看不增加模型调用或消息", async () => {
  await pi.input("心想事成");
  await pi.submit("成竹在胸");
  const calls = llm.calls.length;
  const messages = [...pi.userMessages];
  const entries = pi.entries.length;
  await pi.command("chain");
  expect(pi.entries.slice(entries)).toEqual([{
    customType: "idiom-card",
    data: { title: "📜 接龙链", lines: ["1. 你：心想事成（+2）", "2. Bot：成竹在胸（+2）"] },
  }]);
  expect(llm.calls).toHaveLength(calls);
  expect(pi.userMessages).toEqual(messages);
});

test("/help 自动列出 /chain", async () => {
  await pi.command("help");
  expect(pi.cards().at(-1)!.join("\n")).toContain("/chain — 查看完整接龙链");
});

for (const command of ["undo", "restart"]) {
  test(`/chain 在 /${command} 后只显示当前链`, async () => {
    await pi.input("心想事成");
    await pi.submit("成竹在胸");
    await pi.command("chain");
    expect(pi.cards().at(-1)).toHaveLength(2);
    await pi.command(command);
    await pi.command("chain");
    expect(pi.cards().at(-1)).toEqual(["还没有成语"]);
  });
}

test("/chain 无 UI 时仍追加卡片，0 token 且不发送模型消息", async () => {
  Object.assign(pi.ctx, { hasUI: false });
  await pi.command("chain");
  expect(pi.entries).toEqual([{
    customType: "idiom-card", data: { title: "📜 接龙链", lines: ["还没有成语"] },
  }]);
  expect(llm.calls).toEqual([]);
  expect(pi.userMessages).toEqual([]);
});

const hintCandidates = ["心想事成", "心旷神怡"];

function hintOptions() {
  const options = pi.customCalls[0]!.options!.overlayOptions!;
  return typeof options === "function" ? options() : options;
}

async function hintPanel(index = 0, columns = 80) {
  const call = pi.customCalls[index]!;
  type Args = Parameters<typeof call.factory>;
  return await call.factory({
    terminal: { columns, rows: 30 }, requestRender() {},
  } as unknown as Args[0], fakeTheme, {} as Args[2], call.done);
}

async function flush() {
  for (let i = 0; i < 20; i++) await Promise.resolve();
}

test("TUI 提示捕获焦点并阻塞到确认，选第二个后 Bot 接怡", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  let finished = false;
  const command = pi.command("hint").then(() => { finished = true; });
  await flush();
  const panel = await hintPanel();
  expect(finished).toBe(false);
  expect(pi.userMessages).toEqual([]);
  expect(pi.entries).toEqual([]);
  expect(pi.customCalls[0]!.options!.overlay).toBe(true);
  expect(hintOptions().anchor).toBe("center");
  expect(hintOptions().nonCapturing).not.toBe(true);
  const width = hintOptions().width as number;
  expect(width).toBeGreaterThanOrEqual(40);
  expect(width).toBeLessThanOrEqual(48);
  const lines = panel.render(width);
  for (const line of lines) expect(visibleWidth(line)).toBe(width);
  expect(lines.map(stripTerminalSequences).join("\n")).toContain("剩余提示 2 次");
  panel.handleInput!("\x1b[B");
  panel.handleInput!("\r");
  await command;
  expect(pi.customCalls[0]!.completed).toBe(true);
  expect(pi.userMessages).toHaveLength(1);
  expect(pi.userMessages[0]).toContain("「怡」");
  expect(llm.roles()).toEqual(["hints", "judge"]);
  expect(pi.widgets.get("idiom-board")!.join("\n")).toContain("剩余提示 1 次");
  await pi.submit("怡然自得");
  expect(pi.cards()[0]).toContain("你：心旷神怡（+2，使用提示）");
});

test("TUI Esc 取消不扣次数、不启动 Bot", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  const command = pi.command("hint");
  await flush();
  (await hintPanel()).handleInput!("\x1b");
  await command;
  expect(llm.roles()).toEqual(["hints"]);
  expect(pi.userMessages).toEqual([]);
  expect(pi.widgets.get("idiom-board")!.join("\n")).toContain("剩余提示 2 次");
});

test("裁判拒绝后返回选择框，可重新选择，不重复调用提示模型", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }], judge: (idiom) => idiom !== hintCandidates[0] });
  const command = pi.command("hint");
  await flush();
  (await hintPanel()).handleInput!("\r");
  await flush();
  expect(pi.lastNotice()).toContain("查无此成语");
  expect(pi.userMessages).toEqual([]);
  expect(pi.customCalls).toHaveLength(2);
  const retry = await hintPanel(1);
  expect(retry.render(60).map(stripTerminalSequences).join("\n")).toContain("剩余提示 2 次");
  retry.handleInput!("2");
  retry.handleInput!("\r");
  await command;
  expect(pi.userMessages[0]).toContain("「怡」");
  expect(llm.roles()).toEqual(["hints", "judge", "judge"]);
});

for (const mode of ["rpc", "json", "print"] as const) {
  test(`${mode} 编号卡片，输入候选成语也扣次数并正常计分`, async () => {
    await setup({ mode, hints: [{ candidates: hintCandidates }] });
    await pi.command("hint");
    expect(pi.customCalls).toEqual([]);
    expect(pi.cards()).toEqual([["1. 心想事成", "2. 心旷神怡", "输入候选编号或直接输入成语", "剩余提示 2 次"]]);
    expect(pi.userMessages).toEqual([]);
    expect((await pi.input("心想事成")).text).toContain("「成」");
    expect(pi.widgets.get("idiom-board")!.join("\n")).toContain("剩余提示 1 次");
  });
}

test("非 TUI 无效编号与无效候选不扣次数，仍可另选", async () => {
  await setup({ hints: [{ candidates: hintCandidates }], judge: (idiom) => idiom !== hintCandidates[0] });
  await pi.command("hint");
  expect((await pi.input("9")).action).toBe("handled");
  expect(llm.roles()).toEqual(["hints"]);
  expect((await pi.input("1")).action).toBe("handled");
  expect((await pi.input("2")).text).toContain("「怡」");
});

test("无 UI 仍写编号卡片，restart 后旧编号不可用", async () => {
  await setup({ hints: [{ candidates: hintCandidates }] });
  Object.assign(pi.ctx, { hasUI: false });
  await pi.command("hint");
  expect(pi.cards()[0]).toContain("输入候选编号或直接输入成语");
  await pi.command("restart");
  expect((await pi.input("1")).action).toBe("handled");
  expect(llm.roles()).toEqual(["hints"]);
});

test("极限和用完提示时 /hint 为 0 token，状态和帮助显示新规则", async () => {
  await pi.command("difficulty", "extreme");
  await pi.command("hint");
  expect(pi.lastNotice()).toBe("本局提示次数已用完");
  expect(llm.calls).toEqual([]);
  await setup({ hints: [{ candidates: hintCandidates }] });
  await pi.command("difficulty", "hard");
  await pi.command("hint");
  await pi.input("1");
  await pi.submit("成竹在胸");
  const calls = llm.calls.length;
  await pi.command("hint");
  expect(pi.lastNotice()).toBe("本局提示次数已用完");
  expect(llm.calls.length).toBe(calls);
  await pi.command("status");
  expect(pi.cards().at(-1)!.join("\n")).toContain("剩余提示 0 次");
  await pi.command("help");
  expect(pi.cards().at(-1)!.join("\n")).toContain("简单 3 / 普通 2 / 困难 1 / 极限 0");
});

for (const [label, item] of [
  ["空候选", { candidates: [] }],
  ["无效候选", { candidates: ["一马当先", "心"] }],
  ["模型异常", new Error("offline failure")],
] as const) {
  test(`TUI /hint ${label} 不显示 overlay，不开回合`, async () => {
    await setup({ mode: "tui", hints: [item] });
    await pi.command("hint");
    expect(pi.lastNotice()).toContain("暂时没拿到可用的提示");
    expect(pi.customCalls).toEqual([]);
    expect(pi.userMessages).toEqual([]);
  });
}

for (const sync of [false, true]) {
  test(`overlay ${sync ? "同步" : "异步"}失败只通知，不自动替玩家选词`, async () => {
    await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
    const custom = sync ? spyOn(pi.ctx.ui, "custom").mockImplementation(() => { throw new Error("failed"); }) : undefined;
    try {
      const command = pi.command("hint");
      await flush();
      if (!sync) pi.customCalls[0]!.reject(new Error("failed"));
      await command;
      expect(pi.lastNotice()).toContain("提示面板显示失败");
      expect(pi.userMessages).toEqual([]);
      expect(llm.roles()).toEqual(["hints"]);
    } finally { custom?.mockRestore(); }
  });
}

test("resize 遵守 60% 上限，不隐藏捕获焦点的选择框", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  const command = pi.command("hint");
  await flush();
  const panel = await hintPanel();
  expect(hintOptions().visible!(30, 10)).toBe(true);
  expect(hintOptions().width).toBe(18);
  panel.handleInput!("\x1b");
  await command;
});

for (const late of [false, true]) {
  test(`session_shutdown 取消选择，延迟 factory=${late} 也不重开`, async () => {
    await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
    const command = pi.command("hint");
    await flush();
    if (!late) await hintPanel();
    await pi.emit("session_shutdown");
    if (late) await hintPanel();
    await command;
    expect(pi.customCalls[0]!.completed).toBe(true);
    expect(pi.userMessages).toEqual([]);
  });
}


test("选择框等待不暂停计时，超时确认按跳过且不扣提示", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  const command = pi.command("hint");
  await flush();
  const panel = await hintPanel();
  clock.now += 31;
  expect(pi.customCalls[0]!.completed).toBe(false);
  panel.handleInput!("2");
  panel.handleInput!("\r");
  await command;
  expect(pi.userMessages[0]).toContain("「心」");
  expect(pi.lastNotice()).toContain("超时");
  expect(pi.widgets.get("idiom-board")!.join("\n")).toContain("剩余提示 2 次");
  expect(llm.roles()).toEqual(["hints"]);
});

// ---------- 对局结算 ----------
const finalCards = () => pi.cards().filter((lines) => lines[0] === "🏁 对局结束");
const drawSummary = [
  "🏁 对局结束", "你 2 : 2 Bot · 平局。",
  "第 1 轮：你：心想事成（+2） / Bot：成竹在胸（+2）",
  "输入 /restart 再来一局，或 /rounds 加轮数继续。",
];

for (const mode of [undefined, "rpc", "json", "print"] as const) {
  test(`结算 ${mode ?? "默认 fake"}：无 UI 也写相同文字的卡片，不调 custom`, async () => {
    await setup({ mode });
    pi.ctx.hasUI = false;
    await pi.command("rounds", "1");
    await pi.input("心想事成");
    expect((await pi.submit("成竹在胸")).terminate).toBe(true);
    expect(pi.cards()).toHaveLength(2);
    expect(finalCards()).toEqual([drawSummary]);
    expect(pi.customCalls).toHaveLength(0);
  });
}

test("TUI 结算非阻塞、相同文字、任意键关闭且不增加模型消息或用量", async () => {
  await setup({ mode: "tui" });
  await pi.command("rounds", "1");
  await pi.input("心想事成");
  const result = await pi.submit("成竹在胸");
  expect(result.terminate).toBe(true);
  expect(result.content[0].text).not.toContain("🏁 对局结束");
  expect(pi.customCalls).toHaveLength(1);
  expect(pi.customCalls[0]!.options!.overlay).toBe(true);
  expect(pi.customCalls[0]!.completed).toBe(false);
  expect(pi.cards()).toHaveLength(1);
  expect(finalCards()).toEqual([]);
  const calls = llm.calls.length;
  expect(calls).toBe(2); // 只有人类与 Bot 的裁判调用
  const panel = await hintPanel(0, 120);
  const options = hintOptions();
  const contentWidth = Math.max(40, ...drawSummary.map((line) => visibleWidth(line) + 4));
  expect(options).toMatchObject({ anchor: "center", width: contentWidth, margin: 1 });
  expect(contentWidth).toBeLessThanOrEqual(72); // 120 列的 60%，不是铺满屏幕
  const text = panel.render(options.width as number).map(stripTerminalSequences).join("\n");
  for (const line of drawSummary) expect(text).toContain(line);
  expect(options.visible!(80, 30)).toBe(true);
  expect(options.width).toBe(Math.min(48, contentWidth));
  expect(options.visible!(200, 30)).toBe(true);
  expect(options.width).toBe(contentWidth);
  panel.handleInput!("x");
  await flush();
  expect(pi.customCalls[0]!.completed).toBe(true);
  expect(llm.calls).toHaveLength(calls);
  expect(pi.userMessages).toEqual([]);
  expect(finalCards()).toEqual([]);
});

for (const mode of ["tui", "rpc"] as const) {
  test(`${mode} 非末轮、失败尝试与第一次催促不显示结算`, async () => {
    await setup({ mode });
    await pi.command("rounds", "2");
    await pi.input("心想事成");
    await pi.submit("一马当先");
    await pi.settle();
    expect(finalCards()).toEqual([]);
    expect(pi.customCalls).toHaveLength(0);
    expect(existsSync(recordsPath)).toBe(false);
    await pi.submit("成竹在胸");
    expect(existsSync(recordsPath)).toBe(false);
    expect(finalCards()).toEqual([]);
    expect(pi.customCalls).toHaveLength(0);
  });

  for (const route of ["success", "retry", "no-tool", "aborted", "error", "settled"] as const) {
    test(`${mode} 末轮 ${route} 只结算一次，后续生命周期/提交/状态/输入不重复`, async () => {
      await setup({ mode });
      await pi.command("rounds", "1");
      await pi.input("心想事成");
      if (route === "success") await pi.submit("成竹在胸");
      else if (route === "retry") {
        for (let i = 0; i < 3; i++) await pi.submit("一马当先");
      } else if (route === "no-tool") {
        await pi.settle();
        expect(finalCards()).toHaveLength(0);
        expect(pi.customCalls).toHaveLength(0);
        await pi.settle();
      } else if (route === "settled") await pi.emit("agent_settled");
      else await pi.settle(route);
      const saved = readRecords();
      expect(saved).toHaveLength(1);
      expect(saved[0]).toMatchObject({ rounds: 1, scores: { human: 2, bot: route === "success" ? 2 : 0 },
        winner: route === "success" ? "draw" : "human" });
      let text: string;
      if (mode === "tui") {
        expect(pi.customCalls).toHaveLength(1);
        expect(pi.customCalls[0]!.options?.overlay).toBe(true);
        const panel = await hintPanel();
        text = panel.render(200).map(stripTerminalSequences).join("\n");
        panel.handleInput!("\r");
      } else {
        expect(finalCards()).toHaveLength(1);
        text = finalCards()[0]!.join("\n");
      }
      expect(text).toContain("第 1 轮：你：心想事成（+2）");
      if (route !== "success") {
        expect(text).toContain("Bot 放弃：");
        expect(text).toContain("（本轮 0 分）");
        const reason = { retry: "接不上", "no-tool": "没有调用 submit_idiom", aborted: "回合被中断",
          error: "模型调用出错", settled: "回合意外结束" }[route];
        expect(text).toContain(reason);
      }
      const calls = llm.calls.length;
      for (let i = 0; i < 2; i++) {
        await pi.settle();
        await pi.emit("agent_settled");
      }
      await pi.submit("成竹在胸");
      const status = pi.command("status");
      if (mode === "tui") {
        await flush();
        expect(pi.customCalls).toHaveLength(2);
        const panel = await hintPanel(1);
        const text = panel.render(200).map(stripTerminalSequences).join("\n");
        expect(text).toContain("📊 状态");
        expect(text).not.toContain("🏁 对局结束");
        panel.handleInput!("x");
      }
      await status;
      await pi.input("胸有成竹");
      expect(finalCards()).toHaveLength(mode === "rpc" ? 1 : 0);
      expect(readRecords()).toEqual(saved);
      expect(pi.customCalls).toHaveLength(mode === "tui" ? 2 : 0);
      expect(llm.calls).toHaveLength(calls);
      expect(pi.userMessages).toEqual([]);
    });
  }
}

for (const command of ["rounds", "restart", "undo"] as const) {
  test(`TUI /${command} 后的新终局仍显示结算`, async () => {
    await setup({ mode: "tui" });
    await pi.command("rounds", "1");
    await pi.input("心想事成");
    await pi.submit("成竹在胸");
    (await hintPanel()).handleInput!("x");
    await pi.command(command, command === "rounds" ? "2" : "");
    await pi.input(command === "rounds" ? "胸有成竹" : "心想事成");
    await pi.submit(command === "rounds" ? "竹报平安" : "成竹在胸");
    expect(pi.customCalls).toHaveLength(2);
    expect(finalCards()).toHaveLength(0);
    (await hintPanel(1)).handleInput!("x");
  });
}

for (const failure of ["throw", "reject"] as const) {
  test(`TUI custom ${failure} 回退一次卡片，不影响已结算工具结果`, async () => {
    await setup({ mode: "tui" });
    const spy = failure === "throw" ? spyOn(pi.ctx.ui, "custom").mockImplementation(() => {
      throw new Error("UI unavailable");
    }) : undefined;
    try {
      await pi.command("rounds", "1");
      await pi.input("心想事成");
      const result = await pi.submit("成竹在胸");
      if (failure === "reject") pi.customCalls[0]!.reject(new Error("UI unavailable"));
      await flush();
      expect(result.terminate).toBe(true);
      expect(finalCards()).toEqual([drawSummary]);
      await pi.settle();
      await pi.emit("agent_settled");
      expect(finalCards()).toEqual([drawSummary]);
      if (spy) expect(spy).toHaveBeenCalledTimes(1);
      else expect(pi.customCalls).toHaveLength(1);
      expect(llm.calls).toHaveLength(2);
      expect(pi.userMessages).toEqual([]);
    } finally { spy?.mockRestore(); }
  });
}


// ---------- 跨局战绩 ----------

async function finishDraw() {
  await pi.command("rounds", "1");
  await pi.input("心想事成");
  return pi.submit("成竹在胸");
}

test("终局立即保存完整战绩，无 UI 也保存，新 session 可查看", async () => {
  pi.ctx.hasUI = false;
  await pi.command("rounds", "1");
  await pi.input("心想事成");
  expect(existsSync(recordsPath)).toBe(false);
  expect((await pi.submit("成竹在胸")).terminate).toBe(true);
  const rows = readRecords();
  expect(rows).toHaveLength(1);
  expect(rows[0]).toMatchObject({ mode: "normal", rounds: 1, scores: { human: 2, bot: 2 }, winner: "draw" });
  expect(rows[0]!.id).toBeTruthy();
  expect(new Date(rows[0]!.endedAt).toISOString()).toBe(rows[0]!.endedAt);
  await setup();
  await pi.command("records");
  expect(pi.cards().at(-1)!.join("\n")).toContain("总场次：1 · 胜 0 / 负 0 / 平 1");
  await finishDraw();
  expect(readRecords()).toHaveLength(2);
  expect(readRecords()[1]!.id).not.toBe(rows[0]!.id);
});

test("undo 重打覆盖，失败和忙碌 restart 保留 id，成功 restart 新增一局", async () => {
  await finishDraw();
  const first = readRecords()[0]!;
  await pi.command("restart", "invalid");
  await pi.command("undo");
  expect(readRecords()).toEqual([first]);
  await pi.input("心想事成");
  await pi.command("restart", "天"); // 忙碌，不能更换 id
  await pi.settle("aborted");
  expect(readRecords()).toHaveLength(1);
  expect(readRecords()[0]).toMatchObject({ id: first.id, winner: "human", scores: { human: 2, bot: 0 } });
  const replaced = readRecords()[0]!;
  await pi.command("restart", "心");
  await finishDraw();
  expect(readRecords()).toHaveLength(2);
  expect(readRecords()[0]).toEqual(replaced);
  expect(readRecords()[1]!.id).not.toBe(first.id);
});

test("加轮继续后覆盖原 id；降低轮数结束空闲对局才保存，不额外开结算浮层", async () => {
  await finishDraw();
  const first = readRecords()[0]!;
  await pi.command("rounds", "2");
  expect(readRecords()).toEqual([first]);
  await pi.input("胸有成竹");
  await pi.submit("竹报平安");
  expect(readRecords()).toHaveLength(1);
  expect(readRecords()[0]).toMatchObject({ id: first.id, rounds: 2 });
  await setup({ mode: "tui" });
  await pi.command("rounds", "3");
  await pi.input("心想事成");
  await pi.submit("成竹在胸");
  await pi.command("rounds", "1");
  expect(readRecords()).toHaveLength(2);
  expect(readRecords()[1]!.rounds).toBe(1);
  expect(pi.customCalls).toEqual([]);
});

test("Bot 待提交时 /rounds 不能提前保存", async () => {
  await pi.input("心想事成");
  await pi.submit("成竹在胸");
  await pi.input("胸有成竹");
  await pi.command("rounds", "1");
  expect(existsSync(recordsPath)).toBe(false);
  await pi.submit("竹报平安");
  expect(readRecords()).toHaveLength(1);
  expect(readRecords()[0]!.rounds).toBe(2); // 待提交的实际末轮完成后才保存
});

for (const mode of ["tui", "rpc"] as const) {
  test(`${mode} /records 始终卡片，空历史/反复查看不改变状态、文件或模型用量`, async () => {
    await setup({ mode });
    await pi.command("records");
    expect(pi.entries.at(-1)!.data).toEqual({ title: "📚 战绩", lines: ["还没有战绩"] });
    expect(pi.customCalls).toEqual([]);
    expect(llm.calls).toEqual([]);
    expect(existsSync(recordsPath)).toBe(false);
    await finishDraw();
    const file = readFileSync(recordsPath, "utf8");
    const calls = [...llm.calls];
    const board = [...pi.widgets.get("idiom-board")!];
    const panels = pi.customCalls.length;
    for (let i = 0; i < 2; i++) await pi.command("records");
    expect(pi.cards().at(-1)!.join("\n")).toContain("普通 · 你 2 : 2 Bot · 平");
    expect(pi.customCalls).toHaveLength(panels);
    expect(pi.widgets.get("idiom-board")).toEqual(board);
    expect(readFileSync(recordsPath, "utf8")).toBe(file);
    expect(llm.calls).toEqual(calls);
    expect(pi.userMessages).toEqual([]);
  });
}

for (const failure of ["corrupt", "parent-file"] as const) {
  test(`战绩 ${failure} 读写警告但游戏继续，不覆盖坏文件`, async () => {
    if (failure === "corrupt") mkdirSync(dirname(recordsPath), { recursive: true });
    const broken = failure === "corrupt" ? recordsPath : dirname(recordsPath);
    writeFileSync(broken, "broken");
    await pi.command("records");
    expect(pi.notices.at(-1)?.type).toBe("warning");
    expect(pi.lastNotice()).toContain("战绩读取失败");
    expect(pi.cards()).toEqual([]);
    expect(llm.calls).toEqual([]);
    expect(pi.userMessages).toEqual([]);
    expect((await finishDraw()).terminate).toBe(true);
    expect(pi.notices.at(-1)?.type).toBe("warning");
    expect(pi.lastNotice()).toContain("战绩保存失败");
    expect(finalCards()).toHaveLength(1);
    expect(readFileSync(broken, "utf8")).toBe("broken");
    await pi.command("restart", "心");
    expect((await pi.input("心想事成")).action).toBe("transform");
    await pi.settle("aborted"); // 生命周期路径也不能抛出文件错误
    expect(readFileSync(broken, "utf8")).toBe("broken");
  });
}
