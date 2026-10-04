import type { Theme } from "@earendil-works/pi-coding-agent";
import { Key, matchesKey, parseKey, truncateToWidth, visibleWidth, wrapTextWithAnsi, type Component } from "@earendil-works/pi-tui";

/** 只负责展示，可用于提示、状态和结算；生命周期由调用者管理。 */
export interface PanelContent {
  title: string;
  lines: readonly string[];
  footer?: string;
  theme: Pick<Theme, "fg" | "bg" | "bold">;
}

/** 边框 2 列、左右内边距各 1 列；窄终端优先遵守 60% 上限。 */
export function panelWidth(content: PanelContent, columns: number): number {
  const widest = Math.max(...[content.title, ...content.lines, content.footer ?? ""].map(visibleWidth));
  return Math.max(0, Math.min(Math.floor(columns * 0.6), Math.max(40, widest + 4)));
}

export function createPanel({ title, lines, footer, theme }: PanelContent): Component {
  return {
    render(width) {
      if (width <= 0) return [];
      const border = (text: string) => theme.fg("border", text);
      const fit = (text: string, columns: number) => {
        const clipped = truncateToWidth(text, Math.max(0, columns), "…");
        return clipped + " ".repeat(Math.max(0, columns - visibleWidth(clipped)));
      };
      const inner = Math.max(0, width - 2);
      const body = (text: string, muted = false) => border("│") + " " +
        theme.fg(muted ? "muted" : "customMessageText", fit(text, width - 4)) + " " + border("│");
      const heading = truncateToWidth(` ${title} `, Math.max(0, inner - 1), "…");
      const rows = [
        border("╭─") + theme.fg("accent", theme.bold(heading)) + border("─".repeat(Math.max(0, inner - 1 - visibleWidth(heading))) + "╮"),
        ...lines.map((line) => body(line)),
        ...(footer === undefined ? [] : [border(`├${"─".repeat(inner)}┤`), ...wrapTextWithAnsi(footer, Math.max(1, width - 4)).map((line) => body(line, true))]),
        border(`╰${"─".repeat(inner)}╯`),
      ];
      // 连边框、空格一起铺背景，避免 ANSI 前景样式结束后出现透明缝隙。
      // truncateToWidth 会插入 SGR reset；每次 reset 后重新铺背景，包括省略号与补齐空格。
      return rows.map((line) => fit(line, width).split("\x1b[0m")
        .map((part) => theme.bg("customMessageBg", part)).join("\x1b[0m"));
    },
    invalidate() {},
  };
}

/** 信息面板捕获任意键关闭；重复输入不会重复完成。 */
export function createDismissiblePanel(content: PanelContent, done: () => void): Component {
  let closed = false;
  return {
    ...createPanel(content),
    handleInput() {
      if (closed) return;
      closed = true;
      done();
    },
  };
}

/** 捕获焦点的候选选择框；只有确认才返回词，Esc 返回 undefined。 */
export function createHintSelector(
  hints: readonly string[], remaining: number, theme: PanelContent["theme"],
  done: (idiom: string | undefined) => void, requestRender: () => void,
): Component {
  let selected = 0;
  let closed = false;
  return {
    render(width) {
      return createPanel({
        title: "💡 提示", theme,
        lines: hints.map((hint, i) => i === selected
          ? theme.bold(theme.fg("accent", `❯ ${i + 1}. ${hint}`)) : `  ${i + 1}. ${hint}`),
        footer: visibleWidth(hintFooter(remaining)) <= width - 4
          ? hintFooter(remaining) : hintFooter(remaining).replace(" · 剩余提示", "\n剩余提示"),
      }).render(width);
    },
    handleInput(data) {
      if (closed) return;
      if (matchesKey(data, Key.escape) || matchesKey(data, Key.enter)) {
        closed = true;
        done(matchesKey(data, Key.escape) ? undefined : hints[selected]);
        return;
      }
      if (matchesKey(data, Key.up)) selected = (selected + hints.length - 1) % hints.length;
      else if (matchesKey(data, Key.down)) selected = (selected + 1) % hints.length;
      else {
        const index = hints.findIndex((_, i) => parseKey(data) === String(i + 1));
        if (index < 0) return;
        selected = index;
      }
      requestRender();
    },
    invalidate() {},
  };
}

export function hintFooter(remaining: number): string {
  return `↑↓/数字选择 · 回车确认 · Esc 取消 · 剩余提示 ${remaining} 次`;
}
