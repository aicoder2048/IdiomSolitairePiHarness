/**
 * 【Context Engineering】Bot 的视野只到「本回合」。
 *
 * Pi 会把每次工具报错都写进 session，不裁剪的话，上一回合的失败尝试会一直留在后面每回合的 prompt 里。
 * 每回合的第一条 user 消息（回合 prompt）已经带了压缩过的接龙链，所以只保留最后一条 user 消息及其之后的内容：
 * 本回合的回合 prompt、Bot 的工具调用、工具报错（Observation）。回合一结束，这些 Observation 自然出视野。
 * 完整记录仍在 session 里，供 /export 与调试查看。
 */

export function currentRoundOnly<T extends { role: string }>(messages: T[]): T[] {
  for (let i = messages.length - 1; i >= 0; i--) {
    if (messages[i]!.role === "user") return messages.slice(i);
  }
  return messages;
}
