import { expect, test } from "bun:test";
import { stripTerminalSequences, visibleWidth } from "@earendil-works/pi-tui";
import { createPanel, panelWidth } from "../../src/extension/panel.ts";
import { fakeTheme } from "./fake-pi.ts";

const content = {
  title: "💡 提示",
  lines: ["1. 心想事成", "2. 心旷神怡"],
  footer: "本轮 0 分 · Bot 接龙中",
  theme: fakeTheme,
};

test("面板等宽、不透明，圆角边框内嵌标题，正文编号、分隔线和底注", () => {
  const width = panelWidth(content, 80);
  const panel = createPanel(content);
  const rendered = panel.render(width);
  const lines = rendered.map(stripTerminalSequences);
  expect(width).toBe(28);
  for (const line of rendered) {
    expect(visibleWidth(line)).toBe(width);
    expect(line.startsWith("\x1b[48;5;236m")).toBe(true);
    expect(line.endsWith("\x1b[49m")).toBe(true);
  }
  expect(lines[0]).toMatch(/^╭─ 💡 提示 .*╮$/);
  expect(rendered[0]).toContain("\x1b[1m");
  expect(lines.at(-1)).toBe(`╰${"─".repeat(width - 2)}╯`);
  expect(lines[1]).toContain("│ 1. 心想事成");
  expect(lines[2]).toContain("│ 2. 心旷神怡");
  expect(lines[3]).toBe(`├${"─".repeat(width - 2)}┤`);
  expect(lines[4]).toContain(content.footer);
  panel.invalidate();
  expect(panel.render(width)).toEqual(rendered);
  expect(panel.handleInput).toBeUndefined();
});

test("通用面板支持无底注的状态/结算正文", () => {
  const lines = createPanel({ title: "状态", lines: ["比分：0 : 2"], theme: fakeTheme }).render(28).map(stripTerminalSequences);
  expect(lines).toHaveLength(3);
  expect(lines.join("\n")).not.toContain("├");
});

test("内容宽度加边框内边距，下限 28，上限终端 60%", () => {
  expect(panelWidth({ ...content, lines: ["中".repeat(16)] }, 100)).toBe(36);
  expect(panelWidth({ ...content, lines: ["中".repeat(80)] }, 100)).toBe(60);
});

for (const columns of [0, 1, 2, 3, 5, 10, 20, 40, 80]) {
  test(`窄终端 ${columns} 列不越界，长中文截断带省略号`, () => {
    const data = { ...content, lines: ["很长的中文候选".repeat(20)] };
    const width = panelWidth(data, columns);
    expect(width).toBeLessThanOrEqual(Math.floor(columns * 0.6));
    const rendered = createPanel(data).render(width);
    const lines = rendered.map(stripTerminalSequences);
    for (const line of rendered) {
      expect(visibleWidth(line)).toBe(width);
      expect(line).not.toMatch(/\x1b\[0m(?!\x1b\[48;5;236m)/);
    }
    if (width >= 5) expect(lines[1]).toContain("…");
  });
}
