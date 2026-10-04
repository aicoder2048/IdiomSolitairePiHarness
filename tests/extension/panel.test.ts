import { expect, test } from "bun:test";
import { stripTerminalSequences, visibleWidth } from "@earendil-works/pi-tui";
import { createDismissiblePanel, createHintSelector, createPanel, panelWidth } from "../../src/extension/panel.ts";
import { fakeTheme } from "./fake-pi.ts";

const content = {
  title: "💡 提示",
  lines: ["1. 心想事成", "2. 心旷神怡"],
  footer: "剩余提示 2 次",
  theme: fakeTheme,
};

test("面板等宽、不透明，圆角边框内嵌标题，正文编号、分隔线和底注", () => {
  const width = panelWidth(content, 80);
  const panel = createPanel(content);
  const rendered = panel.render(width);
  const lines = rendered.map(stripTerminalSequences);
  expect(width).toBe(40);
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

test("内容宽度加边框内边距，下限 40，上限终端 60%", () => {
  expect(panelWidth({ ...content, lines: ["中".repeat(16)] }, 100)).toBe(40);
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


test("选择框上下移动、数字选中、回车确认；其余按键不关闭", () => {
  const chosen: (string | undefined)[] = [];
  const panel = createHintSelector(["心想事成", "心旷神怡"], 2, fakeTheme, (value) => chosen.push(value), () => {});
  const text = () => panel.render(48).map(stripTerminalSequences).join("\n");
  expect(text()).toContain("❯ 1. 心想事成");
  panel.handleInput!("\x1b[B");
  expect(text()).toContain("❯ 2. 心旷神怡");
  panel.handleInput!("\x1b[A");
  expect(text()).toContain("❯ 1. 心想事成");
  panel.handleInput!("2");
  expect(text()).toContain("❯ 2. 心旷神怡");
  panel.handleInput!("x");
  panel.handleInput!("9");
  expect(chosen).toEqual([]);
  panel.handleInput!("\r");
  expect(chosen).toEqual(["心旷神怡"]);
  for (const line of panel.render(48)) expect(visibleWidth(line)).toBe(48);
});

test("选择框 Esc 取消，不自动选第一个", () => {
  const chosen: (string | undefined)[] = [];
  const panel = createHintSelector(["心想事成"], 2, fakeTheme, (value) => chosen.push(value), () => {});
  expect(chosen).toEqual([]);
  panel.handleInput!("\x1b");
  expect(chosen).toEqual([undefined]);
});


for (const key of ["x", "\r", "\x1b", "\x1b[A"]) {
  test(`结算面板任意键关闭且只关闭一次：${JSON.stringify(key)}`, () => {
    let closed = 0;
    const summary = { ...content, title: "🏁 对局结束", lines: ["你 2 : 2 Bot · 平局。", "第 1 轮：你：心想事成（+2）"],
      footer: "输入 /restart 再来一局，或 /rounds 加轮数继续。" };
    const panel = createDismissiblePanel(summary, () => closed++);
    const rendered = panel.render(120);
    expect(rendered).toEqual(createPanel(summary).render(120));
    const text = rendered.map(stripTerminalSequences).join("\n");
    for (const line of [summary.title, ...summary.lines, summary.footer]) expect(text).toContain(line);
    panel.invalidate();
    expect(panel.render(120)).toEqual(rendered);
    expect(closed).toBe(0);
    panel.handleInput!(key);
    panel.handleInput!(key);
    expect(closed).toBe(1);
  });
}

for (const width of [0, 1, 2, 3, 5, 20, 80]) {
  test(`结算面板长中文在 ${width} 列内安全截断`, () => {
    const panel = createDismissiblePanel({ ...content, lines: ["第 1 轮：很长的中文结算".repeat(20)] }, () => {});
    for (const row of panel.render(width)) {
      expect(visibleWidth(row)).toBeLessThanOrEqual(width);
      expect(visibleWidth(stripTerminalSequences(row))).toBeLessThanOrEqual(width);
    }
  });
}
