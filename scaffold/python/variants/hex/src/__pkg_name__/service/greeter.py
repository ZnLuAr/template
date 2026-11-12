"""Greeter use case：编排领域规则与端口，不关心具体实现。"""

from __pkg_name__.domain.greeting import greeting_for
from __pkg_name__.domain.ports import Clock


class Greeter:
    def __init__(self, clock: Clock) -> None:
        self._clock = clock

    def greet(self, name: str) -> str:
        return greeting_for(self._clock.current_hour(), name)
