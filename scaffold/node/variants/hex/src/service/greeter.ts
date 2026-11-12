/**
 * Greeter use case：编排领域规则与端口，不关心具体实现。
 */

import type { Clock } from "../domain/clock.js";
import { greetingFor } from "../domain/greeting.js";

export class Greeter {
  constructor(private readonly clock: Clock) {}

  greet(name: string): string {
    return greetingFor(this.clock.currentHour(), name);
  }
}
