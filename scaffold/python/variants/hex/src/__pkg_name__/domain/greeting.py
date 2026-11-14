"""Greeting 实体与生成规则：纯领域规则，零 IO。"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Greeting:
    """一条已生成的问候（领域对象，携带规则输入与输出）。"""

    hour: int
    name: str
    text: str


def greeting_for(hour: int, name: str) -> Greeting:
    """按一天中的时刻（0..23）生成问候。

    Raises:
        ValueError: hour 越界。
    """
    if not 0 <= hour <= 23:
        raise ValueError(f"hour 必须在 0..23，收到 {hour}")
    if 5 <= hour < 12:
        part = "Good morning"
    elif 12 <= hour < 18:
        part = "Good afternoon"
    elif 18 <= hour < 23:
        part = "Good evening"
    else:
        part = "Good night"
    return Greeting(hour=hour, name=name, text=f"{part}, {name}.")
