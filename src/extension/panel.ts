import { truncateToWidth, visibleWidth, type Component } from "@earendil-works/pi-tui";

/** 只给人看的静态面板；任意键关闭，不参与对局状态。 */
export function createPanel(title: string, lines: readonly string[], done: () => void): Component {
  let closed = false;
  return {
    render(width) {
      if (width <= 0) return [];
      return [title, ...lines].map((line) =>
        visibleWidth(line) <= width ? line : truncateToWidth(line, width, ""),
      );
    },
    invalidate() {},
    handleInput() {
      if (closed) return;
      closed = true;
      done();
    },
  };
}
