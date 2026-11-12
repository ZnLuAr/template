/**
 * Clock 接口：按需引入（见 docs/reference/layout.md 渐进条款）。
 * logic 需要替身测试或换实现时才需要它，infra 提供实现。
 */

/** 当前时刻的来源（真实实现见 infra，测试用 fake）。 */
export interface Clock {
  currentHour(): number;
}
