/**
 * 命令型端口：问候历史的存储；infra 提供实现，service 只依赖此接口。
 */

import type { Greeting } from "./greeting.js";

/** 问候历史的存储（真实实现见 infra，测试用 fake）。 */
export interface GreetingLog {
  save(greeting: Greeting): void;
  recent(limit: number): Greeting[];
}
