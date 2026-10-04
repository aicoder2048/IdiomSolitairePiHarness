import { expect, test } from "bun:test";
import { visibleWidth } from "@earendil-works/pi-tui";
import { createPanel } from "../../src/extension/panel.ts";

const title = "💡 提示";
const lines = ["心想事成", "心旷神怡", "本轮 0 分，Bot 接龙中…"];

test("面板依次显示标题、候选和末行；渲染与 invalidate 不关闭", () => {
  let closed = 0;
  const panel = createPanel(title, lines, () => closed++);
  expect(panel.render(80)).toEqual([title, ...lines]);
  panel.invalidate();
  expect(panel.render(80)).toEqual([title, ...lines]);
  expect(closed).toBe(0);
});

for (const key of ["x", "\x1b", "\r", "\x1b[A"]) {
  test(`任意键 ${JSON.stringify(key)} 只关闭一次`, () => {
    let closed = 0;
    const panel = createPanel(title, lines, () => closed++);
    panel.handleInput!(key);
    panel.handleInput!(key);
    expect(closed).toBe(1);
  });
}

for (const width of [0, 1, 2, 3, 5, 10, 20, 80]) {
  test(`面板中文与 emoji 在 ${width} 列内安全截断`, () => {
    const panel = createPanel(title, [...lines, "很长的中文候选".repeat(20)], () => {});
    for (const line of panel.render(width)) expect(visibleWidth(line)).toBeLessThanOrEqual(width);
  });
}
