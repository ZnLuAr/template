/**
 * CLI 入口：参数翻译、组装依赖、输出结果；不含业务规则。
 */

import { InMemoryGreetingLog } from "../infra/inMemoryGreetingLog.js";
import { SystemClock } from "../infra/systemClock.js";
import { Greeter } from "../service/greeter.js";

/** 以给定参数运行 CLI，返回进程退出码（可测试）。 */
export function run(argv: readonly string[]): number {
  // 极简参数解析：第一个参数是名字；--recent N 表示问候后打印最近 N 条历史。
  const recentIndex = argv.indexOf("--recent");
  const count = recentIndex >= 0 ? Number(argv[recentIndex + 1] ?? "0") : 0;
  const recent = Number.isInteger(count) && count > 0 ? count : 0;
  const name = argv[0] !== undefined && recentIndex !== 0 ? argv[0] : "world";

  const greeter = new Greeter(new SystemClock(), new InMemoryGreetingLog()); // 组装只发生在 entry
  console.log(greeter.greet(name).text);
  for (const item of greeter.recent(recent)) {
    console.log(item.text);
  }
  return 0;
}

// 直接以 `node cli.js` / `tsx cli.ts` 运行时才执行；被 import（测试）时不执行。
const entry = process.argv[1] ?? "";
if (entry.endsWith("cli.js") || entry.endsWith("cli.ts")) {
  process.exitCode = run(process.argv.slice(2));
}
