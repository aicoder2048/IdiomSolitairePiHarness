/**
 * 引擎的 LLMClient 在 Pi 上的实现：裁判与提示是「代码调模型」，走 Pi 的 model registry 做嵌套调用，
 * 用当前会话选中的模型（启动时 --model deepseek/...），鉴权与 provider 细节都交给 Pi。
 */

import type { Usage } from "@earendil-works/pi-ai";
import type { ExtensionContext } from "@earendil-works/pi-coding-agent";
import { LLMError, parseJsonObject, type ChatMessage, type LLMClient } from "../engine/llm.ts";

export interface UsageTotals {
  calls: number;
  input: number;
  output: number;
  cost: number;
}

export class PiLLMClient implements LLMClient {
  readonly totals: UsageTotals = { calls: 0, input: 0, output: 0, cost: 0 };
  private ctx: ExtensionContext | undefined;

  /** 每次 session_start 重新绑定；嵌套调用总是用绑定时会话的当前模型。 */
  bind(ctx: ExtensionContext): void {
    this.ctx = ctx;
  }

  async completeJson(messages: ChatMessage[], signal?: AbortSignal): Promise<Record<string, unknown>> {
    const ctx = this.ctx;
    if (!ctx) throw new LLMError("扩展尚未绑定会话");
    const model = ctx.model;
    if (!model) throw new LLMError("当前没有选中模型，请用 --model 指定");

    const systemPrompt = messages.filter((m) => m.role === "system").map((m) => m.content).join("\n");
    const userMessages = messages
      .filter((m) => m.role === "user")
      .map((m) => ({ role: "user" as const, content: m.content, timestamp: Date.now() }));

    const response = await ctx.modelRegistry
      .streamSimple(
        model,
        { systemPrompt, messages: userMessages },
        // DeepSeek 等 OpenAI 兼容接口的 JSON Output；其它 provider 会忽略这个参数
        { signal, samplingParams: { response_format: { type: "json_object" } } },
      )
      .result();
    this.record(response.usage);

    if (response.stopReason === "error" || response.stopReason === "aborted") {
      throw new LLMError(response.errorMessage ?? `模型调用${response.stopReason === "aborted" ? "被中断" : "失败"}`);
    }
    const text = response.content
      .filter((c) => c.type === "text")
      .map((c) => c.text)
      .join("");
    return parseJsonObject(text);
  }

  /** 当前已记录的调用数，配合 usageSince() 算出一段代码里的嵌套调用用量。 */
  mark(): number {
    return this.records.length;
  }

  /** mark 之后所有嵌套调用的用量之和；工具把它放进结果，会话的 token 总数才准确。 */
  usageSince(mark: number): Usage | undefined {
    const recent = this.records.slice(mark);
    if (recent.length === 0) return undefined;
    const sum: Usage = {
      input: 0,
      output: 0,
      cacheRead: 0,
      cacheWrite: 0,
      totalTokens: 0,
      cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0, total: 0 },
    };
    for (const u of recent) {
      sum.input += u.input;
      sum.output += u.output;
      sum.cacheRead += u.cacheRead;
      sum.cacheWrite += u.cacheWrite;
      sum.totalTokens += u.totalTokens;
      sum.cost.input += u.cost.input;
      sum.cost.output += u.cost.output;
      sum.cost.cacheRead += u.cost.cacheRead;
      sum.cost.cacheWrite += u.cost.cacheWrite;
      sum.cost.total += u.cost.total;
    }
    return sum;
  }

  private readonly records: Usage[] = [];

  private record(usage: Usage): void {
    this.records.push(usage);
    this.totals.calls += 1;
    this.totals.input += usage.input;
    this.totals.output += usage.output;
    this.totals.cost += usage.cost.total;
  }
}
