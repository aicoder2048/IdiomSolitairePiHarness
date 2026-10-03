# Pi Extension 入门教程：Hello World

> 最后核对：2026-10-03，基于 pi.dev/docs/latest（@earendil-works/pi-coding-agent 1.0.1）

## 前置条件

```bash
# 确认 pi 已安装
which pi
# → /opt/homebrew/bin/pi

# 进入你的项目
cd /Users/szou/Python/Playground/PiAgent/pi-vs-claude-code
```

## Level 1: 最小的 Extension

创建 `.pi/extensions/hello.ts`：

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.registerCommand("hello", {
    description: "Say hello",
    handler: async (args, ctx) => {
      ctx.ui.notify(`Hello, ${args || "world"}!`, "info");
    },
  });
}
```

### 测试

```bash
# print 模式（非交互式，快速验证加载）
pi -e .pi/extensions/hello.ts -p "say hi"

# 交互式（输入 /hello）
pi -e .pi/extensions/hello.ts
# 然后输入: /hello Sean
```

### 解释

| 概念 | 说明 |
|------|------|
| `export default function(pi)` | Pi 用 jiti 编译 TS，默认导出工厂函数 |
| `pi.registerCommand(name, opts)` | 注册 slash command，用户输入 `/name` 触发 |
| `ctx.ui.notify(msg, level)` | 在 footer 弹出提示，不阻塞（info / warning / error） |
| `-e` 或 `--extension` | 从路径加载一个扩展 |

## Level 2: 注册一个自定义工具 (Tool)

工具是 LLM 可以主动调用的能力。扩展文件现在变成：

```typescript
import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
import { Type } from "typebox";                    // ← 新增

export default function (pi: ExtensionAPI) {
  pi.registerCommand("hello", { ... });            // 同上

  // ===== 新增: 自定义工具 =====
  pi.registerTool({
    name: "greet",                                 // LLM 看到的函数名
    label: "Greet",                                // TUI 显示名
    description: "Say hello to the user by name.", // LLM 会用这个来判断何时调用

    parameters: Type.Object({                      // TypeBox → JSON Schema
      name: Type.String({ description: "..." }),
      style: Type.Optional(Type.String({ description: "casual, formal, excited" })),
    }),

    async execute(toolCallId, params, signal, onUpdate, ctx) {
      return {
        content: [{ type: "text", text: `Hello ${params.name}!` }],
        details: undefined,                        // 无结构化数据时用 undefined；有则存到 session，用于 UI 渲染/状态重建
      };
    },
  });
}
```

### 测试

```bash
pi -e .pi/extensions/hello.ts
# 输入: 请调用 greet 工具向我打招呼，名字是 Sean
```

### 解释

| 参数 | 说明 |
|------|------|
| `toolCallId` | 每次调用的唯一 ID |
| `params` | 已经过 schema 校验的参数 |
| `signal` | AbortSignal，用户按 Esc 时触发 |
| `onUpdate` | 回调函数，用于推送流式进度更新 |
| `ctx` | 扩展上下文（ExtensionContext + `executeTool()`），包含 ui、sessionManager 等 |
| 返回值 `.content` | 发给 LLM 的内容 |
| 返回值 `.details` | 存入 session，扩展可在 `session_start` 中通过 `ctx.sessionManager.getBranch()` 恢复状态 |

## Level 3: 事件拦截

```typescript
export default function (pi: ExtensionAPI) {
  // ... 命令和工具注册同上 ...

  // 3a. 会话生命周期
  pi.on("session_start", async (_event, ctx) => {
    ctx.ui.notify("Extension 已加载", "info");
  });

  // 3b. 拦截危险 bash 命令
  pi.on("tool_call", async (event, ctx) => {
    if (event.toolName === "bash" && event.input.command?.includes("rm -rf")) {
      const ok = await ctx.ui.confirm("危险操作", "确定要执行 rm -rf 吗？");
      if (!ok) return { block: true, reason: "User cancelled" };
    }
  });

  // 3c. 拦截用户输入（在发给 LLM 之前）
  pi.on("input", async (event, ctx) => {
    if (event.text === "ping") {
      ctx.ui.notify("pong!", "info");
      return { action: "handled" };    // 不发给 LLM
    }
    return { action: "continue" };     // 正常流程
  });
}
```

### 常用事件清单

| 事件 | 触发时机 | 可做什么 |
|------|---------|---------|
| `session_start` | 会话启动/恢复/reload | 初始化状态、通知 |
| `session_shutdown` | 会话关闭/切换/reload | 清理资源、保存状态（需幂等） |
| `before_agent_start` | 用户发 prompt 后 | 注入消息、修改 system prompt |
| `agent_start` / `agent_end` | 一次完整的 agent 响应 | 记录、日志 |
| `turn_start` / `turn_end` | 每次 LLM 调用+工具 | 统计、状态栏更新 |
| `tool_call` | 工具执行前 | **拦截/阻止**、改写参数 |
| `tool_result` | 工具执行后 | **修改结果** |
| `input` | 用户输入（命令检查之后）| **拦截/改写输入** |
| `context` | LLM 调用前 | 修改上下文消息 |

## Level 4: 状态栏和 UI

```typescript
// 在 footer 显示持久状态
ctx.ui.setStatus("my-ext", "Processing...");
ctx.ui.setStatus("my-ext", undefined);  // 清除

// 在 turn_end 中更新统计
pi.on("turn_end", async (_event, ctx) => {
  ctx.ui.setStatus("hello-ext", `Turns: ${count}`);
});
```

## 扩展加载方式

| 方式 | 说明 |
|------|------|
| `.pi/extensions/*.ts` | 项目级，启动时自动发现（需先授予 project trust） |
| `~/.pi/agent/extensions/*.ts` | 全局，所有项目生效 |
| `extensions/<name>/index.ts` | 上述两个目录下也可用子目录 + `index.ts` 写多文件扩展 |
| `pi -e ./path.ts` | 手动指定路径加载 |
| `settings.json → "extensions": [...]` | 通过配置加载 |
| `pi install <package>` | 通过 pi packages 安装 |

修改扩展后运行 `/reload` 即可热更新，无需重启 pi。

## 本项目的完整扩展

已创建在 `.pi/extensions/hello.ts`，包含上述所有示例。交互式测试：

```bash
cd /Users/szou/Python/Playground/PiAgent/pi-vs-claude-code
pi
```

进入后尝试：
- `/hello Sean` — 测试自定义命令
- `ping` — 测试输入拦截
- `请用 greet 工具向 Sean 打招呼` — 测试 LLM 主动调用工具
- `/reload` — 热更新扩展
