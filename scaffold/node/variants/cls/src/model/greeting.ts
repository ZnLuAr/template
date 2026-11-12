/**
 * Greeting 策略：纯业务规则，零 IO。
 */

export class InvalidHourError extends Error {
  constructor(hour: number) {
    super(`hour 必须在 0..23，收到 ${hour}`);
    this.name = "InvalidHourError";
  }
}

function partFor(hour: number): string {
  if (hour >= 5 && hour < 12) return "Good morning";
  if (hour >= 12 && hour < 18) return "Good afternoon";
  if (hour >= 18 && hour < 23) return "Good evening";
  return "Good night";
}

/** 按一天中的时刻（0..23）生成问候语；hour 越界抛 InvalidHourError。 */
export function greetingFor(hour: number, name: string): string {
  if (!Number.isInteger(hour) || hour < 0 || hour > 23) {
    throw new InvalidHourError(hour);
  }
  return `${partFor(hour)}, ${name}.`;
}
