import { expect, test } from "bun:test";
import { ChainHistory } from "../../src/engine/context.ts";

function filled(n: number, maxTurns = 3): ChainHistory {
  const chain = new ChainHistory(maxTurns);
  for (let i = 0; i < n; i++) {
    chain.addTurn(i % 2 === 0 ? "human" : "bot", `成语${"一二三四五六七八九十"[i]}号`, 2);
  }
  return chain;
}

test("判重集合覆盖完整历史", () => {
  expect(filled(5).usedIdioms().size).toBe(5);
});

test("模型视野只含最近 N 个", () => {
  expect(filled(5, 3).recentIdioms()).toEqual(["成语三号", "成语四号", "成语五号"]);
});

test("truncate 回滚到指定长度，判重集合随之回滚", () => {
  const chain = filled(4);
  chain.truncate(2);
  expect(chain.turns.map((t) => t.idiom)).toEqual(["成语一号", "成语二号"]);
  expect(chain.usedIdioms().has("成语三号")).toBe(false);
});

test("clear 清空", () => {
  const chain = filled(3);
  chain.clear();
  expect(chain.turns).toEqual([]);
});
