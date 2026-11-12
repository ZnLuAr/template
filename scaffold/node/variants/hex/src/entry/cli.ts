/**
 * CLI 入口：参数翻译、组装依赖、输出结果；不含业务规则。
 */

import { SystemClock } from "../infra/systemClock.js";
import { Greeter } from "../service/greeter.js";

/** 以给定参数运行 CLI，返回进程退出码（可测试）。 */
export function run(argv: readonly string[]): number {
  const name = argv[0] ?? "world";

  const greeter = new Greeter(new SystemClock()); // 组装只发生在 entry
  console.log(greeter.greet(name));
  return 0;
}

// 直接以 `node cli.js` / `tsx cli.ts` 运行时才执行；被 import（测试）时不执行。
const entry = process.argv[1] ?? "";
if (entry.endsWith("cli.js") || entry.endsWith("cli.ts")) {
  process.exitCode = run(process.argv.slice(2));
}
