"""端口定义：查询型（Clock）与命令型（GreetingLog）。

infra 负责实现，service 只依赖这里的协议——外部世界从端口进入应用。
"""

from typing import Protocol

from __pkg_name__.domain.greeting import Greeting


class Clock(Protocol):
    """当前时刻的来源（查询型端口；真实实现见 infra，测试用 fake）。"""

    def current_hour(self) -> int: ...


class GreetingLog(Protocol):
    """问候历史的存储（命令型端口；真实实现见 infra，测试用 fake）。"""

    def save(self, greeting: Greeting) -> None: ...

    def recent(self, limit: int) -> list[Greeting]: ...
