/**
 * SystemClock：model.Clock 接口的实现，本目录唯一的系统时间触点。
 */

import type { Clock } from "../model/clock.js";

export class SystemClock implements Clock {
  currentHour(): number {
    return new Date().getHours();
  }
}
