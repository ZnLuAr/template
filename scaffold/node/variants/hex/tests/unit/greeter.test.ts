import { describe, expect, it } from "vitest";

import type { Clock } from "../../src/domain/clock.js";
import type { Greeting } from "../../src/domain/greeting.js";
import type { GreetingLog } from "../../src/domain/greetingLog.js";
import { Greeter } from "../../src/service/greeter.js";

// fake 替身：Clock 与 GreetingLog，service 全程无真实 IO。
class FakeClock implements Clock {
  constructor(private readonly hour: number) {}

  currentHour(): number {
    return this.hour;
  }
}

class FakeLog implements GreetingLog {
  readonly saved: Greeting[] = [];

  save(greeting: Greeting): void {
    this.saved.push(greeting);
  }

  recent(limit: number): Greeting[] {
    return limit > 0 ? [...this.saved.slice(-limit)].reverse() : [];
  }
}

describe("Greeter", () => {
  it("应用规则并记入历史", () => {
    const log = new FakeLog();
    const greeting = new Greeter(new FakeClock(9), log).greet("Ada");

    expect(greeting.text).toBe("Good morning, Ada.");
    expect(log.saved).toEqual([greeting]); // 编排可见：规则被应用，副作用被记录
  });

  it("recent 经端口读取历史", () => {
    const greeter = new Greeter(new FakeClock(9), new FakeLog());
    greeter.greet("Ada");
    greeter.greet("Grace");

    expect(greeter.recent(1).map((g) => g.name)).toEqual(["Grace"]);
  });
});
