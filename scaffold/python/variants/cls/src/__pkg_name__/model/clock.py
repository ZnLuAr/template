"""Clock 接口：按需引入（见 docs/reference/layout.md 渐进条款）。

logic 需要替身测试或换实现时才在这里定义接口，infra 提供实现。
"""

from typing import Protocol


class Clock(Protocol):
    """当前时刻的来源（真实实现见 infra，测试用 fake）。"""

    def current_hour(self) -> int: ...
