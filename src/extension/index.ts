/**
 * 成语接龙 · Pi extension（方案 B：Pi 原生）
 *
 * 四层在 Pi 上的落点：
 *   Harness  input 拦截人类输入（规则 + 裁判，无效不放行）；斜杠命令 0 token；
 *            submit_idiom 是 Bot 碰到账本的唯一入口；setActiveTools 只留这一个工具
 *   Loop     Pi 自己的 turn 循环：候选无效 → 工具报错（isError）→ 模型读到原因再提交；
 *            预算在引擎里计数，通过或用尽时 terminate；agent_before_settle 催一次、再不交就判放弃
 *   Context  context 事件只保留本回合消息；回合 prompt 自带最近 N 个成语
 *   Prompt   before_agent_start 换成 Bot 的系统提示；工具描述与回合 prompt 也是 prompt
 *
 * 写账只发生在 input 处理器、命令和工具的 execute() 里，都是确定性代码。
 */

import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";
import { Box, Text } from "@earendil-works/pi-tui";
import { Type } from "typebox";
import { IdiomGame, MODES, type BotSubmitResult, type GameOptions, type Outcome } from "../engine/game.ts";
import type { LLMClient } from "../engine/llm.ts";
import { BOT_SYSTEM_PROMPT, NUDGE_MESSAGE, SUBMIT_TOOL, buildRoundEndMessage } from "../engine/prompts.ts";
import { currentRoundOnly } from "./context-filter.ts";
import { PiLLMClient } from "./llm-client.ts";
import { createPanel } from "./panel.ts";
import * as view from "./view.ts";

const WIDGET_KEY = "idiom-board";
const STATUS_KEY = "idiom";
const CARD = "idiom-card";
const NUDGE = "idiom-nudge";
const MAX_NUDGES = 1;

interface CardData {
  title?: string;
  lines: string[];
}

export interface IdiomExtensionOptions {
  /** 裁判与提示用的模型；默认经 Pi 的 model registry 调当前会话的模型（测试注入假模型）。 */
  llm?: LLMClient;
  clock?: () => number;
  game?: Omit<GameOptions, "llm" | "clock">;
}

export function createIdiomExtension(options: IdiomExtensionOptions = {}) {
  return function idiomSolitaire(pi: ExtensionAPI): void {
    const piLLM = options.llm ? undefined : new PiLLMClient();
    const llm: LLMClient = options.llm ?? piLLM!;
    const newGame = () => new IdiomGame({ llm, clock: options.clock, ...options.game });

    let game = newGame();
    let nudges = 0;
    let ticker: ReturnType<typeof setInterval> | undefined;

    // ---------------------------------------------------------------- 展示

    function notify(ctx: ExtensionContext, message: string, type: "info" | "warning" | "error" = "info"): void {
      if (ctx.hasUI) ctx.ui.notify(message, type);
    }

    function refresh(ctx: ExtensionContext): void {
      if (!ctx.hasUI) return;
      ctx.ui.setWidget(WIDGET_KEY, view.boardLines(game));
      if (piLLM) ctx.ui.setStatus(STATUS_KEY, view.usageStatus(piLLM.totals));
    }

    /** 对话流里的卡片：存进 session，但不进模型上下文。 */
    function card(lines: string[], title?: string): void {
      pi.appendEntry<CardData>(CARD, { title, lines });
    }

    pi.registerEntryRenderer<CardData>(CARD, (entry, _options, theme) => {
      const data = entry.data ?? { lines: [] };
      const box = new Box(1, 0, (text) => theme.bg("customMessageBg", text));
      if (data.title) box.addChild(new Text(theme.fg("accent", data.title), 0, 0));
      box.addChild(new Text(data.lines.join("\n"), 0, 0));
      return box;
    });

    /** 人类这一步的结果告诉玩家；开了新回合就返回要交给 Bot 的回合 prompt。 */
    function report(out: Outcome, ctx: ExtensionContext): string | undefined {
      switch (out.kind) {
        case "noop":
          return undefined;
        case "busy":
        case "info":
          notify(ctx, out.message);
          return undefined;
        case "invalid":
          notify(ctx, `✗ ${out.message}`, "warning");
          return undefined;
        case "error":
          notify(ctx, out.message, "error");
          return undefined;
        case "command":
          notify(ctx, out.message);
          refresh(ctx);
          return undefined;
        case "bot_turn":
          nudges = 0;
          if (out.hints.length > 0) {
            if (ctx.mode === "tui") {
              // 只展示，不等待面板关闭：Bot 回合照常开始。
              void ctx.ui.custom<void>(
                (_tui, _theme, _keybindings, done) =>
                  createPanel("💡 提示", [...out.hints, "本轮 0 分，Bot 接龙中…"], () => done()),
                { overlay: true },
              ).catch(() => notify(ctx, "提示面板显示失败。", "error"));
            } else {
              card([`提示：${out.hints.join("、")}`, view.describeHumanMove(out.human)]);
            }
          } else notify(ctx, view.describeHumanMove(out.human));
          refresh(ctx);
          return out.prompt;
      }
    }

    function settle(res: Extract<BotSubmitResult, { kind: "round" }>, ctx: ExtensionContext): void {
      card(view.roundCardLines(res.record));
      if (res.gameOver) card(view.finalLines(game));
      refresh(ctx);
    }

    function forfeit(ctx: ExtensionContext, reason: string): void {
      const res = game.forfeitBot(reason);
      if (res.kind === "round") settle(res, ctx);
    }

    // ---------------------------------------------------------------- 生命周期

    pi.on("session_start", async (_event, ctx) => {
      piLLM?.bind(ctx);
      game = newGame();
      nudges = 0;
      pi.setActiveTools([SUBMIT_TOOL]); // Bot 只有这一个工具：护栏写在代码里，不靠启动参数
      refresh(ctx);
      if (ctx.mode === "tui" && !ticker) {
        ticker = setInterval(() => {
          if (game.timerSeconds > 0 && !game.awaitingBot && !game.gameOver) refresh(ctx);
        }, 1000);
        ticker.unref?.();
      }
      notify(ctx, `成语接龙开始！首字「${game.lastChar}」，共 ${game.maxRounds} 轮。直接输入成语作答，/help 查看规则。`);
    });

    pi.on("session_shutdown", () => {
      if (ticker) clearInterval(ticker);
      ticker = undefined;
    });

    // ---------------------------------------------------------------- Harness：人类输入

    pi.on("input", async (event, ctx) => {
      if (event.source === "extension") return { action: "continue" }; // 本扩展发出的回合 prompt
      const text = event.text.trim();
      if (text.startsWith("/")) {
        notify(ctx, `未知命令 ${text.split(/\s+/)[0]}，输入 /help 查看命令。`, "warning");
        return { action: "handled" };
      }
      const prompt = report(await game.submitHuman(text, ctx.signal), ctx);
      return prompt === undefined ? { action: "handled" } : { action: "transform", text: prompt };
    });

    // ---------------------------------------------------------------- Prompt 与 Context

    // 改提示分段而不是整段强制覆盖：Pi 会把变化记进 transcript，/export 看到的就是模型实际收到的
    pi.on("before_agent_start", (event) => {
      event.systemPromptOptions.customPrompt = BOT_SYSTEM_PROMPT;
    });

    pi.on("context", (event) => ({ messages: currentRoundOnly(event.messages) }));

    // ---------------------------------------------------------------- Loop：Bot 唯一的工具

    pi.registerTool({
      name: SUBMIT_TOOL,
      label: "接龙",
      description:
        "提交你这一回合的接龙成语（只含汉字）。无效时返回错误与原因，请换一个再提交；通过或机会用完时本轮结束。",
      parameters: Type.Object({ idiom: Type.String({ description: "一个成语，例如：成竹在胸" }) }),
      executionMode: "sequential",
      async execute(_toolCallId, params, signal, _onUpdate, ctx) {
        const mark = piLLM?.mark() ?? 0;
        const res = await game.submitBot(params.idiom, signal);
        const usage = piLLM?.usageSince(mark);
        refresh(ctx);
        switch (res.kind) {
          case "rejected":
            return { content: [{ type: "text", text: res.observation }], details: undefined, isError: true, usage };
          case "stale":
            return { content: [{ type: "text", text: `${res.message}请停止输出。` }], details: undefined, terminate: true, usage };
          case "round":
            settle(res, ctx);
            return {
              content: [{ type: "text", text: buildRoundEndMessage(res.record.bot) }],
              details: undefined,
              terminate: true,
              usage,
            };
        }
      },
    });

    pi.on("agent_before_settle", (event, ctx) => {
      if (!game.awaitingBot) return undefined;
      if (event.outcome === "completed" && nudges < MAX_NUDGES && event.context.canContinue) {
        nudges += 1;
        return {
          continue: true,
          entries: [{ type: "custom_message", customType: NUDGE, content: NUDGE_MESSAGE, display: false }],
        };
      }
      const reason =
        event.outcome === "completed" ? "没有调用 submit_idiom 提交成语" : event.outcome === "aborted" ? "回合被中断" : "模型调用出错";
      forfeit(ctx, reason);
      return undefined;
    });

    pi.on("agent_settled", (_event, ctx) => {
      if (game.awaitingBot) forfeit(ctx, "回合意外结束");
    });

    // ---------------------------------------------------------------- 斜杠命令（给人用）

    function command(
      name: keyof typeof view.COMMANDS,
      handler: (args: string, ctx: ExtensionContext) => Promise<void> | void,
      choices?: readonly string[],
    ): void {
      pi.registerCommand(name, {
        description: view.COMMANDS[name]![1],
        handler: async (args, ctx) => handler(args, ctx),
        getArgumentCompletions: choices
          ? (prefix) => choices.filter((c) => c.startsWith(prefix)).map((c) => ({ value: c, label: c }))
          : undefined,
      });
    }

    function startBotTurn(prompt: string | undefined): void {
      if (prompt !== undefined) pi.sendUserMessage(prompt);
    }

    command("hint", async (_args, ctx) => {
      notify(ctx, "正在想提示…");
      startBotTurn(report(await game.hint(3, ctx.signal), ctx));
    });
    command("pass", (_args, ctx) => startBotTurn(report(game.pass(), ctx)));
    command("undo", (_args, ctx) => void report(game.undo(), ctx));
    command("difficulty", (args, ctx) => void report(game.setMode(args), ctx), MODES);
    command("rounds", (args, ctx) => void report(game.setRounds(args), ctx), ["5", "9", "15", "20"]);
    command("timer", (args, ctx) => void report(game.setTimer(args), ctx), ["0", "30", "60", "120"]);
    command("restart", (args, ctx) => void report(game.restart(args), ctx));
    command("status", () => card(view.statusLines(game, piLLM?.totals), "📊 状态"));
    command("chain", () => card(view.chainLines(game), "📜 接龙链"));
    command("help", () => card(view.helpLines(), "📖 成语接龙"));
  };
}

export default createIdiomExtension();
