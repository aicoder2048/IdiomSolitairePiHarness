import { afterEach, beforeEach, expect, spyOn, test } from "bun:test";
import type { ExtensionContext } from "@earendil-works/pi-coding-agent";
import { BOT_SYSTEM_PROMPT, SUBMIT_TOOL } from "../../src/engine/prompts.ts";
import { createIdiomExtension } from "../../src/extension/index.ts";
import { FakeClock, FakeLLM, type ScriptItem } from "../fakes.ts";
import { fakeTheme, FakePi } from "./fake-pi.ts";

let pi: FakePi;
let llm: FakeLLM;

async function setup(opts: { hints?: ScriptItem[]; judge?: (idiom: string) => boolean; mode?: ExtensionContext["mode"] } = {}) {
  await pi?.emit("session_shutdown");
  pi = new FakePi(opts.mode);
  llm = new FakeLLM({ hints: opts.hints, judge: opts.judge });
  const clock = new FakeClock();
  createIdiomExtension({ llm, clock: clock.read })(pi.api);
  await pi.emit("session_start", { reason: "startup" });
}

beforeEach(() => setup());
afterEach(() => pi.emit("session_shutdown"));

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

async function hintPanel(done = pi.customCalls[0]!.done, documentRows = 30, mode = "regular") {
  const call = pi.customCalls[0]!;
  type Args = Parameters<typeof call.factory>;
  return await call.factory({
    terminal: { columns: 80, rows: 30 },
    mode,
    children: [
      { render: () => Array(documentRows).fill("chat") },
      { render: () => Array(8).fill("board/editor/footer") },
    ],
  } as unknown as Args[0], fakeTheme, {
    matches: (data: string) => data === "\r",
  } as unknown as Args[2], done);
}

test("TUI /hint 居中非抢焦点面板，输入前已启动 Bot，普通按键不关闭", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  await pi.command("hint");
  const panel = await hintPanel();
  expect(pi.customCalls).toHaveLength(1);
  expect(pi.customCalls[0]!.options!.overlay).toBe(true);
  expect(hintOptions()).toMatchObject({ anchor: "center", width: 28, nonCapturing: true, margin: 1, maxHeight: "50%" });
  expect(pi.customCalls[0]!.completed).toBe(false);
  expect(pi.entries).toEqual([]);
  expect(llm.roles()).toEqual(["hints"]);
  expect(pi.userMessages).toHaveLength(1);
  expect(panel.render(28).join("\n")).toContain("1. 心想事成");
  expect(panel.handleInput).toBeUndefined();
  expect(pi.terminalInput("x")).toEqual([undefined]);
  expect(pi.customCalls[0]!.completed).toBe(false);
  await pi.input("心想事成", "extension");
  expect(pi.customCalls[0]!.completed).toBe(false);
  const board = pi.widgets.get("idiom-board");
  await pi.input("心想事成");
  expect(pi.customCalls[0]!.completed).toBe(true);
  expect(pi.widgets.get("idiom-board")).toEqual(board);
  expect(llm.roles()).toEqual(["hints"]);
  expect(pi.userMessages).toHaveLength(1);
  expect(pi.terminalListeners.size).toBe(0);
});

for (const name of ["hint", "pass", "undo", "difficulty", "rounds", "timer", "restart", "status", "chain", "help"]) {
  test(`/${name} 关闭已有提示面板`, async () => {
    await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
    await pi.command("hint");
    await hintPanel();
    const calls = llm.calls.length;
    await pi.command(name);
    expect(pi.customCalls[0]!.completed).toBe(true);
    expect(llm.calls).toHaveLength(calls);
  });
}

test("原生命令的提交键也关闭面板，不吞按键", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  await pi.command("hint");
  await hintPanel();
  expect(pi.terminalInput("\r")).toEqual([undefined]);
  expect(pi.customCalls[0]!.completed).toBe(true);
});

test("30 秒后通过 done 关闭，关闭异常不影响后续输入", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  const timer = spyOn(globalThis, "setTimeout");
  try {
    await pi.command("hint");
    let closed = 0;
    await hintPanel(() => { closed++; throw new Error("close failed"); });
    const expiry = timer.mock.calls.find((call) => call[1] === 30_000)!;
    expect(expiry).toBeDefined();
    expect(() => (expiry[0] as () => void)()).not.toThrow();
    expect(closed).toBe(1);
    expect((await pi.input("心想事成")).action).toBe("handled");
    expect(closed).toBe(1);
    expect(pi.userMessages).toHaveLength(1);
    expect(pi.terminalListeners.size).toBe(0);
  } finally { timer.mockRestore(); }
});

test("终端缩小时遵守 60% 上限，空间不足不遮挡仪表盘/输入框", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  await pi.command("hint");
  await hintPanel();
  const options = hintOptions();
  expect(options.visible!(80, 30)).toBe(true);
  expect(options.visible!(30, 30)).toBe(true);
  expect(options.width).toBe(18);
  expect(options.visible!(80, 20)).toBe(true);
  const height = 6;
  const row = 1 + Math.floor((20 - 2 - height) / 2) + options.offsetY!;
  expect(row + height).toBeLessThan(20 - 8);
  expect(options.visible!(80, 10)).toBe(false);
});

for (const mode of ["rpc", "json", "print"] as const) {
  test(`${mode} /hint 保留原卡片`, async () => {
    await setup({ mode, hints: [{ candidates: hintCandidates }] });
    await pi.command("hint");
    expect(pi.customCalls).toEqual([]);
    expect(pi.entries).toEqual([{
      customType: "idiom-card",
      data: { title: undefined, lines: ["提示：心想事成、心旷神怡", "你使用了提示（本轮 0 分）"] },
    }]);
    expect(llm.roles()).toEqual(["hints"]);
    expect(pi.userMessages).toHaveLength(1);
  });
}

test("无 UI 的 /hint 仍写原卡片", async () => {
  await setup({ hints: [{ candidates: hintCandidates }] });
  Object.assign(pi.ctx, { hasUI: false });
  await pi.command("hint");
  expect(pi.customCalls).toEqual([]);
  expect(pi.cards()).toEqual([["提示：心想事成、心旷神怡", "你使用了提示（本轮 0 分）"]]);
  expect(llm.roles()).toEqual(["hints"]);
  expect(pi.userMessages).toHaveLength(1);
});

test("提示 overlay 未关闭时照常挡住人类和重复提示，Bot 结算且人类 0 分", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  await pi.command("hint");
  await hintPanel();
  expect((await pi.input("心想事成")).action).toBe("handled");
  expect(pi.lastNotice()).toContain("Bot 正在接龙");
  await pi.command("hint");
  expect(pi.lastNotice()).toContain("Bot 正在接龙");
  expect(llm.roles()).toEqual(["hints"]);
  expect(pi.customCalls).toHaveLength(1);
  expect(pi.customCalls[0]!.completed).toBe(true);
  expect((await pi.submit("心想事成")).terminate).toBe(true);
  expect(pi.cards()[0]).toContain("你使用了提示（本轮 0 分）");
  expect(pi.cards()[0]).toContain("Bot：心想事成（+2）");
  expect(pi.widgets.get("idiom-board")?.[1]).toContain("你 0 : 2 Bot");
  const board = pi.widgets.get("idiom-board");
  await pi.input("", "extension");
  expect(pi.widgets.get("idiom-board")).toEqual(board);
  expect(pi.cards()).toHaveLength(1);
  expect(pi.userMessages).toHaveLength(1);
  expect(llm.roles()).toEqual(["hints", "judge"]);
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
    expect(pi.entries).toEqual([]);
    expect(pi.userMessages).toEqual([]);
    expect(llm.roles()).toEqual(["hints"]);
  });
}

test("overlay 展示失败只通知，不阻塞或重复启动 Bot", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  await pi.command("hint");
  pi.customCalls[0]!.reject(new Error("offline failure"));
  await Promise.resolve();
  expect(pi.lastNotice()).toContain("提示面板显示失败");
  expect(pi.notices.at(-1)?.type).toBe("error");
  expect(llm.roles()).toEqual(["hints"]);
  expect(pi.userMessages).toHaveLength(1);
});

for (const mode of ["regular", "fullscreen"]) {
  test(`${mode} 短对话也不能遮挡底部控件`, async () => {
    await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
    await pi.command("hint");
    await hintPanel(undefined, 4, mode);
    expect(hintOptions().visible!(80, 30)).toBe(mode === "fullscreen");
  });
}

test("custom 同步抛错也不阻止 Bot 开回合", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  const custom = spyOn(pi.ctx.ui, "custom").mockImplementation(() => { throw new Error("display failed"); });
  try {
    await pi.command("hint");
    expect(pi.lastNotice()).toContain("提示面板显示失败");
    expect(pi.userMessages).toHaveLength(1);
    expect((await pi.submit("心想事成")).terminate).toBe(true);
  } finally { custom.mockRestore(); }
});

test("factory 延迟执行时已关闭的面板不重开，也不再安装键盘监听", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  await pi.command("hint");
  await pi.command("status");
  await hintPanel();
  expect(pi.customCalls[0]!.completed).toBe(true);
  expect(hintOptions().visible!(80, 30)).toBe(false);
  expect(pi.terminalListeners.size).toBe(0);
});

test("session_shutdown 通过 done 关闭面板并移除监听", async () => {
  await setup({ mode: "tui", hints: [{ candidates: hintCandidates }] });
  await pi.command("hint");
  await hintPanel();
  await pi.emit("session_shutdown");
  expect(pi.customCalls[0]!.completed).toBe(true);
  expect(pi.terminalListeners.size).toBe(0);
});
