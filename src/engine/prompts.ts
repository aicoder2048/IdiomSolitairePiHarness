/**
 * 【Prompt Engineering】单步指令：每个函数只负责把一次调用的角色、任务、约束和输出表达清楚，都是纯函数。
 *
 * 与 Python 版的区别：Bot 不再输出 JSON，而是调用 submit_idiom 工具。
 * 于是 Bot 的指令拆成两段：固定不变的系统提示（角色 + 工具协议），
 * 和每回合一条的回合 prompt（接龙字 + 当前模式的约束 + 最近的接龙链）。
 */

import type { ChatMessage } from "./llm.ts";

export type DictLevel = "strict" | "lax";

export const SUBMIT_TOOL = "submit_idiom";

export const DICT_LEVELS: Record<DictLevel, string> = {
  strict:
    "strict：只接受公认的成语——被任一权威成语词典（如《汉语成语大词典》《中华成语大词典》）收录，" +
    "或被普遍当作成语使用的固定语（含常见祝福类成语，如「心想事成」）；普通词组、俗语、自造词判否",
  lax: "lax：除成语外，也接受广为流传的四字俗语、惯用语、熟语；随意拼凑或自造的词组判否",
};

function homophoneRule(allowHomophone: boolean): string {
  return allowHomophone ? "允许谐音：首字可与接龙字同音（不计声调）" : "不允许谐音：首字必须与接龙字完全相同";
}

/** LLM 词库裁判：只判断「是不是成语」，形式规则已由 rules.ts 确定性判定。 */
export function buildVerifierMessages(idiom: string, dictLevel: DictLevel): ChatMessage[] {
  const system = `[ROLE] 你是严谨的成语接龙裁判，精通汉语成语与俗语。
[TASK] 判断候选词在给定词库严格度下是否算作成语。
[词库严格度] ${DICT_LEVELS[dictLevel]}
[OUTPUT] 只输出 json，格式示例：
{"is_idiom": true, "reason": "出自《xx》，意为……（不超过 40 字）"}`;
  return [
    { role: "system", content: system },
    { role: "user", content: `候选词：「${idiom}」；词库严格度：${dictLevel}` },
  ];
}

/** Bot 的系统提示：只讲角色和工具协议，不含任何随回合变化的内容。 */
export const BOT_SYSTEM_PROMPT = `[ROLE] 你是成语接龙高手，正在和人类对战。
[TASK] 每条用户消息给出接龙字、本轮约束和最近的接龙链。想一个合规的成语，调用 ${SUBMIT_TOOL} 工具提交。
[PROTOCOL]
- 只能通过 ${SUBMIT_TOOL} 提交，每次调用只提交一个成语；不要在正文里写成语或解释
- 工具报错说明候选无效：读懂原因，换一个成语再提交
- 工具返回成功或「本轮结束」后立即停止，不要再输出任何内容`;

/** 每回合交给 Bot 的那条消息：接龙字 + 当前模式的约束 + 最近 N 个成语（Compaction 后的视野）。 */
export function buildRoundPrompt(
  targetChar: string,
  allowHomophone: boolean,
  dictLevel: DictLevel,
  recent: readonly string[],
): string {
  const chain =
    recent.length > 0
      ? `[当前接龙历史链条（最近 ${recent.length} 个）]: ${recent.join(" → ")}`
      : "[当前接龙历史链条]: 开局第一个成语";
  return `[接龙字] 「${targetChar}」
[约束]
- ${homophoneRule(allowHomophone)}
- 词库：${DICT_LEVELS[dictLevel]}
- 不能与接龙历史中已出现的成语重复
- 优先选末字好接、常见的成语
${chain}
请调用 ${SUBMIT_TOOL} 提交一个接「${targetChar}」的成语。`;
}

/** 候选被拒后回给 Bot 的 Observation（作为工具错误结果进入本回合上下文）。 */
export function buildObservation(candidate: string, reason: string, attemptsLeft: number): string {
  return `候选词「${candidate}」无效：${reason}。还剩 ${attemptsLeft} 次机会，请换一个成语再调用 ${SUBMIT_TOOL}。`;
}

/** 本回合结算后回给 Bot 的工具结果：明确告诉它停下。 */
export function buildRoundEndMessage(bot: { status: "success" | "failed"; idiom: string }): string {
  return bot.status === "success"
    ? `「${bot.idiom}」通过，本轮结束，请停止输出。`
    : "机会已用完，本轮 Bot 放弃，本轮结束，请停止输出。";
}

/** Bot 没调用工具就想结束时，追加一次的催促。 */
export const NUDGE_MESSAGE = `你还没有提交成语。请立即调用 ${SUBMIT_TOOL} 提交一个接龙成语，不要输出其它文字。`;

/** 为人类玩家生成 n 个候选提示。 */
export function buildHintMessages(targetChar: string, n: number, avoid: readonly string[]): ChatMessage[] {
  const avoidText = avoid.length > 0 ? avoid.join("、") : "无";
  const system = `[ROLE] 你是成语接龙教练。
[TASK] 列出 ${n} 个以 '${targetChar}' 开头的常见成语，供玩家参考。
[CONSTRAINTS]
- 首字必须就是 '${targetChar}'
- 不要包含这些已用过的成语：${avoidText}
[OUTPUT] 只输出 json，格式示例：
{"candidates": ["成语1", "成语2", "成语3"]}`;
  return [
    { role: "system", content: system },
    { role: "user", content: `请给出 ${n} 个以「${targetChar}」开头的成语。` },
  ];
}
