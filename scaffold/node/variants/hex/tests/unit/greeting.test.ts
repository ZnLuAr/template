import { describe, expect, it } from "vitest";

import { greetingFor, InvalidHourError } from "../../src/domain/greeting.js";

describe("greetingFor", () => {
  it.each([
    [0, "Good night"],
    [4, "Good night"],
    [5, "Good morning"],
    [11, "Good morning"],
    [12, "Good afternoon"],
    [17, "Good afternoon"],
    [18, "Good evening"],
    [22, "Good evening"],
    [23, "Good night"],
  ])("hour=%i → %s", (hour, part) => {
    expect(greetingFor(hour, "Ada")).toBe(`${part}, Ada.`);
  });

  it.each([-1, 24, 99, 9.5])("hour=%i 越界报错", (hour) => {
    expect(() => greetingFor(hour, "Ada")).toThrow(InvalidHourError);
  });
});
