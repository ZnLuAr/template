import { afterEach, describe, expect, it, vi } from "vitest";

import { run } from "../../src/entry/cli.js";

describe("cli（真实组装路径）", () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("带名字运行输出问候", () => {
    const log = vi.spyOn(console, "log").mockImplementation(() => {});

    const code = run(["Ada"]);

    expect(code).toBe(0);
    // 具体问候随系统时钟变化，只断言结构与名字
    expect(log).toHaveBeenCalledExactlyOnceWith(expect.stringMatching(/, Ada\.$/));
  });

  it("无参数默认问候 world", () => {
    const log = vi.spyOn(console, "log").mockImplementation(() => {});

    expect(run([])).toBe(0);
    expect(log).toHaveBeenCalledExactlyOnceWith(expect.stringMatching(/^Good \w+, world\.$/));
  });

  it("--recent 回放历史（同一次组装）", () => {
    const log = vi.spyOn(console, "log").mockImplementation(() => {});

    expect(run(["Ada", "--recent", "3"])).toBe(0);
    const lines = log.mock.calls.map((args) => String(args[0]));
    expect(lines).toHaveLength(2); // 本次问候 + 历史里刚生成的这一条
    expect(lines[0]).toBe(lines[1]);
    expect(lines[0]).toMatch(/, Ada\.$/);
  });
});
