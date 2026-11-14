"""InMemoryGreetingLog：domain.GreetingLog 端口的内存实现。

演示用；换文件 / DB 存储时新写 adapter 即可，domain 与 service 不动。
"""

from __pkg_name__.domain.greeting import Greeting


class InMemoryGreetingLog:
    """进程内保存问候历史，最近的在前。"""

    def __init__(self) -> None:
        self._items: list[Greeting] = []

    def save(self, greeting: Greeting) -> None:
        self._items.append(greeting)

    def recent(self, limit: int) -> list[Greeting]:
        if limit <= 0:
            return []
        return list(reversed(self._items[-limit:]))
