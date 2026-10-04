/**
 * 假的 ExtensionAPI：只实现本扩展用到的部分，记录注册的处理器与副作用，
 * 让测试按 Pi 的事件顺序（input → before_agent_start → context → 工具 → agent_before_settle）手动驱动。
 */

import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";

type Handler = (event: any, ctx: ExtensionContext) => unknown;
type CustomArgs = Parameters<ExtensionContext["ui"]["custom"]>;

interface CustomCall {
  factory: CustomArgs[0];
  options: CustomArgs[1];
  done: (result?: unknown) => void;
  reject: (reason: Error) => void;
  completed: boolean;
}

export interface Notice {
  message: string;
  type: string;
}

export class FakePi {
  readonly handlers = new Map<string, Handler[]>();
  readonly tools = new Map<string, any>();
  readonly commands = new Map<string, any>();
  readonly entries: { customType: string; data: any }[] = [];
  readonly userMessages: string[] = [];
  readonly notices: Notice[] = [];
  readonly widgets = new Map<string, string[] | undefined>();
  activeTools: string[] = [];
  readonly customCalls: CustomCall[] = [];

  constructor(mode: ExtensionContext["mode"] = "rpc") {
    this.ctx.mode = mode;
  }

  readonly api = {
    on: (event: string, handler: Handler) => {
      this.handlers.set(event, [...(this.handlers.get(event) ?? []), handler]);
      return () => {};
    },
    registerTool: (tool: any) => this.tools.set(tool.name, tool),
    registerCommand: (name: string, options: any) => this.commands.set(name, options),
    registerEntryRenderer: () => {},
    appendEntry: (customType: string, data: any) => this.entries.push({ customType, data }),
    sendUserMessage: (content: string) => this.userMessages.push(content),
    setActiveTools: (names: string[]) => {
      this.activeTools = names;
    },
  } as unknown as ExtensionAPI;

  readonly ctx = {
    hasUI: true,
    mode: "rpc",
    signal: undefined,
    ui: {
      notify: (message: string, type = "info") => this.notices.push({ message, type }),
      setWidget: (key: string, lines: string[] | undefined) => this.widgets.set(key, lines),
      setStatus: () => {},
      custom: (factory: CustomArgs[0], options: CustomArgs[1]) => new Promise((resolve, reject) => {
        const call: CustomCall = {
          factory, options, reject, completed: false,
          done: (result) => {
            call.completed = true;
            resolve(result);
          },
        };
        this.customCalls.push(call);
      }),
    },
  } as unknown as ExtensionContext;

  async emit(event: string, payload: Record<string, unknown> = {}): Promise<unknown> {
    let result: unknown;
    for (const handler of this.handlers.get(event) ?? []) {
      result = await handler({ type: event, ...payload }, this.ctx);
    }
    return result;
  }

  input(text: string, source = "interactive"): Promise<any> {
    return this.emit("input", { text, source });
  }

  submit(idiom: string): Promise<any> {
    return this.tools.get("submit_idiom").execute("call-1", { idiom }, undefined, undefined, this.ctx);
  }

  command(name: string, args = ""): Promise<void> {
    return this.commands.get(name).handler(args, this.ctx);
  }

  settle(outcome: "completed" | "aborted" | "error" = "completed"): Promise<any> {
    return this.emit("agent_before_settle", { outcome, entries: [], continue: false, context: { canContinue: true } });
  }

  cards(): string[][] {
    return this.entries.filter((e) => e.customType === "idiom-card").map((e) => e.data.lines);
  }

  lastNotice(): string {
    return this.notices.at(-1)?.message ?? "";
  }
}
