/**
 * Greeter use case：编排领域规则与端口，不关心具体实现。
 */

import type { Clock } from "../domain/clock.js";
import { type Greeting, greetingFor } from "../domain/greeting.js";
import type { GreetingLog } from "../domain/greetingLog.js";

export class Greeter {
  constructor(
    private readonly clock: Clock,
    private readonly log: GreetingLog,
  ) {}

  /** 应用规则生成问候并记入历史。 */
  greet(name: string): Greeting {
    const greeting = greetingFor(this.clock.currentHour(), name);
    this.log.save(greeting);
    return greeting;
  }

  /** 读取最近 limit 条问候。 */
  recent(limit: number): Greeting[] {
    return this.log.recent(limit);
  }
}
