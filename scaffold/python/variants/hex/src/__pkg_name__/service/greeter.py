"""Greeter use case：编排领域规则与端口，不关心具体实现。"""

from __pkg_name__.domain.greeting import Greeting, greeting_for
from __pkg_name__.domain.ports import Clock, GreetingLog


class Greeter:
    """问候用例：应用规则生成问候并记录历史；recent 读取历史。"""

    def __init__(self, clock: Clock, log: GreetingLog) -> None:
        self._clock = clock
        self._log = log

    def greet(self, name: str) -> Greeting:
        greeting = greeting_for(self._clock.current_hour(), name)
        self._log.save(greeting)
        return greeting

    def recent(self, limit: int) -> list[Greeting]:
        return self._log.recent(limit)
