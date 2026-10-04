import type { Theme } from "@earendil-works/pi-coding-agent";
import { truncateToWidth, visibleWidth, type Component } from "@earendil-works/pi-tui";

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
  return Math.max(0, Math.min(Math.floor(columns * 0.6), Math.max(28, widest + 4)));
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
        ...(footer === undefined ? [] : [border(`├${"─".repeat(inner)}┤`), body(footer, true)]),
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
