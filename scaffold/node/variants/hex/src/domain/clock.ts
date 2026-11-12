/**
 * 端口定义：infra 负责实现，service 只依赖这里的接口。
 */

/** 当前时刻的来源（真实实现见 infra，测试用 fake）。 */
export interface Clock {
  currentHour(): number;
}
