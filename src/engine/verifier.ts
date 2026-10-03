/**
 * 两级 Cheap Verifier：先确定性规则（0 token），通过后才问 LLM 词库裁判。
 * 人类答案的裁判与 Bot 的自检共用同一个 Verifier，保证两边标准一致。
 */

import type { LLMClient } from "./llm.ts";
import { buildVerifierMessages, type DictLevel } from "./prompts.ts";
import { checkRules } from "./rules.ts";

export type VerdictStage = "rules" | "llm" | "error";

export interface Verdict {
  isValid: boolean;
  score: number; // 2 原字 / 1 谐音 / 0 无效（未乘模式倍率）
  reason: string;
  stage: VerdictStage; // 在哪一级被判定
}

interface Judgement {
  isIdiom: boolean;
  reason: string;
}

export class Verifier {
  private readonly judgements = new Map<string, Judgement>();

  constructor(private readonly llm: LLMClient) {}

  async verify(
    targetChar: string,
    idiom: string,
    allowHomophone: boolean,
    dictLevel: DictLevel,
    used: ReadonlySet<string>,
    signal?: AbortSignal,
  ): Promise<Verdict> {
    const rule = checkRules(targetChar, idiom, allowHomophone, used);
    if (!rule.ok) return { isValid: false, score: 0, reason: rule.reason, stage: "rules" };

    let judgement: Judgement;
    try {
      judgement = await this.judge(idiom, dictLevel, signal);
    } catch (e) {
      // 裁判不可用时判本次无效，但原因要原样交代出去，交给调用方展示或重试
      return { isValid: false, score: 0, reason: `裁判暂时不可用：${errorMessage(e)}`, stage: "error" };
    }
    if (!judgement.isIdiom) {
      return { isValid: false, score: 0, reason: `「${idiom}」不被 ${dictLevel} 词库认可：${judgement.reason}`, stage: "llm" };
    }
    return { isValid: true, score: rule.score, reason: `${rule.reason}。${judgement.reason}`, stage: "llm" };
  }

  private async judge(idiom: string, dictLevel: DictLevel, signal?: AbortSignal): Promise<Judgement> {
    const key = `${dictLevel}:${idiom}`;
    const cached = this.judgements.get(key);
    if (cached) return cached;
    const res = await this.llm.completeJson(buildVerifierMessages(idiom, dictLevel), signal);
    const judgement = { isIdiom: res.is_idiom === true, reason: String(res.reason ?? "").trim() };
    this.judgements.set(key, judgement);
    return judgement;
  }
}

export function errorMessage(e: unknown): string {
  return e instanceof Error ? e.message : String(e);
}
