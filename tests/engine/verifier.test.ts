import { expect, test } from "bun:test";
import { LLMError, type LLMClient } from "../../src/engine/llm.ts";
import { Verifier } from "../../src/engine/verifier.ts";
import { FakeLLM } from "../fakes.ts";

const none = new Set<string>();

test("规则不过直接短路，不调用模型", async () => {
  const llm = new FakeLLM();
  const v = await new Verifier(llm).verify("心", "一马当先", true, "strict", none);
  expect([v.isValid, v.score, v.stage]).toEqual([false, 0, "rules"]);
  expect(llm.calls).toEqual([]);
});

test("合法原字成语得 2 分", async () => {
  const v = await new Verifier(new FakeLLM()).verify("心", "心想事成", false, "strict", none);
  expect([v.isValid, v.score, v.stage]).toEqual([true, 2, "llm"]);
});

test("谐音成语得 1 分", async () => {
  const v = await new Verifier(new FakeLLM()).verify("心", "新官上任", true, "lax", none);
  expect([v.isValid, v.score]).toEqual([true, 1]);
});

test("裁判否决自造词", async () => {
  const llm = new FakeLLM({ judge: () => false });
  const v = await new Verifier(llm).verify("心", "心花乱飞", true, "strict", none);
  expect([v.isValid, v.score, v.stage]).toEqual([false, 0, "llm"]);
  expect(v.reason).toContain("查无此成语");
});

test("模型异常写进裁决，不往外抛", async () => {
  const broken: LLMClient = {
    completeJson: async () => {
      throw new LLMError("网络断了");
    },
  };
  const v = await new Verifier(broken).verify("心", "心想事成", true, "strict", none);
  expect([v.isValid, v.stage]).toEqual([false, "error"]);
  expect(v.reason).toContain("网络断了");
});

test("裁判结论按（成语, 词库）缓存", async () => {
  const llm = new FakeLLM();
  const verifier = new Verifier(llm);
  await verifier.verify("心", "心想事成", true, "strict", none);
  await verifier.verify("心", "心想事成", true, "strict", none);
  await verifier.verify("心", "心想事成", true, "lax", none);
  expect(llm.roles()).toEqual(["judge", "judge"]);
});

test("模型异常不进缓存，下次重新裁判", async () => {
  let calls = 0;
  const flaky: LLMClient = {
    completeJson: async () => {
      calls += 1;
      if (calls === 1) throw new LLMError("超时");
      return { is_idiom: true, reason: "ok" };
    },
  };
  const verifier = new Verifier(flaky);
  expect((await verifier.verify("心", "心想事成", true, "strict", none)).stage).toBe("error");
  expect((await verifier.verify("心", "心想事成", true, "strict", none)).isValid).toBe(true);
});
