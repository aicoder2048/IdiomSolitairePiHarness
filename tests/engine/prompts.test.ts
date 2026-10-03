import { expect, test } from "bun:test";
import type { ChatMessage } from "../../src/engine/llm.ts";
import {
  BOT_SYSTEM_PROMPT,
  buildHintMessages,
  buildRoundPrompt,
  buildVerifierMessages,
} from "../../src/engine/prompts.ts";

const allText = (messages: ChatMessage[]) => messages.map((m) => m.content).join("\n");

test("裁判 prompt 含候选词、词库档位与 json 约定", () => {
  const msgs = buildVerifierMessages("心想事成", "strict");
  const text = allText(msgs);
  expect(msgs[0]?.role).toBe("system");
  expect(text).toContain("心想事成");
  expect(text).toContain("strict");
  expect(text.toLowerCase()).toContain("json");
  expect(text).toContain("is_idiom");
});

test("lax 词库的说明提到俗语", () => {
  const text = allText(buildVerifierMessages("一见如故", "lax"));
  expect(text).toContain("lax");
  expect(text).toContain("俗语");
});

test("Bot 系统提示只描述角色与工具协议，不含具体接龙字", () => {
  expect(BOT_SYSTEM_PROMPT).toContain("submit_idiom");
  expect(BOT_SYSTEM_PROMPT).toContain("接龙");
});

test("回合 prompt 含接龙字、谐音约束与工具名", () => {
  const prompt = buildRoundPrompt("心", false, "strict", []);
  expect(prompt).toContain("「心」");
  expect(prompt).toContain("不允许谐音");
  expect(prompt).toContain("submit_idiom");
  expect(prompt).toContain("开局");
});

test("回合 prompt 允许谐音时的措辞", () => {
  const prompt = buildRoundPrompt("心", true, "lax", []);
  expect(prompt).toContain("允许谐音");
  expect(prompt).not.toContain("不允许谐音");
});

test("回合 prompt 带最近接龙链", () => {
  const prompt = buildRoundPrompt("胸", false, "strict", ["心想事成", "成竹在胸"]);
  expect(prompt).toContain("最近 2 个");
  expect(prompt).toContain("心想事成 → 成竹在胸");
});

test("提示 prompt 要 n 个候选并避开已用成语", () => {
  const text = allText(buildHintMessages("心", 3, ["心想事成"]));
  expect(text).toContain("3");
  expect(text).toContain("心想事成");
  expect(text).toContain("candidates");
});
