/**
 * Live 冒烟：经 Pi 的 RPC 模式真实跑两回合 + 一条命令。会调用 DeepSeek，产生少量费用（约几千 tokens）。
 * 用法：just smoke（需要 .env 里的 DEEPSEEK_API_KEY）
 *
 * 第 1 回合：人类作答「心想事成」→ input 校验 → Bot 经 submit_idiom 出词
 * 第 2 回合：/pass → 命令开回合 → Bot 出词
 * 最后：/status → 状态卡片，不启动 agent
 */

import { execFileSync } from "node:child_process";
import { realpathSync } from "node:fs";
import { RpcClient } from "@earendil-works/pi-coding-agent";

const TIMEOUT_MS = 120_000;
const model = process.env.DEEPSEEK_MODEL || "deepseek-flash";
if (!process.env.DEEPSEEK_API_KEY) throw new Error("缺少 DEEPSEEK_API_KEY（.env）");

type AnyEvent = { type: string; [key: string]: any };

const client = new RpcClient({
  cliPath: realpathSync(execFileSync("which", ["pi"]).toString().trim()),
  cwd: process.cwd(),
  env: process.env as Record<string, string>,
  args: ["-ne", "-nbt", "-ns", "-np", "-nc", "--no-session", "--model", `deepseek/${model}`, "--thinking", "off", "-e", "./src/extension/index.ts"],
});

const events: AnyEvent[] = [];
client.onEvent((event) => events.push(event as AnyEvent));

function waitFor(predicate: (e: AnyEvent) => boolean, from: number): Promise<void> {
  return new Promise((resolve, reject) => {
    const started = Date.now();
    const timer = setInterval(() => {
      if (events.slice(from).some(predicate)) {
        clearInterval(timer);
        resolve();
      } else if (Date.now() - started > TIMEOUT_MS) {
        clearInterval(timer);
        reject(new Error(`等待超时；最近事件：${events.slice(-5).map((e) => e.type).join(", ")}`));
      }
    }, 100);
  });
}

async function step(label: string, message: string, until: (e: AnyEvent) => boolean): Promise<AnyEvent[]> {
  const from = events.length;
  await client.prompt(message);
  await waitFor(until, from);
  const slice = events.slice(from);
  const cards = slice.filter((e) => e.type === "entry_appended").map((e) => e.entry.data.lines.join(" / "));
  const inputs = slice
    .filter((e) => e.type === "message_end" && e.message.role === "assistant")
    // input 不含命中前缀缓存的部分，两者相加才是这次请求的完整上下文大小
    .map((e) => `${e.message.usage.input + e.message.usage.cacheRead}（缓存命中 ${e.message.usage.cacheRead}）`);
  console.log(`\n== ${label}\n  Bot 每次请求的上下文 tokens：${inputs.join(", ") || "（无模型调用）"}`);
  for (const c of cards) console.log(`  卡片：${c}`);
  return slice;
}

const failures: string[] = [];
const check = (ok: boolean, what: string) => {
  console.log(`  ${ok ? "✓" : "✗"} ${what}`);
  if (!ok) failures.push(what);
};
const cardText = (slice: AnyEvent[]) =>
  slice.filter((e) => e.type === "entry_appended").map((e) => e.entry.data.lines.join("\n")).join("\n");

try {
  await client.start();

  const r1 = await step("第 1 回合：心想事成", "心想事成", (e) => e.type === "agent_settled");
  check(/Bot(：|\s放弃)/.test(cardText(r1)), "回合卡片记录了 Bot 这一步");
  check(r1.some((e) => e.type === "tool_execution_end" && e.toolName === "submit_idiom"), "Bot 通过 submit_idiom 出词");

  const r2 = await step("第 2 回合：/pass", "/pass", (e) => e.type === "agent_settled");
  check(cardText(r2).includes("你跳过本轮"), "/pass 开了新回合");

  const st = await step("/status", "/status", (e) => e.type === "entry_appended");
  check(cardText(st).includes("比分"), "/status 写出状态卡片");
  check(!st.some((e) => e.type === "agent_start"), "/status 不启动 agent（0 token）");
} finally {
  await client.stop();
}

if (failures.length > 0) {
  console.error(`\n冒烟失败：${failures.join("；")}`);
  process.exit(1);
}
console.log("\n冒烟通过。");
