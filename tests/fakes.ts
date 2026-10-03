/** 测试替身：按 system prompt 的角色把请求路由到裁判函数或提示脚本，不碰网络。 */

import { LLMError, type ChatMessage, type LLMClient } from "../src/engine/llm.ts";

type Role = "judge" | "hints";
export type ScriptItem = Record<string, unknown> | Error;

export class FakeLLM implements LLMClient {
  readonly calls: { role: Role; messages: ChatMessage[] }[] = [];
  private readonly hints: ScriptItem[];
  private readonly judge: (idiom: string) => boolean;

  constructor(opts: { hints?: ScriptItem[]; judge?: (idiom: string) => boolean } = {}) {
    this.hints = [...(opts.hints ?? [])];
    this.judge = opts.judge ?? (() => true);
  }

  async completeJson(messages: ChatMessage[]): Promise<Record<string, unknown>> {
    const system = messages[0]?.content ?? "";
    const role: Role = system.includes("裁判") ? "judge" : "hints";
    this.calls.push({ role, messages });

    if (role === "judge") {
      const idiom = (messages.at(-1)?.content ?? "").split("「")[1]?.split("」")[0] ?? "";
      const ok = this.judge(idiom);
      return { is_idiom: ok, reason: ok ? "测试裁判：通过" : "测试裁判：查无此成语" };
    }
    const item = this.hints.shift();
    if (item === undefined) throw new LLMError("FakeLLM: hints 脚本已用完");
    if (item instanceof Error) throw item;
    return item;
  }

  roles(): Role[] {
    return this.calls.map((c) => c.role);
  }
}

/** 手动拨动的时钟（秒）。 */
export class FakeClock {
  now = 1000;
  readonly read = (): number => this.now;
}
