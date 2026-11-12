import { describe, expect, it } from "vitest";

import type { Clock } from "../../src/domain/clock.js";
import { Greeter } from "../../src/service/greeter.js";

// fake Clock 替身，测试不触真实时间。
class FakeClock implements Clock {
  constructor(private readonly hour: number) {}
  currentHour(): number {
    return this.hour;
  }
}

describe("Greeter", () => {
  it("上午问候", () => {
    expect(new Greeter(new FakeClock(9)).greet("Ada")).toBe("Good morning, Ada.");
  });

  it("晚上问候", () => {
    expect(new Greeter(new FakeClock(21)).greet("Ada")).toBe("Good evening, Ada.");
  });
});
