/**
 * 引擎看到的模型只有一个窄接口：发一组消息，拿回一个 JSON 对象。
 * 裁判与提示走这里；Bot 出词不走这里，它由 Pi 的 agent loop 驱动。
 * 具体实现（Pi 的 model registry）在 extension 层注入，引擎与测试都不碰网络。
 */

export interface ChatMessage {
  role: "system" | "user";
  content: string;
}

export interface LLMClient {
  completeJson(messages: ChatMessage[], signal?: AbortSignal): Promise<Record<string, unknown>>;
}

export class LLMError extends Error {
  override name = "LLMError";
}

const FENCE = /^```(?:json)?\s*([\s\S]*?)\s*```$/i;

/** 从模型回复中取出 JSON 对象；容忍代码围栏，其余一律报 LLMError。 */
export function parseJsonObject(text: string): Record<string, unknown> {
  const trimmed = text.trim();
  if (!trimmed) throw new LLMError("模型返回了空内容");
  const body = FENCE.exec(trimmed)?.[1] ?? trimmed;
  let value: unknown;
  try {
    value = JSON.parse(body);
  } catch {
    throw new LLMError(`模型返回的不是合法 JSON：${body.slice(0, 80)}`);
  }
  if (typeof value !== "object" || value === null || Array.isArray(value)) {
    throw new LLMError("模型返回的 JSON 顶层不是对象");
  }
  return value as Record<string, unknown>;
}
