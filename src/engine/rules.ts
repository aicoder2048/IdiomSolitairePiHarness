/**
 * 确定性规则校验（Hashimoto 原则：能用代码判定的，绝不交给概率性模型）。
 *
 * 接龙的「形式规则」全部在这里 0 token 判定：
 *   - 4~12 个汉字、不含其它字符
 *   - 本局未出现过
 *   - 首字 == 接龙字 → 2 分（原字匹配）
 *   - 首字与接龙字同音（忽略声调，多音字取任一读音）→ 1 分（谐音匹配，需当前档位允许）
 * 「是不是一个真成语」属于知识判断，交给 verifier.ts 里的 LLM 词库裁判。
 */

import { pinyin } from "pinyin-pro";

export const MIN_LEN = 4;
export const MAX_LEN = 12;

const CJK = /^[一-鿿]+$/;
const STRIP = new Set(" \t\r\n，。！？、；：,.!?;:'\"“”‘’「」『』《》()（）[]【】");

export type Match = "exact" | "homophone" | "none";

export interface RuleResult {
  ok: boolean;
  score: number; // 2 原字匹配 / 1 谐音匹配 / 0 无效
  match: Match;
  reason: string;
}

/** 去掉首尾空白与常见标点（人类常会顺手打个句号或引号）。 */
export function normalizeIdiom(text: string): string {
  const chars = Array.from(text);
  let start = 0;
  let end = chars.length;
  while (start < end && STRIP.has(chars[start]!)) start++;
  while (end > start && STRIP.has(chars[end - 1]!)) end--;
  return chars.slice(start, end).join("");
}

const readingCache = new Map<string, Set<string>>();

function readings(char: string): Set<string> {
  let cached = readingCache.get(char);
  if (!cached) {
    cached = new Set(pinyin(char, { toneType: "none", multiple: true, type: "array" }));
    readingCache.set(char, cached);
  }
  return cached;
}

/** 两个汉字是否同音：不计声调，多音字只要任一读音相同即可。 */
export function isHomophone(a: string, b: string): boolean {
  const ra = readings(a);
  for (const r of readings(b)) if (ra.has(r)) return true;
  return false;
}

export function checkRules(
  targetChar: string,
  idiom: string,
  allowHomophone: boolean,
  used: ReadonlySet<string>,
): RuleResult {
  if (!CJK.test(idiom)) return reject(`「${idiom}」必须全部是汉字`);
  const length = Array.from(idiom).length;
  if (length < MIN_LEN || length > MAX_LEN) {
    return reject(`成语长度需在 ${MIN_LEN}~${MAX_LEN} 个字之间，「${idiom}」有 ${length} 个字`);
  }
  if (used.has(idiom)) return reject(`「${idiom}」本局已经用过了`);

  const first = Array.from(idiom)[0]!;
  if (first === targetChar) return { ok: true, score: 2, match: "exact", reason: `首字「${first}」与接龙字一致` };
  if (isHomophone(first, targetChar)) {
    if (allowHomophone) {
      return { ok: true, score: 1, match: "homophone", reason: `首字「${first}」与「${targetChar}」谐音` };
    }
    return reject(`首字「${first}」只是「${targetChar}」的谐音，当前模式不允许谐音`);
  }
  return reject(`首字「${first}」接不上「${targetChar}」`);
}

function reject(reason: string): RuleResult {
  return { ok: false, score: 0, match: "none", reason };
}
