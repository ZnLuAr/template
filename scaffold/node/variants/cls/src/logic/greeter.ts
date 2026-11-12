/**
 * Greeter 业务逻辑：编排规则与外部能力，不关心具体实现。
 */

import type { Clock } from "../model/clock.js";
import { greetingFor } from "../model/greeting.js";

export class Greeter {
  constructor(private readonly clock: Clock) {}

  greet(name: string): string {
    return greetingFor(this.clock.currentHour(), name);
  }
}
