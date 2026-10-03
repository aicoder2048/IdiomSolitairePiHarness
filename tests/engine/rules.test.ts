import { expect, test } from "bun:test";
import { checkRules, isHomophone, normalizeIdiom } from "../../src/engine/rules.ts";

const none = new Set<string>();

test("原字接龙得 2 分", () => {
  const r = checkRules("心", "心想事成", false, none);
  expect([r.ok, r.score, r.match]).toEqual([true, 2, "exact"]);
});

test("允许谐音时谐音接龙得 1 分", () => {
  const r = checkRules("心", "新官上任", true, none);
  expect([r.ok, r.score, r.match]).toEqual([true, 1, "homophone"]);
});

test("不允许谐音时谐音被拒", () => {
  const r = checkRules("心", "新官上任", false, none);
  expect([r.ok, r.score]).toEqual([false, 0]);
  expect(r.reason).toContain("谐音");
});

test("原字匹配优先于谐音", () => {
  expect(checkRules("心", "心心相印", true, none).score).toBe(2);
});

test("首字无关被拒，原因里点名接龙字", () => {
  const r = checkRules("心", "一马当先", true, none);
  expect([r.ok, r.score]).toEqual([false, 0]);
  expect(r.reason).toContain("心");
});

test("多音字任一读音相同即谐音", () => {
  expect(isHomophone("长", "常")).toBe(true);
  expect(isHomophone("行", "航")).toBe(true);
});

test("谐音不计声调", () => {
  expect(isHomophone("意", "一")).toBe(true);
});

test("不同音", () => {
  expect(isHomophone("心", "山")).toBe(false);
});

test("太短被拒", () => {
  const r = checkRules("心", "心想", true, none);
  expect(r.ok).toBe(false);
  expect(r.reason).toContain("4");
});

test("非汉字被拒", () => {
  expect(checkRules("心", "心abc", true, none).ok).toBe(false);
});

test("本局用过的成语被拒", () => {
  const r = checkRules("心", "心想事成", true, new Set(["心想事成"]));
  expect(r.ok).toBe(false);
  expect(r.reason).toContain("用过");
});

test("去掉首尾空白与标点", () => {
  expect(normalizeIdiom("  心想事成。 ")).toBe("心想事成");
  expect(normalizeIdiom("「心想事成」！")).toBe("心想事成");
});
