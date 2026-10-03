import { expect, test } from "bun:test";
import { LLMError, parseJsonObject } from "../../src/engine/llm.ts";

test("解析纯 JSON 对象", () => {
  expect(parseJsonObject('{"is_idiom": true}')).toEqual({ is_idiom: true });
});

test("容忍 markdown 代码围栏与前后空白", () => {
  expect(parseJsonObject('\n```json\n{"candidates": ["心想事成"]}\n```\n')).toEqual({ candidates: ["心想事成"] });
});

test("空内容报 LLMError", () => {
  expect(() => parseJsonObject("  ")).toThrow(LLMError);
});

test("非法 JSON 报 LLMError", () => {
  expect(() => parseJsonObject("不是 json")).toThrow(LLMError);
});

test("顶层不是对象报 LLMError", () => {
  expect(() => parseJsonObject("[1, 2]")).toThrow(LLMError);
});
