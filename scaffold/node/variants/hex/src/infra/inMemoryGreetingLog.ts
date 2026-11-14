/**
 * InMemoryGreetingLog：domain.GreetingLog 端口的内存实现。
 * 演示用；换文件 / DB 存储时新写 adapter 即可，domain 与 service 不动。
 */

import type { Greeting } from "../domain/greeting.js";
import type { GreetingLog } from "../domain/greetingLog.js";

export class InMemoryGreetingLog implements GreetingLog {
  private readonly items: Greeting[] = [];

  save(greeting: Greeting): void {
    this.items.push(greeting);
  }

  recent(limit: number): Greeting[] {
    if (limit <= 0) return [];
    return [...this.items.slice(-limit)].reverse();
  }
}
